"""
Télécharge les images et extrait EXIF/DateTimeOriginal si présent.
"""
import os
import requests
from PIL import Image
from io import BytesIO
import piexif
from datetime import datetime
from typing import Optional

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def download_image(url: str, out_path: str) -> bool:
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print("Download failed:", e)
        return False

def get_exif_date(path: str) -> Optional[datetime]:
    try:
        img = Image.open(path)
        exif_bytes = img.info.get("exif")
        if not exif_bytes:
            return None
        exif_dict = piexif.load(exif_bytes)
        dt = exif_dict["0th"].get(piexif.ImageIFD.DateTime)
        if dt:
            if isinstance(dt, bytes):
                dt = dt.decode("utf8")
            return datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None
    return None
