from pathlib import Path

import torch
from torch import nn
from torchvision import models


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "classification"
    / "best_finetuned_model.pt"
)


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ============================================================
# CACHED MODEL
# ============================================================

_model = None


# ============================================================
# LOAD MODEL
# ============================================================

def get_model():

    global _model

    # Return cached model
    if _model is not None:
        return _model

    # Check model file
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Classification model not found:\n"
            f"{MODEL_PATH}"
        )

    print(
        f"Loading classification model:\n"
        f"{MODEL_PATH}"
    )

    # --------------------------------------------------------
    # LOAD CHECKPOINT
    # --------------------------------------------------------

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=False
    )

    # --------------------------------------------------------
    # VALIDATE CHECKPOINT
    # --------------------------------------------------------

    required_keys = {
        "model_state_dict",
        "class_names"
    }

    missing_keys = (
        required_keys
        - set(checkpoint.keys())
    )

    if missing_keys:
        raise ValueError(
            "Invalid model checkpoint. "
            f"Missing keys: {missing_keys}"
        )

    class_names = checkpoint[
        "class_names"
    ]

    image_size = checkpoint.get(
        "image_size",
        224
    )

    # --------------------------------------------------------
    # CREATE EFFICIENTNET-B0
    # --------------------------------------------------------

    model = models.efficientnet_b0(
        weights=None
    )

    # --------------------------------------------------------
    # RECREATE CLASSIFIER
    # --------------------------------------------------------

    input_features = (
        model.classifier[1].in_features
    )

    model.classifier[1] = nn.Linear(
        input_features,
        len(class_names)
    )

    # --------------------------------------------------------
    # LOAD TRAINED WEIGHTS
    # --------------------------------------------------------

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    model = model.to(
        DEVICE
    )

    model.eval()

    # --------------------------------------------------------
    # CACHE
    # --------------------------------------------------------

    _model = {
        "model": model,
        "class_names": class_names,
        "image_size": image_size,
        "device": DEVICE,
        "validation_accuracy":
            checkpoint.get(
                "validation_accuracy"
            ),
        "epoch":
            checkpoint.get(
                "epoch"
            ),
        "fine_tuned":
            checkpoint.get(
                "fine_tuned",
                False
            )
    }

    print(
        "Classification model loaded successfully."
    )

    return _model