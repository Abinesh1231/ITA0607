from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, models
from torch import nn

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

from ml.src.data.transforms import get_validation_transforms

from ml.src.classification.config import (
    TEST_DIR,
    MODEL_DIR,
    OUTPUT_DIR,
    BATCH_SIZE,
    NUM_WORKERS,
    IMAGE_SIZE,
)


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = MODEL_DIR / "best_finetuned_model.pt"

OUTPUT_METRICS_DIR = (
    OUTPUT_DIR / "metrics"
)

OUTPUT_PLOTS_DIR = (
    OUTPUT_DIR / "confusion_matrices"
)


# ============================================================
# DEVICE
# ============================================================

def get_device():

    if torch.cuda.is_available():

        return torch.device("cuda")

    return torch.device("cpu")


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(
    class_names,
    device
):

    print("\nLoading trained EfficientNet-B0...")

    model = models.efficientnet_b0(
        weights=None
    )

    input_features = (
        model.classifier[1].in_features
    )

    model.classifier[1] = nn.Linear(
        input_features,
        len(class_names)
    )

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(device)

    model.eval()

    print("✓ Model loaded successfully.")

    return model


# ============================================================
# EVALUATE
# ============================================================

def evaluate_model(
    model,
    loader,
    device
):

    all_predictions = []

    all_labels = []

    print("\nRunning test-set inference...")

    with torch.no_grad():

        for batch_index, (
            images,
            labels
        ) in enumerate(loader, start=1):

            images = images.to(device)

            outputs = model(images)

            predictions = outputs.argmax(
                dim=1
            )

            all_predictions.extend(
                predictions.cpu().numpy()
            )

            all_labels.extend(
                labels.numpy()
            )

            if (
                batch_index % 20 == 0
                or batch_index == len(loader)
            ):

                print(
                    f"Batch "
                    f"{batch_index}/"
                    f"{len(loader)}"
                )

    return (
        np.array(all_labels),
        np.array(all_predictions)
    )


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

def create_report(
    labels,
    predictions,
    class_names
):

    accuracy = accuracy_score(
        labels,
        predictions
    )

    precision = precision_score(
        labels,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        labels,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        labels,
        predictions,
        average="weighted",
        zero_division=0
    )

    report = classification_report(
        labels,
        predictions,
        target_names=class_names,
        zero_division=0,
        output_dict=True
    )

    metrics = {

        "accuracy": float(accuracy),

        "weighted_precision":
            float(precision),

        "weighted_recall":
            float(recall),

        "weighted_f1":
            float(f1),

        "classification_report":
            report
    }

    return metrics


# ============================================================
# CONFUSION MATRIX
# ============================================================

def create_confusion_matrix(
    labels,
    predictions,
    class_names
):

    matrix = confusion_matrix(
        labels,
        predictions
    )

    print("\nConfusion Matrix:")
    print(matrix)

    OUTPUT_PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    figure, axis = plt.subplots(
        figsize=(12, 10)
    )

    image = axis.imshow(
        matrix
    )

    axis.set_title(
        "Waste Classification Confusion Matrix"
    )

    axis.set_xlabel(
        "Predicted Class"
    )

    axis.set_ylabel(
        "Actual Class"
    )

    axis.set_xticks(
        range(len(class_names))
    )

    axis.set_yticks(
        range(len(class_names))
    )

    axis.set_xticklabels(
        class_names,
        rotation=45,
        ha="right"
    )

    axis.set_yticklabels(
        class_names
    )

    # Add numbers to each cell.
    for row in range(
        matrix.shape[0]
    ):

        for col in range(
            matrix.shape[1]
        ):

            axis.text(
                col,
                row,
                str(matrix[row, col]),
                ha="center",
                va="center"
            )

    figure.colorbar(
        image,
        ax=axis
    )

    figure.tight_layout()

    output_path = (
        OUTPUT_PLOTS_DIR /
        "confusion_matrix.png"
    )

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(figure)

    print(
        f"\nConfusion matrix saved to:"
        f"\n{output_path}"
    )

    return matrix


# ============================================================
# SAVE METRICS
# ============================================================

def save_metrics(metrics):

    OUTPUT_METRICS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        OUTPUT_METRICS_DIR /
        "test_metrics.json"
    )

    output_path.write_text(
        json.dumps(
            metrics,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        f"Metrics saved to:"
        f"\n{output_path}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)

    print(
        "CIRCULAR ECONOMY INTELLIGENCE"
    )

    print(
        "TEST SET EVALUATION"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Trained model not found:"
            f"\n{MODEL_PATH}"
        )

    if not TEST_DIR.exists():

        raise FileNotFoundError(
            f"Test dataset not found:"
            f"\n{TEST_DIR}"
        )

    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    device = get_device()

    print(
        f"\nDevice: {device}"
    )

    # --------------------------------------------------------
    # TEST DATASET
    # --------------------------------------------------------

    print(
        "\nLoading untouched test dataset..."
    )

    test_dataset = datasets.ImageFolder(
        TEST_DIR,
        transform=get_validation_transforms()
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS
    )

    class_names = test_dataset.classes

    print(
        f"Test images: "
        f"{len(test_dataset)}"
    )

    print(
        f"Classes: "
        f"{len(class_names)}"
    )

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    model = load_model(
        class_names,
        device
    )

    # --------------------------------------------------------
    # INFERENCE
    # --------------------------------------------------------

    labels, predictions = evaluate_model(
        model,
        test_loader,
        device
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    metrics = create_report(
        labels,
        predictions,
        class_names
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "TEST RESULTS"
    )

    print(
        "=" * 60
    )

    print(
        f"Accuracy: "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"Weighted Precision: "
        f"{metrics['weighted_precision']:.4f}"
    )

    print(
        f"Weighted Recall: "
        f"{metrics['weighted_recall']:.4f}"
    )

    print(
        f"Weighted F1: "
        f"{metrics['weighted_f1']:.4f}"
    )

    # --------------------------------------------------------
    # PER-CLASS RESULTS
    # --------------------------------------------------------

    print(
        "\nPer-class performance:"
    )

    report = metrics[
        "classification_report"
    ]

    for class_name in class_names:

        class_metrics = report[
            class_name
        ]

        print(
            f"\n{class_name}"
        )

        print(
            f"  Precision: "
            f"{class_metrics['precision']:.4f}"
        )

        print(
            f"  Recall: "
            f"{class_metrics['recall']:.4f}"
        )

        print(
            f"  F1: "
            f"{class_metrics['f1-score']:.4f}"
        )

        print(
            f"  Images: "
            f"{int(class_metrics['support'])}"
        )

    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    create_confusion_matrix(
        labels,
        predictions,
        class_names
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    save_metrics(
        metrics
    )

    print(
        "\nEvaluation completed successfully."
    )


if __name__ == "__main__":

    main()