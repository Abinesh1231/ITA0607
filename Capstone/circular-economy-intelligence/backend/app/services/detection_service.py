from pathlib import Path

from backend.app.core.config import settings


def detect_objects(image_path: str):
    model_path = Path(settings.DETECTOR_MODEL_PATH)

    if not model_path.exists():
        return {
            "detections": [],
            "model_status": "unavailable",
            "message": "No trained detector found.",
        }

    try:
        from ultralytics import YOLO

        model = YOLO(str(model_path))

        results = model(
            image_path,
            conf=0.10,
            iou=0.45,
            max_det=15,
            verbose=False,
        )

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            names = result.names

            for box in result.boxes:
                confidence = float(box.conf[0].item())

                if confidence < 0.10:
                    continue

                cls_id = int(box.cls[0].item())

                detections.append(
                    {
                        "label": names.get(
                            cls_id,
                            str(cls_id),
                        ),
                        "confidence": round(
                            confidence,
                            4,
                        ),
                        "bbox": [
                            round(float(x), 2)
                            for x in box.xyxy[0].tolist()
                        ],
                    }
                )

        # Highest-confidence detections first
        detections.sort(
            key=lambda x: x["confidence"],
            reverse=True,
        )

        return {
            "detections": detections,
            "count": len(detections),
            "model_status": "ready",
        }

    except Exception as exc:
        return {
            "detections": [],
            "model_status": "error",
            "detail": str(exc),
        }