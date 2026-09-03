import io

import torch
from PIL import Image
from torchvision import transforms

from backend.app.ml.model_loader import get_model


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

TRANSFORM = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],
        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ============================================================
# CLASSIFY IMAGE
# ============================================================

def classify_image(
    image_bytes: bytes
):

    loaded = get_model()

    model = loaded[
        "model"
    ]

    class_names = loaded[
        "class_names"
    ]

    device = loaded[
        "device"
    ]

    # --------------------------------------------------------
    # OPEN IMAGE
    # --------------------------------------------------------

    try:

        image = Image.open(
            io.BytesIO(
                image_bytes
            )
        ).convert("RGB")

    except Exception as exc:

        raise ValueError(
            "Unable to read uploaded image."
        ) from exc

    # --------------------------------------------------------
    # PREPROCESS
    # --------------------------------------------------------

    tensor = TRANSFORM(
        image
    )

    tensor = tensor.unsqueeze(
        0
    )

    tensor = tensor.to(
        device
    )

    # --------------------------------------------------------
    # INFERENCE
    # --------------------------------------------------------

    with torch.no_grad():

        outputs = model(
            tensor
        )

        probabilities = (
            torch.softmax(
                outputs,
                dim=1
            )
        )

    # --------------------------------------------------------
    # BEST PREDICTION
    # --------------------------------------------------------

    confidence, index = (
        probabilities[0].max(
            dim=0
        )
    )

    predicted_index = (
        index.item()
    )

    material = class_names[
        predicted_index
    ]

    confidence_value = (
        confidence.item()
    )

    # --------------------------------------------------------
    # TOP 3 PREDICTIONS
    # --------------------------------------------------------

    number_of_predictions = min(
        3,
        len(class_names)
    )

    top_values, top_indices = (
        probabilities[0].topk(
            number_of_predictions
        )
    )

    top_predictions = []

    for probability, class_index in zip(
        top_values,
        top_indices
    ):

        top_predictions.append({
            "material":
                class_names[
                    class_index.item()
                ],

            "confidence":
                round(
                    probability.item(),
                    4
                )
        })

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {
        "material":
            material,

        "confidence":
            round(
                confidence_value,
                4
            ),

        "top_predictions":
            top_predictions
    }