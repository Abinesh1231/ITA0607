from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.services.dashboard_service import get_dashboard_data


router = APIRouter()


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    return get_dashboard_data(db)