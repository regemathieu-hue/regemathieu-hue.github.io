#!/usr/bin/env python3
"""Génère les pages support et confidentialité de chaque appli dans toutes les langues.

Usage : python3 build.py

Entrées :
  apps.json                   applis (id, name, date de mise à jour, langues facultatives), auteur, e-mail
  i18n/common/<locale>.json   chaînes communes (titres, liens, nom de la langue)
  i18n/<appli>/<locale>.json  contenu de l'appli (FAQ, sections de la politique)
  templates/*.html            gabarits

Sorties (commitées, servies par GitHub Pages) :
  <appli>/index.html             page de support en français + redirection vers la langue du navigateur
  <appli>/privacy.html           politique en français + redirection vers la langue du navigateur
  <appli>/<locale>/index.html    page de support traduite
  <appli>/<locale>/privacy.html  politique traduite

Une appli peut limiter ses langues avec « locales » dans apps.json (ex. "locales": ["fr-FR"] pour une appli vendue
dans une seule langue). Avec une seule langue, seules les deux pages racine sont générées, sans redirection ni liste
de langues.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
I18N = os.path.join(ROOT, "i18n")
TPL = os.path.join(ROOT, "templates")
sys.path.insert(0, ROOT)
from validate_i18n import check  # noqa: E402


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_json(path):
    return json.load(open(path, encoding="utf-8"))


def load_locales(cfg):
    """Retourne {locale: {"common": {...}, "<app id>": {...}}} après validation."""
    common_dir = os.path.join(I18N, "common")
    locales = sorted(n[:-5] for n in os.listdir(common_dir) if n.endswith(".json"))
    only = os.environ.get("BUILD_LOCALES")  # ex. BUILD_LOCALES=fr-FR,en-US pour un essai partiel
    if only:
        locales = [l for l in locales if l in only.split(",")]
    data, errors = {}, []
    for loc in locales:
        data[loc] = {}
        for folder in ["common"] + [a["id"] for a in cfg["apps"] if loc in a.get("locales", [loc])]:
            path = os.path.join(I18N, folder, f"{loc}.json")
            if not os.path.exists(path):
                errors.append(f"{folder}/{loc}.json manquant")
                continue
            for e in check(path):
                errors.append(f"{folder}/{loc}.json : {e}")
            data[loc][folder] = load_json(path)
    if errors:
        print("Erreurs de traduction :", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    return data


def app_locales(app, locales):
    """Langues d'une appli : toutes, ou celles de « locales » dans apps.json."""
    if "locales" not in app:
        return locales
    missing = [loc for loc in app["locales"] if loc not in locales]
    if missing and not os.environ.get("BUILD_LOCALES"):
        sys.exit(f'{app["id"]} : langue(s) inconnue(s) dans apps.json : {", ".join(missing)}')
    return {loc: strings for loc, strings in locales.items() if loc in app["locales"]}


def single_language(page):
    """Retire d'une page le lien « Autres langues » et la liste des langues (appli dans une seule langue)."""
    lines, out, skipping = page.split("\n"), [], False
    for line in lines:
        if 'class="lang-switch"' in line:
            continue
        if '<h2 id="languages">' in line:
            skipping = True
        if not skipping:
            out.append(line)
        elif line.strip() == "</ul>":
            skipping = False
    text = "\n".join(out)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text


def app_name(app, loc):
    """Nom de l'appli dans une langue : « names » (facultatif) dans apps.json, sinon « name »."""
    return app.get("names", {}).get(loc, app["name"])


def fill(text, cfg):
    email = cfg["email"]
    return text.replace("{email}", f'<a href="mailto:{email}">{email}</a>')


def alternates(cfg, app, page, locales):
    if len(locales) < 2:
        return ""
    base = f'{cfg["base_url"]}/{app["id"]}'
    lines = [f'  <link rel="alternate" hreflang="{loc}" href="{base}/{loc}/{page}">' for loc in locales]
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{base}/{page}">')
    return "\n".join(lines) + "\n"


def language_links(locales, page, current, prefix):
    items = []
    for loc, strings in locales.items():
        label = html.escape(strings["common"]["name"])
        if loc == current:
            items.append(f"    <li><strong>{label}</strong></li>")
        else:
            items.append(f'    <li><a href="{prefix}{loc}/{page}" hreflang="{loc}" lang="{loc}">{label}</a></li>')
    return "\n".join(items)


REDIRECT = """  <script>
  (function () {
    var available = %s, skip = %s, fallback = %s;
    var langs = (navigator.languages || [navigator.language || ""]).map(String);
    var target = null;
    for (var i = 0; i < langs.length && !target; i++) {
      var l = langs[i], base = l.split("-")[0].toLowerCase();
      if (available.indexOf(l) >= 0) { target = l; break; }
      if (base === "zh") {
        var zh = /hant|tw|hk|mo/i.test(l) ? "zh-Hant" : "zh-Hans";
        if (available.indexOf(zh) >= 0) { target = zh; break; }
      }
      for (var j = 0; j < available.length; j++) {
        if (available[j].split("-")[0].toLowerCase() === base) { target = available[j]; break; }
      }
    }
    target = target || fallback;
    if (target && skip.indexOf(target) < 0) { location.replace(target + "/%s"); }
  })();
  </script>
"""


def redirect_script(cfg, locales, page):
    if len(locales) < 2:
        return ""
    fallback = cfg["fallback_locale"] if cfg["fallback_locale"] in locales else cfg["default_locale"]
    return REDIRECT % (
        json.dumps(list(locales)),
        json.dumps([cfg["default_locale"]]),
        json.dumps(fallback),
        page,
    )


def render_support(cfg, app, loc, locales, tpl, root_page):
    c = locales[loc]["common"]
    s = locales[loc][app["id"]]["support"]
    faq = "".join(
        f'  <div class="faq-item">\n    <p class="faq-q">{fill(item["q"], cfg)}</p>\n'
        f'    <p class="faq-a">{fill(item["a"], cfg)}</p>\n  </div>\n\n'
        for item in s["faq"]
    )
    return tpl.format(
        lang=c["lang"], dir=c["dir"], app=html.escape(app_name(app, loc)),
        support_title=c["support_title"], root="../" if root_page else "../../",
        alternates=alternates(cfg, app, "index.html", locales),
        redirect=redirect_script(cfg, locales, "index.html") if root_page else "",
        subtitle=fill(s["subtitle"], cfg), other_languages=c["other_languages"],
        contact_h=c["contact_h"], contact=fill(s["contact"], cfg), faq_h=c["faq_h"], faq=faq,
        privacy_h=c["privacy_h"], privacy_summary=fill(s["privacy_summary"], cfg),
        read_full_privacy=c["read_full_privacy"], language_list_h=c["language_list_h"],
        languages=language_links(locales, "index.html", None if root_page else loc, "" if root_page else "../"),
        year=cfg["year"], author=html.escape(cfg["author"]), home="../" if root_page else "../../",
        all_apps=c["all_apps"],
    )


def render_privacy(cfg, app, loc, locales, tpl, root_page):
    c = locales[loc]["common"]
    p = locales[loc][app["id"]]["privacy"]
    out = []
    for section in p["sections"]:
        out.append(f"  <h2>{fill(section['h'], cfg)}</h2>")
        for block in section["blocks"]:
            if "p" in block:
                out.append(f"  <p>{fill(block['p'], cfg)}</p>")
            else:
                out.append("  <ul>")
                out.extend(f"    <li>{fill(item, cfg)}</li>" for item in block["ul"])
                out.append("  </ul>")
        out.append("")
    return tpl.format(
        lang=c["lang"], dir=c["dir"], app=html.escape(app_name(app, loc)),
        privacy_title=c["privacy_title"], root="../" if root_page else "../../",
        alternates=alternates(cfg, app, "privacy.html", locales),
        redirect=redirect_script(cfg, locales, "privacy.html") if root_page else "",
        back_to_support=c["back_to_support"],
        updated=c["updated"].replace("{date}", app["updated"]),
        other_languages=c["other_languages"], sections="\n".join(out),
        language_list_h=c["language_list_h"],
        languages=language_links(locales, "privacy.html", None if root_page else loc, "" if root_page else "../"),
        year=cfg["year"], author=html.escape(cfg["author"]), home="../" if root_page else "../../",
        all_apps=c["all_apps"],
    )


def main():
    cfg = load_json(os.path.join(ROOT, "apps.json"))
    locales = load_locales(cfg)
    support_tpl = read(os.path.join(TPL, "support.html"))
    privacy_tpl = read(os.path.join(TPL, "privacy.html"))
    count = 0
    for app in cfg["apps"]:
        app_dir = os.path.join(ROOT, app["id"])
        own = app_locales(app, locales)
        if not own:
            continue  # essai partiel (BUILD_LOCALES) sans aucune langue de cette appli
        if len(own) == 1:
            # Une seule langue : les deux pages racine suffisent.
            loc = next(iter(own))
            write(os.path.join(app_dir, "index.html"),
                  single_language(render_support(cfg, app, loc, own, support_tpl, True)))
            write(os.path.join(app_dir, "privacy.html"),
                  single_language(render_privacy(cfg, app, loc, own, privacy_tpl, True)))
            count += 2
            continue
        for loc in own:
            write(os.path.join(app_dir, loc, "index.html"), render_support(cfg, app, loc, own, support_tpl, False))
            write(os.path.join(app_dir, loc, "privacy.html"), render_privacy(cfg, app, loc, own, privacy_tpl, False))
            count += 2
        loc = cfg["default_locale"] if cfg["default_locale"] in own else next(iter(own))
        write(os.path.join(app_dir, "index.html"), render_support(cfg, app, loc, own, support_tpl, True))
        write(os.path.join(app_dir, "privacy.html"), render_privacy(cfg, app, loc, own, privacy_tpl, True))
        count += 2
    print(f"{count} pages générées pour {len(cfg['apps'])} applis et {len(locales)} langues.")


if __name__ == "__main__":
    main()
