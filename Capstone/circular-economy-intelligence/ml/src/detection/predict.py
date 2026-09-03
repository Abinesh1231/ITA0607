from pathlib import Path

def predict(image_path, model_path="ml/models/detection/best_model.pt"):
    if not Path(model_path).exists():
        return {"detections": [], "model_status": "unavailable"}
    from ultralytics import YOLO
    model = YOLO(model_path)
    results = model(image_path, verbose=False)
    output = []
    for r in results:
        for b in r.boxes:
            output.append({
                "class_id": int(b.cls[0]),
                "confidence": float(b.conf[0]),
                "bbox": [float(v) for v in b.xyxy[0].tolist()]
            })
    return {"detections": output, "model_status": "ready"}
