import torch

from torchvision import transforms


IMAGE_SIZE = 224

# ImageNet statistics.
# We use these because EfficientNet-B0 is pretrained on ImageNet.
IMAGENET_MEAN = [
    0.485,
    0.456,
    0.406
]

IMAGENET_STD = [
    0.229,
    0.224,
    0.225
]


def get_train_transforms():

    return transforms.Compose([

        # Resize the shortest side first.
        transforms.Resize(
            256
        ),

        # Random crop prevents the model from
        # depending too much on image position.
        transforms.RandomResizedCrop(
            IMAGE_SIZE,
            scale=(0.80, 1.0),
            ratio=(0.9, 1.1)
        ),

        # Horizontal flipping is useful for
        # most waste categories.
        transforms.RandomHorizontalFlip(
            p=0.5
        ),

        # Small rotations make the model
        # more robust to differently oriented objects.
        transforms.RandomRotation(
            degrees=15
        ),

        # Slight color changes improve robustness
        # to different lighting conditions.
        transforms.ColorJitter(
            brightness=0.20,
            contrast=0.20,
            saturation=0.20,
            hue=0.05
        ),

        # Convert PIL image to PyTorch tensor.
        transforms.ToTensor(),

        # Normalize using ImageNet statistics.
        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD
        ),
    ])


def get_validation_transforms():

    return transforms.Compose([

        transforms.Resize(
            256
        ),

        transforms.CenterCrop(
            IMAGE_SIZE
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD
        ),
    ])


def get_test_transforms():

    return transforms.Compose([

        transforms.Resize(
            256
        ),

        transforms.CenterCrop(
            IMAGE_SIZE
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=IMAGENET_MEAN,
            std=IMAGENET_STD
        ),
    ])


if __name__ == "__main__":

    print("Testing image transformations...")

    train_transform = get_train_transforms()
    val_transform = get_validation_transforms()

    print("\nTraining transformations:")
    print(train_transform)

    print("\nValidation transformations:")
    print(val_transform)

    print("\nImage size:", IMAGE_SIZE)

    print("\nTransform configuration is valid.")