from pathlib import Path

folders = [
    "ml/data/raw", "ml/data/interim", "ml/data/processed",
    "ml/models/classification", "ml/models/detection", "ml/models/valuation",
    "ml/outputs/plots", "ml/outputs/confusion_matrices", "ml/outputs/metrics",
    "ml/outputs/predictions", "backend/uploads/processed"
]
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)
print("Project directories initialized.")
