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
