from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.image_service import save_upload
from backend.app.services.detection_service import detect_objects

router = APIRouter()

@router.post("/analyze")
async def detect(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Please upload an image")
    path = await save_upload(file)
    return detect_objects(path)
