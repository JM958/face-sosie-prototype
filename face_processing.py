"""
Détection de visage et extraction d'encodage (face embeddings) via face_recognition.
"""
import face_recognition
import numpy as np

def detect_faces_and_embeddings(image_path: str):
    img = face_recognition.load_image_file(image_path)
    locations = face_recognition.face_locations(img, model="hog")
    encodings = face_recognition.face_encodings(img, locations)
    results = []
    for loc, emb in zip(locations, encodings):
        results.append({
            "location": loc,
            "encoding": np.array(emb, dtype=np.float32)
        })
    return results
