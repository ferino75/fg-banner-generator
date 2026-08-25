# FG Banner Generator v3 final

Finálna HTML/CSS + Jinja2 + Playwright verzia generátora jednotných FG bannerov v pomere **16:7**.

## Cieľ

Jedným skriptom generovať bannery, ktoré patria do jednej produktovej rodiny:

- tmavomodré technologické pozadie
- veľký glossy panel s logom naľavo
- výrazný headline na pravej strane
- slogan, divider line a 3–4 feature rows
- jednotná typografia a ikonografia

## Použitie

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Zoznam projektov:

```bash
python render.py list
```

Jeden banner:

```bash
python render.py email-remover
```

Všetky bannery:

```bash
python render.py all
```

Po vyrenderovaní vzniknú PNG bannery v `output/` a náhľadová stránka `output/index.html`.

## Obsah repozitára

```text
fg-banner-generator-v3/
├── render.py
├── projects.json
├── requirements.txt
├── templates/
│   ├── banner.html
│   ├── banner.css
│   ├── preview.html
│   └── icons/*.svg
├── assets/logos/
├── output/
└── .github/workflows/render.yml
```

## Testovacie projekty

Aktuálne sú pripravené tieto konfigurácie:

- `email-remover`
- `strip-comments`
- `auto-lightbox`

## Pridanie nového pluginu

1. vlož logo do `assets/logos/`
2. pridaj nový objekt do `projects.json`
3. spusti `python render.py <project-id>`

Vo väčšine prípadov nie je potrebné meniť Python ani CSS.

## Poznámka k logám

Ak reálne logo ešte nemáš pripravené, generátor použije `placeholder_logo`. To umožňuje rýchlo testovať layout aj bez finálnych assetov.

## FG Banner Style v1

Táto verzia je považovaná za základný master štýl pre ďalšie FG bannery. Pri ďalších pluginoch by sa mali meniť už len:

- logo
- názov
- slogan
- typ rozšírenia
- zoznam hlavných vlastností


## Logo tuning per project

V3.1 podporuje tieto parametre v `projects.json`:

```json
"logo_mode": "contain",
"logo_size": "90%",
"logo_scale": 1.0,
"logo_offset_x": 0,
"logo_offset_y": 0
```

Význam:

- `logo_mode` – `contain` alebo `full`
- `logo_size` – základná šírka/výška loga v paneli, napr. `90%` alebo `100%`
- `logo_scale` – jemné optické zväčšenie/zmenšenie, napr. `0.95`, `1`, `1.08`
- `logo_offset_x` – horizontálny posun v px
- `logo_offset_y` – vertikálny posun v px

Príklady:

```json
"logo_mode": "contain",
"logo_size": "90%",
"logo_scale": 1.0
```

```json
"logo_mode": "full",
"logo_size": "100%",
"logo_scale": 1.05,
"logo_offset_x": 0,
"logo_offset_y": 0
```


## Tabler Icons – V3.2

V3.2 štandardizuje feature ikonky na **Tabler Icons / Outline**. Tabler používa
24×24 mriežku a 2px stroke, takže ikony sú vizuálne konzistentné naprieč bannermi.

Kurátorovaná sada je definovaná v:

```text
tabler-icons.json
```

Aktuálne obsahuje viac než 30 praktických ikon, napr.:

```text
shield
shield-check
image
photo
code
puzzle
bolt
broom
link
check
database
world
lock
settings
language
eye
file
files
mail
at
user
users
search
filter
download
upload
refresh
trash
replace
device-desktop
browser
server
```

### Synchronizácia ikon

Pred prvým lokálnym renderom alebo po zmene `tabler-icons.json`:

```bash
python sync_icons.py
```

Alebo iba konkrétne ikonky:

```bash
python sync_icons.py database server lock
```

GitHub Actions ich synchronizuje automaticky pred renderovaním.

### Použitie v projects.json

```json
{
  "icon": "database",
  "heading": "Database access",
  "description": "..."
}
```

Generátor následne vloží:

```text
templates/icons/database.svg
```

### Vlastná ikona

Stále môžeš pridať aj vlastné SVG priamo do `templates/icons/`.
Ak napríklad vytvoríš:

```text
templates/icons/my-special-icon.svg
```

v `projects.json` použiješ:

```json
"icon": "my-special-icon"
```

Odporúčané je držať vlastné ikony v rovnakom štýle: `viewBox="0 0 24 24"`,
outline, `currentColor`, približne 2px stroke.

Licenčné informácie pre Tabler sú v `THIRD_PARTY_LICENSES.md`.
