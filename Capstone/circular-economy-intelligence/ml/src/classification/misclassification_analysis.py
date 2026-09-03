from pathlib import Path
from collections import Counter, defaultdict
import csv

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models

from ml.src.data.transforms import get_validation_transforms

from ml.src.classification.config import (
    TEST_DIR,
    MODEL_DIR,
    OUTPUT_DIR,
    BATCH_SIZE,
    NUM_WORKERS,
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = (
    MODEL_DIR / "best_finetuned_model.pt"
)

OUTPUT_DIR = (
    OUTPUT_DIR / "misclassified"
)

MAX_IMAGES_PER_PAIR = 25


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

    print("\nLoading fine-tuned EfficientNet-B0...")

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

    print("✓ Fine-tuned model loaded.")

    return model


# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():

    print("=" * 60)

    print(
        "CIRCULAR ECONOMY INTELLIGENCE"
    )

    print(
        "MISCLASSIFICATION ANALYSIS"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # CHECK FILES
    # --------------------------------------------------------

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model not found:\n{MODEL_PATH}"
        )

    if not TEST_DIR.exists():

        raise FileNotFoundError(
            f"Test directory not found:\n{TEST_DIR}"
        )

    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    device = get_device()

    print(
        f"\nDevice: {device}"
    )

    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

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
        f"\nTest images: "
        f"{len(test_dataset)}"
    )

    print(
        f"Classes: "
        f"{len(class_names)}"
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = load_model(
        class_names,
        device
    )

    # --------------------------------------------------------
    # OUTPUT DIRECTORIES
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    all_errors = []

    pair_counter = Counter()

    actual_counter = Counter()

    # --------------------------------------------------------
    # INFERENCE
    # --------------------------------------------------------

    print(
        "\nAnalyzing test images..."
    )

    image_index = 0

    with torch.no_grad():

        for batch_index, (
            images,
            labels
        ) in enumerate(
            test_loader,
            start=1
        ):

            images = images.to(device)

            outputs = model(images)

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            confidences, predictions = (
                probabilities.max(dim=1)
            )

            for i in range(
                len(labels)
            ):

                actual_index = (
                    labels[i].item()
                )

                predicted_index = (
                    predictions[i].item()
                )

                confidence = (
                    confidences[i].item()
                )

                image_path = (
                    test_dataset.samples[
                        image_index
                    ][0]
                )

                image_index += 1

                if (
                    actual_index
                    != predicted_index
                ):

                    actual_class = (
                        class_names[
                            actual_index
                        ]
                    )

                    predicted_class = (
                        class_names[
                            predicted_index
                        ]
                    )

                    pair = (
                        actual_class,
                        predicted_class
                    )

                    pair_counter[pair] += 1

                    actual_counter[
                        actual_class
                    ] += 1

                    all_errors.append({

                        "image":
                            image_path,

                        "actual":
                            actual_class,

                        "predicted":
                            predicted_class,

                        "confidence":
                            confidence

                    })

            if (
                batch_index % 20 == 0
                or batch_index == len(test_loader)
            ):

                print(
                    f"Batch "
                    f"{batch_index}/"
                    f"{len(test_loader)}"
                )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    total_errors = len(
        all_errors
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "MISCLASSIFICATION SUMMARY"
    )

    print(
        "=" * 60
    )

    print(
        f"Total incorrect predictions: "
        f"{total_errors}"
    )

    # --------------------------------------------------------
    # TOP CONFUSION PAIRS
    # --------------------------------------------------------

    print(
        "\nTop confusion pairs:"
    )

    for (
        actual,
        predicted
    ), count in pair_counter.most_common():

        print(
            f"{actual:15} -> "
            f"{predicted:15} : "
            f"{count}"
        )

    # --------------------------------------------------------
    # SAVE CSV
    # --------------------------------------------------------

    csv_path = (
        OUTPUT_DIR /
        "misclassified_images.csv"
    )

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "image",
                "actual",
                "predicted",
                "confidence"
            ]
        )

        writer.writeheader()

        writer.writerows(
            all_errors
        )

    print(
        f"\nCSV saved to:"
        f"\n{csv_path}"
    )

    # --------------------------------------------------------
    # COPY REPRESENTATIVE ERRORS
    # --------------------------------------------------------

    print(
        "\nCreating representative "
        "misclassification folders..."
    )

    pair_counts = defaultdict(int)

    for error in all_errors:

        actual = error["actual"]

        predicted = error["predicted"]

        pair = (
            actual,
            predicted
        )

        # Limit copied images.
        if (
            pair_counts[pair]
            >= MAX_IMAGES_PER_PAIR
        ):

            continue

        pair_counts[pair] += 1

        folder_name = (
            f"{actual}_as_{predicted}"
        )

        pair_directory = (
            OUTPUT_DIR /
            folder_name
        )

        pair_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        source = Path(
            error["image"]
        )

        destination = (
            pair_directory /
            source.name
        )

        # Avoid overwriting.
        if destination.exists():

            destination = (
                pair_directory /
                f"{pair_counts[pair]}_"
                f"{source.name}"
            )

        import shutil

        shutil.copy2(
            source,
            destination
        )

    # --------------------------------------------------------
    # SAVE CONFUSION SUMMARY
    # --------------------------------------------------------

    summary_path = (
        OUTPUT_DIR /
        "confusion_pairs.csv"
    )

    with open(
        summary_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "actual_class",
            "predicted_class",
            "count"
        ])

        for (
            actual,
            predicted
        ), count in pair_counter.most_common():

            writer.writerow([
                actual,
                predicted,
                count
            ])

    print(
        f"\nConfusion summary saved to:"
        f"\n{summary_path}"
    )

    print(
        "\nRepresentative images saved to:"
        f"\n{OUTPUT_DIR}"
    )

    print(
        "\nAnalysis completed successfully."
    )


if __name__ == "__main__":

    main()