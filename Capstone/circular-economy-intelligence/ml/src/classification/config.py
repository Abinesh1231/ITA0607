from pathlib import Path


# ============================================================
# DATA PATHS
# ============================================================

# Balanced dataset is used ONLY for training.
TRAIN_DIR = Path(
    "ml/data/balanced/train"
)

# Original validation set remains untouched.
VAL_DIR = Path(
    "ml/data/processed/val"
)

# Original test set remains untouched.
TEST_DIR = Path(
    "ml/data/processed/test"
)


# ============================================================
# OUTPUT PATHS
# ============================================================

MODEL_DIR = Path(
    "ml/models/classification"
)

OUTPUT_DIR = Path(
    "ml/outputs"
)


# ============================================================
# IMAGE SETTINGS
# ============================================================

IMAGE_SIZE = 224


# ============================================================
# TRAINING SETTINGS
# ============================================================

BATCH_SIZE = 16

EPOCHS = 5

LEARNING_RATE = 1e-4

WEIGHT_DECAY = 1e-4

SEED = 42


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "efficientnet_b0"

NUM_CLASSES = 12


# ============================================================
# DATA LOADER
# ============================================================

NUM_WORKERS = 0
TORCH_THREADS = 6

# ============================================================
# EARLY STOPPING
# ============================================================

EARLY_STOPPING_PATIENCE = 3