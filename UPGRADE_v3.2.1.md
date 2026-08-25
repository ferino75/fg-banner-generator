# Upgrade to FG Banner Generator v3.2.1

V3.2.1 changes the icon workflow so that Tabler SVG files are kept in the repository
and are NOT downloaded during every render.

## If upgrading an existing v3.2 repository

Your current `templates/icons/` directory already contains the icons synchronized
by v3.2. Keep those SVG files.

Replace/update these files from v3.2.1:

- `.github/workflows/render.yml`
- `README.md`

Keep these helper files as well:

- `sync_icons.py`
- `tabler-icons.json`
- `THIRD_PARTY_LICENSES.md`

Do NOT delete `templates/icons/`.

From now on, normal rendering uses the committed SVG files directly.

Only when you intentionally add or update Tabler icons run:

```bash
python sync_icons.py
git add templates/icons/
git commit -m "Update Tabler icons"
git push
```

GitHub Actions will then use those committed SVG files without downloading them.
