from pathlib import Path

from PIL import Image

from ml.src.data.transforms import (
    get_train_transforms,
    get_validation_transforms
)


DATASET_DIR = Path(
    "ml/data/processed/train"
)


def find_first_image():

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp"
    }

    for class_dir in DATASET_DIR.iterdir():

        if not class_dir.is_dir():
            continue

        for image_path in class_dir.iterdir():

            if image_path.suffix.lower() in extensions:

                return image_path

    return None


def main():

    image_path = find_first_image()

    if image_path is None:

        raise FileNotFoundError(
            "No image found in the training dataset."
        )

    print(
        f"Testing image: {image_path}"
    )

    image = Image.open(
        image_path
    ).convert("RGB")

    print(
        "Original image size:",
        image.size
    )

    train_transform = (
        get_train_transforms()
    )

    val_transform = (
        get_validation_transforms()
    )

    train_tensor = train_transform(
        image
    )

    val_tensor = val_transform(
        image
    )

    print(
        "Training tensor shape:",
        train_tensor.shape
    )

    print(
        "Validation tensor shape:",
        val_tensor.shape
    )

    print(
        "Training tensor dtype:",
        train_tensor.dtype
    )

    print(
        "Validation tensor dtype:",
        val_tensor.dtype
    )

    expected_shape = (
        3,
        224,
        224
    )

    assert train_tensor.shape == expected_shape
    assert val_tensor.shape == expected_shape

    print(
        "\nPreprocessing test PASSED."
    )


if __name__ == "__main__":

    main()