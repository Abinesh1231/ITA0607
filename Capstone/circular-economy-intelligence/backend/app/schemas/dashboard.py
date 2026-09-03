from pydantic import BaseModel

class DashboardStats(BaseModel):
    total_analyses: int
    recyclable_analyses: int
    estimated_value: float
