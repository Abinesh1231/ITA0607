from pathlib import Path
import random

import matplotlib.pyplot as plt
from PIL import Image


DATASET_DIR = Path("ml/data/processed/train")
OUTPUT_DIR = Path("ml/outputs/plots")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CLASSES = [
    "battery",
    "biological",
    "brown-glass",
    "cardboard",
    "clothes",
    "green-glass",
    "metal",
    "paper",
    "plastic",
    "shoes",
    "trash",
    "white-glass",
]

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
}


def get_images(class_name, count=4):
    folder = DATASET_DIR / class_name

    images = [
        p
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    random.seed(42)
    random.shuffle(images)

    return images[:count]


def create_sample_grid():

    fig, axes = plt.subplots(
        4,
        12,
        figsize=(24, 10)
    )

    for col, class_name in enumerate(CLASSES):

        samples = get_images(class_name, 4)

        for row in range(4):

            ax = axes[row, col]

            if row < len(samples):

                try:

                    image = Image.open(
                        samples[row]
                    ).convert("RGB")

                    ax.imshow(image)

                except Exception:

                    ax.text(
                        0.5,
                        0.5,
                        "Image error",
                        ha="center",
                        va="center"
                    )

            else:

                ax.text(
                    0.5,
                    0.5,
                    "No image",
                    ha="center",
                    va="center"
                )

            ax.axis("off")

            if row == 0:
                ax.set_title(
                    class_name,
                    fontsize=9
                )

    fig.suptitle(
        "Waste Dataset - Sample Images from All 12 Classes",
        fontsize=18
    )

    fig.tight_layout()

    output_file = (
        OUTPUT_DIR /
        "dataset_samples_all_classes.png"
    )

    fig.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

    print(
        f"Saved visualization to: {output_file}"
    )


def create_class_distribution():

    counts = []

    for class_name in CLASSES:

        folder = DATASET_DIR / class_name

        count = len([
            p
            for p in folder.iterdir()
            if p.is_file()
            and p.suffix.lower() in IMAGE_EXTENSIONS
        ])

        counts.append(count)

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.bar(
        CLASSES,
        counts
    )

    ax.set_title(
        "Training Dataset Class Distribution"
    )

    ax.set_xlabel(
        "Waste Category"
    )

    ax.set_ylabel(
        "Number of Images"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    for i, count in enumerate(counts):

        ax.text(
            i,
            count + max(counts) * 0.01,
            str(count),
            ha="center",
            fontsize=8
        )

    fig.tight_layout()

    output_file = (
        OUTPUT_DIR /
        "class_distribution.png"
    )

    fig.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight"
    )

    plt.show()

    print(
        f"Saved distribution chart to: {output_file}"
    )


if __name__ == "__main__":

    print("Creating dataset sample grid...")
    create_sample_grid()

    print("Creating class distribution chart...")
    create_class_distribution()

    print("Visualization completed successfully.")