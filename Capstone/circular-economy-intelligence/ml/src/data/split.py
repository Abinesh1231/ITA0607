from pathlib import Path
import random
import shutil

SEED = 42
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def split_dataset(source="ml/data/raw/garbage_classification", output="ml/data/processed",
                  train_ratio=0.7, val_ratio=0.15):
    random.seed(SEED)
    source, output = Path(source), Path(output)
    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")

    for cls_dir in sorted(p for p in source.iterdir() if p.is_dir()):
        images = [p for p in cls_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS]
        random.shuffle(images)
        n = len(images)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        splits = {
            "train": images[:n_train],
            "val": images[n_train:n_train+n_val],
            "test": images[n_train+n_val:],
        }
        for split, items in splits.items():
            target = output / split / cls_dir.name
            target.mkdir(parents=True, exist_ok=True)
            for image in items:
                destination = target / image.name
                if not destination.exists():
                    shutil.copy2(image, destination)
        print(cls_dir.name, {k: len(v) for k,v in splits.items()})

if __name__ == "__main__":
    split_dataset()
