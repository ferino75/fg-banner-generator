#!/usr/bin/env python3
"""
Download the curated Tabler Icons set used by FG Banner Generator.

The local icon name is stable for projects.json; tabler-icons.json maps it
to the upstream Tabler filename.
"""

from __future__ import annotations
import argparse
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "tabler-icons.json"
DEST = ROOT / "templates" / "icons"

RAW_BASE = "https://raw.githubusercontent.com/tabler/tabler-icons/{branch}/icons/{variant}/{name}.svg"


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def normalize_svg(svg: str) -> str:
    # Tabler SVGs use currentColor, which is ideal for our inline CSS.
    # Keep upstream SVG semantics intact; only normalize the XML declaration.
    svg = svg.strip()
    if svg.startswith("<?xml"):
        svg = svg.split("?>", 1)[1].lstrip()
    return svg + "\n"


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "FG-Banner-Generator/3.2"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def sync(selected: set[str] | None = None) -> int:
    data = load_manifest()
    branch = data.get("branch", "main")
    variant = data.get("variant", "outline")
    icons = data["icons"]
    DEST.mkdir(parents=True, exist_ok=True)

    failures = 0
    for local_name, upstream_name in icons.items():
        if selected and local_name not in selected:
            continue

        url = RAW_BASE.format(
            branch=branch,
            variant=variant,
            name=upstream_name,
        )
        target = DEST / f"{local_name}.svg"

        try:
            svg = normalize_svg(fetch(url))
            target.write_text(svg, encoding="utf-8")
            print(f"✓ {local_name:<18} <- {upstream_name}.svg")
        except Exception as e:
            failures += 1
            print(f"✗ {local_name:<18} {e}")

    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "icons",
        nargs="*",
        help="Optional local icon names. Without arguments all curated icons are synced.",
    )
    args = ap.parse_args()

    failures = sync(set(args.icons) if args.icons else None)
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
