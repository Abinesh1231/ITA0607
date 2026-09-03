from pathlib import Path
import random
import shutil


# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_DIR = Path(
    "ml/data/processed/train"
)

OUTPUT_DIR = Path(
    "ml/data/balanced/train"
)

MAX_IMAGES_PER_CLASS = 1000

SEED = 42

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
}


# ============================================================
# MAIN
# ============================================================

def main():

    random.seed(SEED)

    if not SOURCE_DIR.exists():

        raise FileNotFoundError(
            f"Training directory not found: "
            f"{SOURCE_DIR}"
        )

    # Create output directory.
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 60)
    print("BALANCING TRAINING DATASET")
    print("=" * 60)

    print(
        f"\nMaximum images per class: "
        f"{MAX_IMAGES_PER_CLASS}"
    )

    print(
        f"Source: {SOURCE_DIR}"
    )

    print(
        f"Output: {OUTPUT_DIR}"
    )

    print()

    total_original = 0
    total_balanced = 0

    # --------------------------------------------------------
    # PROCESS EACH CLASS
    # --------------------------------------------------------

    class_directories = sorted(
        [
            directory
            for directory in SOURCE_DIR.iterdir()
            if directory.is_dir()
        ]
    )

    for class_directory in class_directories:

        class_name = class_directory.name

        images = [
            image
            for image in class_directory.iterdir()
            if (
                image.is_file()
                and image.suffix.lower()
                in IMAGE_EXTENSIONS
            )
        ]

        original_count = len(images)

        total_original += original_count

        # Randomize the images.
        random.shuffle(images)

        # Keep at most MAX_IMAGES_PER_CLASS.
        selected_images = images[
            :MAX_IMAGES_PER_CLASS
        ]

        output_class_directory = (
            OUTPUT_DIR / class_name
        )

        output_class_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # Copy selected images.
        for image in selected_images:

            destination = (
                output_class_directory /
                image.name
            )

            shutil.copy2(
                image,
                destination
            )

        balanced_count = len(
            selected_images
        )

        total_balanced += balanced_count

        if original_count > MAX_IMAGES_PER_CLASS:

            status = "DOWNSAMPLED"

        else:

            status = "KEPT ALL"

        print(
            f"{class_name:15} "
            f"{original_count:5} -> "
            f"{balanced_count:5} "
            f"{status}"
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print("BALANCING COMPLETE")

    print("=" * 60)

    print(
        f"Original training images: "
        f"{total_original}"
    )

    print(
        f"Balanced training images: "
        f"{total_balanced}"
    )

    print(
        f"Images removed from training: "
        f"{total_original - total_balanced}"
    )

    print(
        f"\nBalanced dataset:"
        f"\n{OUTPUT_DIR}"
    )


if __name__ == "__main__":

    main()