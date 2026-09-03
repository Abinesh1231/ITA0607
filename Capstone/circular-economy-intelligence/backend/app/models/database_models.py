from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.app.database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class WasteAnalysis(Base):
    __tablename__ = "waste_analyses"
    id = Column(Integer, primary_key=True)
    material = Column(String(80), nullable=False)
    confidence = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    estimated_value = Column(Float, nullable=True)
    recommendation = Column(String(255), nullable=True)
    image_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
