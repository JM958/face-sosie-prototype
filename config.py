# Configuration générale
ALLOWED_LICENSES = ("public domain", "cc-by", "cc-by-sa", "cc-zero", "cc0")
ALLOW_MINORS = False  # NE PAS activer — risqué et souvent illégal sans consentement
AGE_TOLERANCE_YEARS = 1

DATA_DIR = "data"
IMAGES_DIR = f"{DATA_DIR}/images"
INDEX_FILE = f"{DATA_DIR}/faiss.index"
METADATA_FILE = f"{DATA_DIR}/metadata.json"