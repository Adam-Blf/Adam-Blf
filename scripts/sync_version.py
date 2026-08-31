#!/usr/bin/env python3
"""Propage le numero de VERSION vers le badge version du README.

VERSION est la source de verite. Le README ne fait que l'afficher, donc il ne
se saisit jamais a la main : `--write` le reecrit, `--check` echoue si les deux
ont diverge. Le mode check tourne en CI pour que la divergence soit vue rouge
plutot que decouverte six mois plus tard sur un README qui ment.

Stdlib uniquement, pas de dependance a installer.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(ROOT, "VERSION")
README = os.path.join(ROOT, "README.md")
BADGE = re.compile(r"(!\[Version\]\(https://img\.shields\.io/badge/version-)([^-]+)(-)")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def read_version():
    with open(VERSION_FILE, encoding="utf-8") as f:
        version = f.read().strip()
    if not SEMVER.match(version):
        raise SystemExit(f"VERSION invalide, semver attendu, lu: {version!r}")
    return version


def main(argv):
    write = "--write" in argv
    version = read_version()
    with open(README, encoding="utf-8") as f:
        content = f.read()

    found = BADGE.search(content)
    if not found:
        raise SystemExit("Badge version introuvable dans le README")

    if found.group(2) == version:
        print(f"OK version {version}")
        return 0

    if not write:
        print(f"KO badge README a {found.group(2)}, VERSION a {version}")
        print("Corriger avec: python scripts/sync_version.py --write")
        return 1

    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(BADGE.sub(rf"\g<1>{version}\g<3>", content, count=1))
    print(f"OK badge README aligne sur {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
