import json
import time
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models

from ml.src.data.transforms import (
    get_train_transforms,
    get_validation_transforms
)

from ml.src.classification.config import (
    TRAIN_DIR,
    VAL_DIR,
    MODEL_DIR,
    OUTPUT_DIR,
    IMAGE_SIZE,
    BATCH_SIZE,
    NUM_WORKERS,
    TORCH_THREADS,
)


# ============================================================
# SETTINGS
# ============================================================

BASE_MODEL_PATH = (
    MODEL_DIR / "best_finetuned_model.pt"
)

FINE_TUNED_MODEL_PATH = (
    MODEL_DIR / "best_finetuned_model.pt"
)

FINE_TUNED_HISTORY_PATH = (
    OUTPUT_DIR /
    "metrics" /
    "fine_tuning_history.json"
)

FINE_TUNE_EPOCHS = 3

FINE_TUNE_LR = 1e-5

WEIGHT_DECAY = 1e-4


# ============================================================
# DEVICE
# ============================================================

def get_device():

    if torch.cuda.is_available():

        print("CUDA available.")

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

        return torch.device("cuda")

    print("CUDA unavailable.")

    print("Fine-tuning will use CPU.")

    return torch.device("cpu")


# ============================================================
# DATA
# ============================================================

def create_datasets():

    train_dataset = datasets.ImageFolder(
        TRAIN_DIR,
        transform=get_train_transforms()
    )

    validation_dataset = datasets.ImageFolder(
        VAL_DIR,
        transform=get_validation_transforms()
    )

    return (
        train_dataset,
        validation_dataset
    )


def create_dataloaders(
    train_dataset,
    validation_dataset
):

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS
    )

    return (
        train_loader,
        validation_loader
    )


# ============================================================
# MODEL
# ============================================================

def create_model(
    class_names,
    device
):

    print(
        "\nLoading EfficientNet-B0..."
    )

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
        BASE_MODEL_PATH,
        map_location=device
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    # --------------------------------------------------------
    # FREEZE EVERYTHING
    # --------------------------------------------------------

    for parameter in model.parameters():

        parameter.requires_grad = False

    # --------------------------------------------------------
    # UNFREEZE LAST TWO FEATURE BLOCKS
    # --------------------------------------------------------

    for parameter in model.features[-2:].parameters():

        parameter.requires_grad = True

    # --------------------------------------------------------
    # UNFREEZE CLASSIFIER
    # --------------------------------------------------------

    for parameter in model.classifier.parameters():

        parameter.requires_grad = True

    model = model.to(device)

    trainable = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )

    total = sum(
        parameter.numel()
        for parameter in model.parameters()
    )

    print(
        "\nFine-tuning configuration:"
    )

    print(
        "Early EfficientNet layers: FROZEN"
    )

    print(
        "Last two EfficientNet blocks: TRAINABLE"
    )

    print(
        "Classifier: TRAINABLE"
    )

    print(
        f"Trainable parameters: "
        f"{trainable:,}"
    )

    print(
        f"Total parameters: "
        f"{total:,}"
    )

    return model


# ============================================================
# TRAIN ONE EPOCH
# ============================================================

def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    device,
    epoch
):

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0

    start_time = time.time()

    total_batches = len(loader)

    for batch_index, (
        images,
        labels
    ) in enumerate(
        loader,
        start=1
    ):

        images = images.to(device)

        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item()
            * images.size(0)
        )

        predictions = outputs.argmax(
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

        if (
            batch_index == 1
            or batch_index % 20 == 0
            or batch_index == total_batches
        ):

            elapsed = (
                time.time()
                - start_time
            )

            print(
                f"\rEpoch {epoch}/{FINE_TUNE_EPOCHS} "
                f"| Batch {batch_index}/{total_batches} "
                f"| Loss {loss.item():.4f} "
                f"| Time {elapsed:.1f}s",
                end="",
                flush=True
            )

    print()

    return (
        running_loss / total,
        correct / total
    )


# ============================================================
# VALIDATION
# ============================================================

def validate(
    model,
    loader,
    criterion,
    device
):

    model.eval()

    running_loss = 0.0

    correct = 0

    total = 0

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(device)

            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            running_loss += (
                loss.item()
                * images.size(0)
            )

            predictions = outputs.argmax(
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    return (
        running_loss / total,
        correct / total
    )


# ============================================================
# MAIN
# ============================================================

def main():

    torch.set_num_threads(
        TORCH_THREADS
    )

    device = get_device()

    print("=" * 60)

    print(
        "CIRCULAR ECONOMY INTELLIGENCE"
    )

    print(
        "EFFICIENTNET-B0 FINE-TUNING"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # CHECK BASE MODEL
    # --------------------------------------------------------

    if not BASE_MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Base model not found:\n"
            f"{BASE_MODEL_PATH}"
        )

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    print(
        "\nLoading datasets..."
    )

    (
        train_dataset,
        validation_dataset
    ) = create_datasets()

    print(
        f"Training images: "
        f"{len(train_dataset)}"
    )

    print(
        f"Validation images: "
        f"{len(validation_dataset)}"
    )

    print(
        f"Classes: "
        f"{len(train_dataset.classes)}"
    )

    # --------------------------------------------------------
    # LOADERS
    # --------------------------------------------------------

    (
        train_loader,
        validation_loader
    ) = create_dataloaders(
        train_dataset,
        validation_dataset
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = create_model(
        train_dataset.classes,
        device
    )

    # --------------------------------------------------------
    # LOSS
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    # --------------------------------------------------------
    # OPTIMIZER
    # --------------------------------------------------------

    trainable_parameters = [
        parameter
        for parameter in model.parameters()
        if parameter.requires_grad
    ]

    optimizer = torch.optim.AdamW(
        trainable_parameters,
        lr=FINE_TUNE_LR,
        weight_decay=WEIGHT_DECAY
    )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    (
        OUTPUT_DIR / "metrics"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    best_accuracy = 0.0

    history = []

    for epoch in range(
        1,
        FINE_TUNE_EPOCHS + 1
    ):

        print(
            "\n" + "=" * 60
        )

        print(
            f"Fine-tuning Epoch "
            f"{epoch}/{FINE_TUNE_EPOCHS}"
        )

        print(
            "=" * 60
        )

        train_loss, train_accuracy = (
            train_one_epoch(
                model,
                train_loader,
                criterion,
                optimizer,
                device,
                epoch
            )
        )

        validation_loss, validation_accuracy = (
            validate(
                model,
                validation_loader,
                criterion,
                device
            )
        )

        print(
            f"\nTrain Loss: "
            f"{train_loss:.4f}"
        )

        print(
            f"Train Accuracy: "
            f"{train_accuracy:.4f}"
        )

        print(
            f"Validation Loss: "
            f"{validation_loss:.4f}"
        )

        print(
            f"Validation Accuracy: "
            f"{validation_accuracy:.4f}"
        )

        history.append({

            "epoch": epoch,

            "train_loss": train_loss,

            "train_accuracy":
                train_accuracy,

            "validation_loss":
                validation_loss,

            "validation_accuracy":
                validation_accuracy

        })

        # ----------------------------------------------------
        # SAVE BEST
        # ----------------------------------------------------

        if validation_accuracy > best_accuracy:

            best_accuracy = validation_accuracy

            checkpoint = {

                "model_state_dict":
                    model.state_dict(),

                "class_names":
                    train_dataset.classes,

                "image_size":
                    IMAGE_SIZE,

                "validation_accuracy":
                    best_accuracy,

                "epoch":
                    epoch,

                "fine_tuned":
                    True

            }

            torch.save(
                checkpoint,
                FINE_TUNED_MODEL_PATH
            )

            print(
                "\n✓ New best fine-tuned model saved."
            )

            print(
                f"✓ Validation accuracy: "
                f"{best_accuracy:.4f}"
            )

    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    FINE_TUNED_HISTORY_PATH.write_text(
        json.dumps(
            history,
            indent=2
        ),
        encoding="utf-8"
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "FINE-TUNING COMPLETE"
    )

    print(
        "=" * 60
    )

    print(
        f"Best validation accuracy: "
        f"{best_accuracy:.4f}"
    )

    print(
        f"Fine-tuned model:"
        f"\n{FINE_TUNED_MODEL_PATH}"
    )


if __name__ == "__main__":

    main()