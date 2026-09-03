from pathlib import Path
from PIL import Image

VALID = {".jpg", ".jpeg", ".png", ".webp"}

def clean_dataset(source="ml/data/raw/garbage_classification"):
    source = Path(source)
    bad = []
    for p in source.rglob("*"):
        if p.is_file() and p.suffix.lower() in VALID:
            try:
                with Image.open(p) as im:
                    im.verify()
            except Exception:
                bad.append(str(p))
    print(f"Corrupt images found: {len(bad)}")
    return bad

if __name__ == "__main__":
    clean_dataset()
