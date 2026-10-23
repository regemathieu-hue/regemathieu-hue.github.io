#!/usr/bin/env python3
"""Vérifie qu'un fichier de traduction a la même structure que la source fr-FR.
Usage : python3 validate_i18n.py i18n/<dossier>/<locale>.json [...]"""
import json, os, re, sys

TAG_RE = re.compile(r"<[^>]+>|\{[a-z_]+\}")

def shape(x):
    if isinstance(x, dict):
        return {k: shape(v) for k, v in x.items()}
    if isinstance(x, list):
        return [shape(v) for v in x]
    return "str"

def leaves(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f"{path}[{i}]")
    else:
        yield path, x

def check(path):
    src_path = os.path.join(os.path.dirname(path), "fr-FR.json")
    src = json.load(open(src_path, encoding="utf-8"))
    data = json.load(open(path, encoding="utf-8"))
    errors = []
    if shape(src) != shape(data):
        errors.append("structure différente de fr-FR.json (clés, nombre d'éléments FAQ/sections/blocs)")
        return errors
    sl, dl = dict(leaves(src)), dict(leaves(data))
    for k, v in sl.items():
        d = dl[k]
        if k.endswith(".lang") or k.endswith(".dir") or k.endswith(".name"):
            continue
        if sorted(TAG_RE.findall(v)) != sorted(TAG_RE.findall(d)):
            errors.append(f"{k}: balises/placeholders {TAG_RE.findall(v)} attendus, trouvé {TAG_RE.findall(d)}")
        if not d.strip():
            errors.append(f"{k}: vide")
        if "\n" in d:
            errors.append(f"{k}: contient un retour à la ligne")
    return errors

if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        errs = check(p)
        if errs:
            bad += 1
            print(f"ERREUR {p}")
            for e in errs:
                print("   " + e)
        else:
            print(f"ok {p}")
    sys.exit(1 if bad else 0)
