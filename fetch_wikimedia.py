"""
Recherche d'images sur Wikimedia Commons pour un nom et une année.
Retourne liste de dict: {pageid, title, image_url, extmetadata}
"""
import requests
import time
from typing import List, Dict

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"

def search_commons_images(name: str, year: int, limit: int = 50) -> List[Dict]:
    q = f"{name} {year}"
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo|pageprops",
        "generator": "search",
        "gsrsearch": q,
        "gsrlimit": limit,
        "iiprop": "url|extmetadata",
        "iiurlwidth": 800,
    }
    r = requests.get(WIKIMEDIA_API, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    results = []
    pages = data.get("query", {}).get("pages", {})
    for pageid, p in pages.items():
        if "imageinfo" in p:
            for info in p["imageinfo"]:
                results.append({
                    "pageid": pageid,
                    "title": p.get("title"),
                    "image_url": info.get("thumburl") or info.get("url"),
                    "extmetadata": info.get("extmetadata", {}),
                })
    time.sleep(0.5)
    return results

def extract_license(extmetadata: Dict) -> str:
    lic = extmetadata.get("LicenseShortName", {}).get("value")
    return lic.lower() if lic else ""