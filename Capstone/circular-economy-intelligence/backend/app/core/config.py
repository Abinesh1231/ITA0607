from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Circular Economy Intelligence API"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-secret-key"
    DATABASE_URL: str = "sqlite:///./circular_economy.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    CLASSIFIER_MODEL_PATH: str = "ml/models/classification/best_model.pt"
    CLASS_NAMES_PATH: str = "ml/models/classification/class_names.json"
    DETECTOR_MODEL_PATH: str = "ml/models/detection/best_model.pt"
    VALUATION_MODEL_PATH: str = "ml/models/valuation/recycling_value_model.pkl"
    VALUATION_SCALER_PATH: str = "ml/models/valuation/scaler.pkl"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self):
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

settings = Settings()
