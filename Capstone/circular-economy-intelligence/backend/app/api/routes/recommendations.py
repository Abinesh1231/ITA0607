from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.recommendation_service import recommendation_for

router = APIRouter()

class RecommendationRequest(BaseModel):
    material: str

@router.post("")
def recommendation(payload: RecommendationRequest):
    return recommendation_for(payload.material)
