from typing import List

from pydantic import BaseModel


class TopPrediction(BaseModel):
    material: str
    confidence: float


class WastePrediction(BaseModel):
    material: str
    confidence: float
    top_predictions: List[TopPrediction]
    recyclable: bool


class WasteAnalysisResult(BaseModel):
    filename: str
    image_path: str

    material: str
    confidence: float
    top_predictions: List[TopPrediction]
    recyclable: bool

    weight_kg: float

    rate_per_kg: float
    quality_factor: float
    estimated_value: float
    currency: str

    recommendation: str
    recommendation_detail: str

    status: str