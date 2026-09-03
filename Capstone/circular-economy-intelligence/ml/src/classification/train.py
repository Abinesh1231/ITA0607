from pathlib import Path
import json
import random
import time

import numpy as np
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
    EPOCHS,
    LEARNING_RATE,
    WEIGHT_DECAY,
    SEED,
    NUM_WORKERS,
    TORCH_THREADS,
    EARLY_STOPPING_PATIENCE
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

def seed_everything(seed=SEED):

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


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
    print("Training will use CPU.")

    return torch.device("cpu")


# ============================================================
# DATASET
# ============================================================

def create_datasets():

    if not TRAIN_DIR.exists():

        raise FileNotFoundError(
            f"Training directory not found: {TRAIN_DIR}"
        )

    if not VAL_DIR.exists():

        raise FileNotFoundError(
            f"Validation directory not found: {VAL_DIR}"
        )

    train_dataset = datasets.ImageFolder(
        TRAIN_DIR,
        transform=get_train_transforms()
    )

    validation_dataset = datasets.ImageFolder(
        VAL_DIR,
        transform=get_validation_transforms()
    )

    return train_dataset, validation_dataset


# ============================================================
# DATA LOADERS
# ============================================================

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

    return train_loader, validation_loader


# ============================================================
# MODEL
# ============================================================

def create_model(number_of_classes):

    print("\nLoading EfficientNet-B0...")

    model = models.efficientnet_b0(
        weights=models.EfficientNet_B0_Weights.DEFAULT
    )

    # --------------------------------------------------------
    # FREEZE PRETRAINED FEATURE EXTRACTOR
    # --------------------------------------------------------

    for parameter in model.features.parameters():

        parameter.requires_grad = False

    # --------------------------------------------------------
    # REPLACE CLASSIFIER
    # --------------------------------------------------------

    input_features = (
        model.classifier[1].in_features
    )

    model.classifier[1] = nn.Linear(
        input_features,
        number_of_classes
    )

    print(
        "EfficientNet feature extractor: FROZEN"
    )

    print(
        "Classification head: TRAINABLE"
    )

    return model


# ============================================================
# TRAIN
# ============================================================

def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    device,
    epoch,
    total_epochs
):

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0

    start_time = time.time()

    total_batches = len(loader)

    for batch_index, (images, labels) in enumerate(
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

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        if (
            batch_index == 1
            or batch_index % 20 == 0
            or batch_index == total_batches
        ):

            elapsed = time.time() - start_time

            print(
                f"\rEpoch {epoch}/{total_epochs} "
                f"| Batch {batch_index}/{total_batches} "
                f"| Loss {loss.item():.4f} "
                f"| Time {elapsed:.1f}s",
                end="",
                flush=True
            )

    print()

    epoch_loss = (
        running_loss /
        max(total, 1)
    )

    epoch_accuracy = (
        correct /
        max(total, 1)
    )

    return epoch_loss, epoch_accuracy


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

    loss = (
        running_loss /
        max(total, 1)
    )

    accuracy = (
        correct /
        max(total, 1)
    )

    return loss, accuracy


# ============================================================
# MAIN
# ============================================================

def main():

    seed_everything()

    torch.set_num_threads(
        TORCH_THREADS
    )

    print(
        f"PyTorch CPU threads: "
        f"{torch.get_num_threads()}"
    )

    print("=" * 60)

    print(
        "CIRCULAR ECONOMY INTELLIGENCE"
    )

    print(
        "Waste Classification Training"
    )

    print("=" * 60)

    device = get_device()

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    print("\nLoading datasets...")

    train_dataset, validation_dataset = (
        create_datasets()
    )

    print(
        f"\nTraining images: "
        f"{len(train_dataset)}"
    )

    print(
        f"Validation images: "
        f"{len(validation_dataset)}"
    )

    print(
        f"Number of classes: "
        f"{len(train_dataset.classes)}"
    )

    print("\nClasses:")

    for index, class_name in enumerate(
        train_dataset.classes
    ):

        print(
            f"{index}: {class_name}"
        )

    # --------------------------------------------------------
    # DATA LOADERS
    # --------------------------------------------------------

    train_loader, validation_loader = (
        create_dataloaders(
            train_dataset,
            validation_dataset
        )
    )

    print(
        f"\nTraining batches per epoch: "
        f"{len(train_loader)}"
    )

    print(
        f"Validation batches: "
        f"{len(validation_loader)}"
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = create_model(
        len(train_dataset.classes)
    )

    model = model.to(device)

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
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    metrics_dir = (
        OUTPUT_DIR / "metrics"
    )

    metrics_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # TRAINING
    # --------------------------------------------------------

    best_accuracy = 0.0

    epochs_without_improvement = 0

    history = []

    for epoch in range(
        1,
        EPOCHS + 1
    ):

        print("\n" + "=" * 60)

        print(
            f"Epoch {epoch}/{EPOCHS}"
        )

        print("=" * 60)

        train_loss, train_accuracy = (
            train_one_epoch(
                model,
                train_loader,
                criterion,
                optimizer,
                device,
                epoch,
                EPOCHS
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

            "train_accuracy": train_accuracy,

            "validation_loss": validation_loss,

            "validation_accuracy":
                validation_accuracy

        })

        # ----------------------------------------------------
        # SAVE BEST MODEL
        # ----------------------------------------------------

        if validation_accuracy > best_accuracy:

            best_accuracy = validation_accuracy

            epochs_without_improvement = 0

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
                    epoch

            }

            model_path = (
                MODEL_DIR /
                "best_model.pt"
            )

            torch.save(
                checkpoint,
                model_path
            )

            class_names_path = (
                MODEL_DIR /
                "class_names.json"
            )

            class_names_path.write_text(
                json.dumps(
                    train_dataset.classes,
                    indent=2
                ),
                encoding="utf-8"
            )

            print(
                "\n✓ Best model saved."
            )

            print(
                f"✓ Best validation accuracy: "
                f"{best_accuracy:.4f}"
            )

        else:

            epochs_without_improvement += 1

            print(
                "\nNo validation improvement."
            )

        # ----------------------------------------------------
        # EARLY STOPPING
        # ----------------------------------------------------

        if (
            epochs_without_improvement
            >= EARLY_STOPPING_PATIENCE
        ):

            print(
                "\nEarly stopping triggered."
            )

            break

    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    history_path = (
        metrics_dir /
        "training_history.json"
    )

    history_path.write_text(
        json.dumps(
            history,
            indent=2
        ),
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print("TRAINING COMPLETE")

    print("=" * 60)

    print(
        f"Best validation accuracy: "
        f"{best_accuracy:.4f}"
    )

    print(
        f"Model: "
        f"{MODEL_DIR / 'best_model.pt'}"
    )

    print(
        f"History: "
        f"{history_path}"
    )


if __name__ == "__main__":

    main()