from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from backend.app.core.config import settings

UPLOAD_DIR = Path("backend/uploads")
PROCESSED_DIR = UPLOAD_DIR / "processed"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

async def save_upload(file: UploadFile) -> str:
    suffix = Path(file.filename or ".jpg").suffix.lower() or ".jpg"
    destination = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    data = await file.read()
    destination.write_bytes(data)
    return str(destination)
