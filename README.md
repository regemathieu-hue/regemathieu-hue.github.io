# regemathieu-hue.github.io

Pages de support et politiques de confidentialité de mes applications iOS, publiées avec GitHub Pages sur https://regemathieu-hue.github.io/

Chaque page existe en 39 langues. Les textes sont dans `i18n/`, les pages HTML sont générées par `build.py`.

## Structure

```
index.html                       liste des applis
assets/style.css                 style commun (clair / sombre)
apps.json                        applis (id, nom, noms par langue facultatifs, date de mise à jour), auteur, e-mail
i18n/common/<langue>.json        textes communs (titres, liens, nom de la langue)
i18n/<appli>/<langue>.json       textes de l'appli (sous-titre, contact, FAQ, politique)
templates/                       gabarits HTML
build.py                         générateur (Python 3, sans dépendance)
validate_i18n.py                 vérifie qu'une traduction a la même structure que fr-FR
<appli>/index.html               support en français + redirection vers la langue du navigateur
<appli>/privacy.html             politique en français + redirection vers la langue du navigateur
<appli>/<langue>/index.html      support traduit        (généré, ne pas éditer)
<appli>/<langue>/privacy.html    politique traduite     (généré, ne pas éditer)
_redirections/                   pages à copier dans les anciens dépôts (non publiées)
```

Les URL déclarées dans App Store Connect ne changent pas : `<appli>/` et `<appli>/privacy.html`. Elles affichent le français, redirigent vers la langue du navigateur si elle est disponible (sinon vers l'anglais) et listent toutes les langues en bas de page. Chaque page porte des liens `hreflang` vers ses traductions.

## Langues

ar-SA, ca, cs, da, de-DE, el, en-AU, en-CA, en-GB, en-US, es-ES, es-MX, fi, fr-CA, fr-FR, he, hi, hr, hu, id, it, ja, ko, ms, nl-NL, no, pl, pt-BR, pt-PT, ro, ru, sk, sv, th, tr, uk, vi, zh-Hans, zh-Hant.

## Modifier un texte

1. Éditer `i18n/<appli>/<langue>.json` (ou `i18n/common/<langue>.json`). Le français (`fr-FR`) est la référence : toutes les langues doivent avoir la même structure (mêmes clés, même nombre de questions, de sections et de puces) et les mêmes balises (`<strong>`, `<a href>`, `<br>`) et placeholders (`{email}`, `{date}`).
2. Si le texte change de sens, mettre à jour les autres langues, et la date dans `apps.json`.
3. Lancer `python3 build.py`. Le script refuse de générer si une langue est incomplète ou mal structurée.
4. Commiter les fichiers générés.

## Ajouter une appli

1. Ajouter l'appli dans `apps.json` (`id` en minuscules avec tirets = dossier et URL). Si son nom change selon la langue, ajouter `"names": { "<langue>": "<nom>" }` ; les autres langues prennent `name`.
2. Créer `i18n/<appli>/fr-FR.json` sur le modèle d'une appli existante, puis les autres langues.
3. Lancer `python3 build.py`, ajouter l'appli dans `index.html`, commiter.
4. Renseigner dans App Store Connect :
   - URL de confidentialité : `https://regemathieu-hue.github.io/<appli>/privacy.html`
   - URL de support : `https://regemathieu-hue.github.io/<appli>/`

## URL actuelles

| Appli | Support | Confidentialité |
|---|---|---|
| Atelier Fichiers | https://regemathieu-hue.github.io/atelier-fichiers/ | https://regemathieu-hue.github.io/atelier-fichiers/privacy.html |
| Carnet de shooting (Shootbook) | https://regemathieu-hue.github.io/carnetshooting/ | https://regemathieu-hue.github.io/carnetshooting/privacy.html |
| Convert Everything | https://regemathieu-hue.github.io/convert-everything/ | https://regemathieu-hue.github.io/convert-everything/privacy.html |
| Flashbooth | https://regemathieu-hue.github.io/flashbooth/ | https://regemathieu-hue.github.io/flashbooth/privacy.html |
| Nuit Claire | https://regemathieu-hue.github.io/nuitclaire/ | https://regemathieu-hue.github.io/nuitclaire/privacy.html |

Une langue précise : `https://regemathieu-hue.github.io/<appli>/<langue>/` et `.../<langue>/privacy.html`.

`nuitclaire/soiree.html` est la page d'invitation ouverte par les liens « soirée » partagés depuis Nuit Claire : ne pas la renommer ni la déplacer, l'app pointe vers cette adresse.
