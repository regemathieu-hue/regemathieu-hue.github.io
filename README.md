# regemathieu-hue.github.io

Pages de support et politiques de confidentialité de mes applications iOS, publiées avec GitHub Pages sur https://regemathieu-hue.github.io/

## Structure

```
index.html                 liste des applis
assets/style.css           style commun (clair / sombre)
<appli>/index.html         page de support
<appli>/privacy.html       politique de confidentialité
_redirections/             pages à copier dans les anciens dépôts (non publiées)
```

## Ajouter une appli

1. Copier le dossier `convert-everything/` sous un nouveau nom (minuscules, tirets).
2. Adapter le texte des deux pages.
3. Ajouter l'appli dans la liste de `index.html`.
4. Renseigner dans App Store Connect :
   - URL de confidentialité : `https://regemathieu-hue.github.io/<appli>/privacy.html`
   - URL de support : `https://regemathieu-hue.github.io/<appli>/`

## URL actuelles

| Appli | Support | Confidentialité |
|---|---|---|
| Atelier Fichiers | https://regemathieu-hue.github.io/atelier-fichiers/ | https://regemathieu-hue.github.io/atelier-fichiers/privacy.html |
| Convert Everything | https://regemathieu-hue.github.io/convert-everything/ | https://regemathieu-hue.github.io/convert-everything/privacy.html |
| Flashbooth | https://regemathieu-hue.github.io/flashbooth/ | https://regemathieu-hue.github.io/flashbooth/privacy.html |
| Nuit Claire | https://regemathieu-hue.github.io/nuitclaire/ | https://regemathieu-hue.github.io/nuitclaire/privacy.html |

`nuitclaire/soiree.html` est la page d'invitation ouverte par les liens « soirée » partagés depuis Nuit Claire : ne pas la renommer ni la déplacer, l'app pointe vers cette adresse.
