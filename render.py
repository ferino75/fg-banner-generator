#!/usr/bin/env python3
from __future__ import annotations
import argparse, asyncio, json, shutil, base64, mimetypes
from pathlib import Path
from typing import Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
PROJECTS_FILE = ROOT / 'projects.json'
TEMPLATES_DIR = ROOT / 'templates'
OUTPUT_DIR = ROOT / 'output'
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=select_autoescape(['html','xml']))

def load_data() -> dict[str, Any]:
    return json.loads(PROJECTS_FILE.read_text(encoding='utf-8'))

def merged_project(data, project):
    defaults = dict(data.get('defaults', {}))
    theme_name = project.get('theme', defaults.get('theme', 'orange'))
    theme = data.get('themes', {}).get(theme_name, {})
    cfg = {}; cfg.update(defaults); cfg.update(project)
    palette = {}; palette.update(defaults.get('palette', {})); palette.update(theme.get('palette', {})); palette.update(project.get('palette', {}))
    cfg['palette'] = palette
    return cfg

def projects():
    data = load_data()
    return [merged_project(data, p) for p in data.get('projects', [])]

def asset_data_uri(relative_path):
    if not relative_path:
        return None
    p = (ROOT / relative_path).resolve()
    if not p.exists():
        return None
    mime = mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
    data = base64.b64encode(p.read_bytes()).decode('ascii')
    return f"data:{mime};base64,{data}"

def render_html(project):
    t = env.get_template('banner.html')
    ctx = dict(project)
    ctx['logo_uri'] = asset_data_uri(project.get('logo'))
    ctx['css_text'] = (TEMPLATES_DIR / 'banner.css').read_text(encoding='utf-8')
    return t.render(**ctx)

async def render_png(project):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    w, h = int(project.get('width',1600)), int(project.get('height',700))
    out = OUTPUT_DIR / project.get('output', f"{project['id']}.png")
    html = render_html(project)
    async with async_playwright() as p:
        chromium = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
        launch_args = {"executable_path": chromium} if chromium else {}
        browser = await p.chromium.launch(**launch_args)
        page = await browser.new_page(viewport={'width':w,'height':h}, device_scale_factor=1)
        await page.set_content(html, wait_until='networkidle')
        await page.screenshot(path=str(out), full_page=False, clip={'x':0,'y':0,'width':w,'height':h})
        await browser.close()
    return out

def write_icon_catalog():
    manifest = json.loads((ROOT / "tabler-icons.json").read_text(encoding="utf-8"))
    t = env.get_template("icon-catalog.html")
    out = OUTPUT_DIR / "icons.html"
    out.write_text(t.render(icon_names=manifest["icons"].keys()), encoding="utf-8")
    return out

def write_preview():
    t = env.get_template('preview.html')
    out = OUTPUT_DIR/'index.html'
    out.write_text(t.render(projects=projects()), encoding='utf-8')
    return out

async def render_selected(ids=None):
    ps = projects()
    if ids is not None:
        known = {p['id'] for p in ps}; missing = set(ids)-known
        if missing: raise SystemExit('Unknown project(s): '+', '.join(sorted(missing)))
        ps = [p for p in ps if p['id'] in ids]
    for p in ps:
        out = await render_png(p)
        print(f"✓ {p['id']}: {out.relative_to(ROOT)}")
    print(f"✓ preview: {write_preview().relative_to(ROOT)}")
    print(f"✓ icons: {write_icon_catalog().relative_to(ROOT)}")

def main():
    ap = argparse.ArgumentParser(description='FG Banner Generator v3')
    ap.add_argument('command', help='list | all | preview | <project-id>')
    a = ap.parse_args()
    if a.command == 'list':
        for p in projects(): print(f"{p['id']:<22} FG {p['title']}")
    elif a.command == 'preview': print(write_preview())
    elif a.command == 'all': asyncio.run(render_selected())
    else: asyncio.run(render_selected([a.command]))
if __name__ == '__main__': main()
