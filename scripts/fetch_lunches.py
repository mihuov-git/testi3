import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "lunches.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LunchBot/1.0; +https://github.com/)"
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def unique_keep_order(items):
    seen = set()
    out = []
    for item in items:
        key = item.strip()
        if key and key not in seen:
            seen.add(key)
            out.append(key)
    return out


def fetch_aitiopaikka():
    url = "https://www.frescoravintolat.fi/lounas/aitiopaikan-lounaslista/"
    items = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        lines = [clean_text(x.get_text(" ", strip=True)) for x in soup.find_all(["h1", "h2", "h3", "p", "li"])]
        lines = [x for x in lines if x]

        start = None
        end = None

        for i, line in enumerate(lines):
            if "maanantai" in line.lower():
                start = i
                break

        for i, line in enumerate(lines):
            low = line.lower()
            if "l = laktoositon" in low or "lihojen ja broilerin alkuperämaa" in low:
                end = i
                break

        if start is not None:
            section = lines[start:end] if end else lines[start:start + 40]
            items = unique_keep_order(section)

        if not items:
            items = ["Lounasta ei saatu haettua tällä hetkellä."]
    except Exception as e:
        items = [f"Lounaan haku epäonnistui: {type(e).__name__}"]

    return {
        "name": "Aitiopaikka",
        "url": url,
        "items": items,
    }


def fetch_viides_nayttamo():
    url = "https://www.viidesnayttamo.fi/?page_id=73"
    items = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        text = clean_text(soup.get_text("\n", strip=True))
        raw_lines = [clean_text(x) for x in text.split("\n")]
        lines = [x for x in raw_lines if x]

        weekdays = ("maanantai", "tiistai", "keskiviikko", "torstai", "perjantai")
        start = None
        end = None

        for i, line in enumerate(lines):
            if any(day in line.lower() for day in weekdays):
                start = i
                break

        for i, line in enumerate(lines):
            low = line.lower()
            if "kysy henkilökunnalta lisää allergeeneista" in low or "pidätämme oikeuden hinnanmuutoksiin" in low:
                end = i + 1
                break

        if start is not None:
            section = lines[start:end] if end else lines[start:start + 50]
            items = unique_keep_order(section)

        if not items:
            items = ["Lounasta ei saatu haettua tällä hetkellä."]
    except Exception as e:
        items = [f"Lounaan haku epäonnistui: {type(e).__name__}"]

    return {
        "name": "Viides Näyttämö",
        "url": "https://www.viidesnayttamo.fi/",
        "source_url": url,
        "items": items,
    }


def fetch_grill_it():
    url = "https://www.raflaamo.fi/fi/ravintola/turku/grill-it-marina-turku/menu/lounas"
    items = []

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        text = clean_text(soup.get_text("\n", strip=True))
        raw_lines = [clean_text(x) for x in text.split("\n")]
        lines = [x for x in raw_lines if x]

        weekdays = ("maanantai", "tiistai", "keskiviikko", "torstai", "perjantai")
        start = None
        end = None

        for i, line in enumerate(lines):
            if any(day in line.lower() for day in weekdays):
                start = i
                break

        for i, line in enumerate(lines):
            low = line.lower()
            if "lounaan hintaan sisältyy" in low and i > (start or 0):
                end = i
                break

        if start is not None:
            section = lines[start:end] if end else lines[start:start + 80]
            items = unique_keep_order(section)

        if not items:
            items = ["Lounasta ei saatu haettua tällä hetkellä."]
    except Exception as e:
        items = [f"Lounaan haku epäonnistui: {type(e).__name__}"]

    return {
        "name": "Grill it! Marina",
        "url": url,
        "items": items,
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "restaurants": [
            fetch_aitiopaikka(),
            fetch_viides_nayttamo(),
            fetch_grill_it(),
        ],
    }

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
