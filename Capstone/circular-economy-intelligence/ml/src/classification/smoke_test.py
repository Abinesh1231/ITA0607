import time

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models

from ml.src.data.transforms import get_train_transforms
from ml.src.classification.config import (
    TRAIN_DIR,
    BATCH_SIZE,
    NUM_WORKERS,
)


def main():

    print("=" * 60)
    print("EFFICIENTNET-B0 TRAINING SMOKE TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # CPU CONFIGURATION
    # --------------------------------------------------------

    torch.set_num_threads(6)

    device = torch.device("cpu")

    print(
        f"\nDevice: {device}"
    )

    print(
        f"PyTorch threads: "
        f"{torch.get_num_threads()}"
    )

    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    dataset = datasets.ImageFolder(
        TRAIN_DIR,
        transform=get_train_transforms()
    )

    # Only load a small portion for testing.
    subset_size = min(
        128,
        len(dataset)
    )

    subset = torch.utils.data.Subset(
        dataset,
        range(subset_size)
    )

    loader = DataLoader(
        subset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS
    )

    print(
        f"Smoke-test images: "
        f"{subset_size}"
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    print(
        "\nLoading EfficientNet-B0..."
    )

    model = models.efficientnet_b0(
        weights=models.EfficientNet_B0_Weights.DEFAULT
    )

    input_features = (
        model.classifier[1].in_features
    )

    model.classifier[1] = nn.Linear(
        input_features,
        12
    )

    model = model.to(device)

    # --------------------------------------------------------
    # LOSS + OPTIMIZER
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=1e-4
    )

    # --------------------------------------------------------
    # TEST BATCHES
    # --------------------------------------------------------

    model.train()

    start_time = time.time()

    batches_completed = 0

    for images, labels in loader:

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

        batches_completed += 1

        print(
            f"Batch {batches_completed}: "
            f"loss={loss.item():.4f}"
        )

        # Four batches are enough.
        if batches_completed >= 4:
            break

    elapsed = time.time() - start_time

    print("\n" + "=" * 60)

    print("SMOKE TEST COMPLETE")

    print("=" * 60)

    print(
        f"Batches completed: "
        f"{batches_completed}"
    )

    print(
        f"Time: "
        f"{elapsed:.2f} seconds"
    )

    print(
        f"Average time/batch: "
        f"{elapsed / batches_completed:.2f} seconds"
    )

    print(
        "\nEfficientNet-B0 forward + backward pass works."
    )


if __name__ == "__main__":
    main()