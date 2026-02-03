"""
Construire un index FAISS depuis un répertoire d'images / metadata.
"""
import os
import json
import numpy as np
import faiss
from glob import glob
from download_and_exif import get_exif_date
from face_processing import detect_faces_and_embeddings
from config import IMAGES_DIR, DATA_DIR, METADATA_FILE, INDEX_FILE

def build_index(images_dir=IMAGES_DIR, out_index_path=INDEX_FILE):
    metadata = []
    embeddings = []
    files = glob(os.path.join(images_dir, "*.jpg")) + glob(os.path.join(images_dir, "*.jpeg")) + glob(os.path.join(images_dir, "*.png"))
    for p in files:
        faces = detect_faces_and_embeddings(p)
        for i, f in enumerate(faces):
            emb = f["encoding"]
            embeddings.append(emb)
            meta = {
                "image_path": p,
                "face_idx": i,
                "location": f["location"],
                "exif_date": None
            }
            dt = get_exif_date(p)
            if dt:
                meta["exif_date"] = dt.isoformat()
            metadata.append(meta)
    if len(embeddings) == 0:
        raise RuntimeError("Aucun visage trouvé. Index vide.")
    X = np.vstack(embeddings).astype('float32')
    dim = X.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(X)
    faiss.write_index(index, out_index_path)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print("Index construit: %d vecteurs" % X.shape[0])
    return index, metadata

if __name__ == "__main__":
    print("Construction de l'index depuis", IMAGES_DIR)
    build_index()