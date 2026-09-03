from pathlib import Path

from backend.app.ml.inference import (
    classify_image
)


def main():

    test_directory = (
        Path("ml/data/processed/test")
    )

    # Find one plastic image
    images = list(
        (
            test_directory
            / "plastic"
        ).glob("*")
    )

    if not images:

        raise FileNotFoundError(
            "No plastic test images found."
        )

    image_path = images[0]

    print("=" * 60)
    print(
        "BACKEND IMAGE CLASSIFICATION TEST"
    )
    print("=" * 60)

    print(
        f"\nTest image:\n{image_path}"
    )

    image_bytes = (
        image_path.read_bytes()
    )

    result = classify_image(
        image_bytes
    )

    print(
        "\nPrediction:"
    )

    print(
        f"Material: "
        f"{result['material']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence']}"
    )

    print(
        "\nTop predictions:"
    )

    for prediction in (
        result["top_predictions"]
    ):

        print(
            f"  {prediction['material']}: "
            f"{prediction['confidence']}"
        )

    print(
        "\nClassification inference PASSED."
    )


if __name__ == "__main__":

    main()