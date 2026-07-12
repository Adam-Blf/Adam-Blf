#!/usr/bin/env python3
"""Genere assets/terminal-dark.svg et terminal-light.svg avec les stats GitHub.

Tourne en GitHub Actions (cron quotidien) avec GITHUB_TOKEN.
Stdlib uniquement, pas de dependance a installer.
"""
import datetime
import json
import os
import sys
import urllib.request

USER = "Adam-Blf"
BIRTHDATE = datetime.date(2004, 6, 20)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "assets", "terminal.template.svg")

PALETTES = {
    "dark": {
        "BG": "#0D1117",
        "BORDER": "#30363D",
        "TITLEBAR": "#161B22",
        "TEXT": "#C9D1D9",
        "LABEL": "#D4A437",
        "ACCENT": "#D4A437",
        "MUTED": "#8B949E",
        "PROMPT": "#3FB950",
    },
    "light": {
        "BG": "#FFFFFF",
        "BORDER": "#D0D7DE",
        "TITLEBAR": "#F6F8FA",
        "TEXT": "#24292F",
        "LABEL": "#B08020",
        "ACCENT": "#001329",
        "MUTED": "#6E7781",
        "PROMPT": "#1A7F37",
    },
}


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def uptime():
    today = datetime.date.today()
    years = today.year - BIRTHDATE.year
    last_bday = BIRTHDATE.replace(year=today.year)
    if last_bday > today:
        years -= 1
        last_bday = BIRTHDATE.replace(year=today.year - 1)
    days = (today - last_bday).days
    return f"{years} ans, {days} jours"


def collect():
    user = api(f"/users/{USER}")
    stars = 0
    page = 1
    while True:
        repos = api(f"/users/{USER}/repos?per_page=100&page={page}")
        if not repos:
            break
        stars += sum(r.get("stargazers_count", 0) for r in repos)
        if len(repos) < 100:
            break
        page += 1
    commits = api(f"/search/commits?q=author:{USER}").get("total_count", 0)
    return {
        "AGE": uptime(),
        "REPOS": str(user.get("public_repos", 0)),
        "STARS": str(stars),
        "FOLLOWERS": str(user.get("followers", 0)),
        "COMMITS": f"{commits:,}".replace(",", " "),
        "UPDATED": datetime.date.today().strftime("%d/%m/%Y"),
    }


def main():
    with open(TEMPLATE, encoding="utf-8") as f:
        template = f.read()
    stats = collect()
    for theme, colors in PALETTES.items():
        svg = template
        for key, value in {**colors, **stats}.items():
            svg = svg.replace("{" + key + "}", value)
        out = os.path.join(ROOT, "assets", f"terminal-{theme}.svg")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        print(f"OK {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
