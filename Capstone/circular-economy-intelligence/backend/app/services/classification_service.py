from pathlib import Path

from backend.app.ml.inference import classify_image as run_classification


def classify_image(image_path: str):
    """
    Classify an uploaded waste image.

    Parameters
    ----------
    image_path : str
        Path to the uploaded image.

    Returns
    -------
    dict
        Classification result from EfficientNet-B0.
    """

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image file not found: {path}"
        )

    # Read image as bytes
    image_bytes = path.read_bytes()

    # Run trained EfficientNet-B0
    result = run_classification(
        image_bytes
    )

    # Add useful application-level information
    material = result["material"]

    recyclable_materials = {
        "paper",
        "cardboard",
        "plastic",
        "metal",
        "white-glass",
        "green-glass",
        "brown-glass",
        "battery",
        "clothes",
        "shoes",
    }

    result["recyclable"] = (
        material in recyclable_materials
    )

    return result