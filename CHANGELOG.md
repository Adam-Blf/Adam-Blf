# Changelog

Format [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/), versions en
[semver](https://semver.org/lang/fr/). La source de vérité du numéro est le
fichier `VERSION`, propagé au badge du README par `scripts/sync_version.py`.

## [2.0.0] - 2026-08-31

### Ajouté

- Sections de fond du README : À propos, Stack, Projets, Architecture. Le profil
  ne portait que des visuels et des compteurs, aucune information sur le parcours.
- Bloc de badges Adam-Blf standard, encadré par les sentinelles `adam-badges`.
- `VERSION` et `scripts/sync_version.py`, garde qui échoue si le badge du README
  diverge du fichier `VERSION`. Branchée en CI dans le workflow `profile-svg`.
- Ce CHANGELOG.

### Modifié

- Carte terminal : `M1` devient `M2` (rentrée de septembre 2026), et l'invite
  passe de la commune de résidence à `adam@paris`, l'implantation annoncée.

### Retiré

- La commune de résidence, qui apparaissait dans l'invite de la carte terminal
  et n'a pas à être publiée.

## [1.0.0] - 2026-07-12

Version attribuée rétroactivement le 31/08/2026 : le dépôt existe depuis le
09/12/2025 mais n'a jamais porté de numéro. La date retenue est celle du dernier
élément structurant, la carte terminal.

### Ajouté

- Carte terminal générée quotidiennement depuis l'API GitHub, en clair et sombre
  (12/07/2026).
- Snake des contributions et cartes de statistiques.
- Synchronisation des topics des dépôts Adam-Blf (03/05/2026).
