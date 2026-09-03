import json
import torch
from PIL import Image
from torchvision import models
from ml.src.data.augment import eval_transforms
from ml.src.classification.config import *

def predict(image_path):
    checkpoint = torch.load(MODEL_DIR / "best_model.pt", map_location="cpu", weights_only=False)
    classes = checkpoint["class_names"]
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(classes))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    image = Image.open(image_path).convert("RGB")
    x = eval_transforms(IMAGE_SIZE)(image).unsqueeze(0)
    with torch.no_grad():
        p = torch.softmax(model(x), 1)[0]
    conf, idx = p.max(0)
    return {"label": classes[int(idx)], "confidence": float(conf)}

if __name__ == "__main__":
    import sys
    print(predict(sys.argv[1]))
