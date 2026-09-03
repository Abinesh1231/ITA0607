from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.image_service import save_upload
from backend.app.services.classification_service import classify_image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Please upload an image")
    path = await save_upload(file)
    return classify_image(path)
