from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.valuation_service import (
    estimate_value,
    get_valuation_metrics,
)

router = APIRouter()

class ValuationRequest(BaseModel):
    material: str
    weight_kg: float = Field(gt=0)
    quality_factor: float = Field(default=1.0, ge=0.0, le=1.2)

@router.post("/estimate")
def valuation(payload: ValuationRequest):
    return estimate_value(payload.material, payload.weight_kg, payload.quality_factor)

@router.get("/metrics")
def valuation_metrics():
    return get_valuation_metrics()