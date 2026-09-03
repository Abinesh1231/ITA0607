from pydantic import BaseModel

class ValuationResult(BaseModel):
    material: str
    weight_kg: float
    rate_per_kg: float
    quality_factor: float
    estimated_value: float
    currency: str
