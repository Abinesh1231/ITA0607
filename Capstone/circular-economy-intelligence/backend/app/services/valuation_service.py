from pathlib import Path

import joblib
import pandas as pd

from backend.app.core.config import settings


# ============================================================
# DEFAULT RECYCLING RATES
# ============================================================

DEFAULT_RATES = {
    "paper": 12.0,
    "cardboard": 8.0,
    "plastic": 25.0,
    "metal": 45.0,
    "white-glass": 4.0,
    "green-glass": 4.0,
    "brown-glass": 4.0,
    "battery": 80.0,
    "clothes": 15.0,
    "shoes": 10.0,
    "biological": 0.0,
    "trash": 0.0,
}


# ============================================================
# MODEL PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_DIR = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "valuation"
)

MODEL_FILE = (
    MODEL_DIR
    / "recycling_value_model.pkl"
)

SCALER_FILE = (
    MODEL_DIR
    / "scaler.pkl"
)


# ============================================================
# LOAD RECYCLING RATES
# ============================================================

def _load_rates():
    path = PROJECT_ROOT / "database" / "recycling_rates.csv"

    if not path.exists():
        return DEFAULT_RATES

    try:
        df = pd.read_csv(path)

        return {
            str(row.material).lower().strip():
            float(row.rate_per_kg)
            for row in df.itertuples()
        }

    except Exception:
        return DEFAULT_RATES


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

def _load_model():

    if not MODEL_FILE.exists():
        return None

    return joblib.load(MODEL_FILE)


# ============================================================
# LOAD SCALER
# ============================================================

def _load_scaler():

    if not SCALER_FILE.exists():
        return None

    return joblib.load(SCALER_FILE)


# ============================================================
# VALUE ESTIMATION
# ============================================================

def estimate_value(
    material: str,
    weight_kg: float,
    quality_factor: float = 1.0,
):

    rates = _load_rates()

    key = material.lower().strip()

    if key not in rates:
        raise ValueError(
            f"Material '{key}' is not available."
        )

    rate = rates[key]

    # --------------------------------------------------------
    # CHECK MODEL AVAILABILITY
    # --------------------------------------------------------

    model = _load_model()
    scaler = _load_scaler()

    if model is None or scaler is None:

        # Fallback to reference calculation
        value = (
            weight_kg
            * rate
            * quality_factor
        )

        return {
            "material": key,
            "weight_kg": round(weight_kg, 4),
            "rate_per_kg": rate,
            "quality_factor": quality_factor,
            "estimated_value": round(value, 2),
            "currency": "INR",
            "prediction_method": "reference_calculation",
            "note": (
                "Trained valuation model unavailable. "
                "Reference rate calculation used."
            ),
        }

    # --------------------------------------------------------
    # PREPARE MODEL FEATURES
    # --------------------------------------------------------

    features = pd.DataFrame(
        [
            {
                "weight_kg": weight_kg,
                "rate_per_kg": rate,
                "quality_factor": quality_factor,
            }
        ]
    )

    # --------------------------------------------------------
    # SCALE FEATURES
    # --------------------------------------------------------

    features_scaled = scaler.transform(
        features
    )

    # --------------------------------------------------------
    # RANDOM FOREST PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(
        features_scaled
    )

    estimated_value = float(
        prediction[0]
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {
        "material": key,
        "weight_kg": round(weight_kg, 4),
        "rate_per_kg": rate,
        "quality_factor": quality_factor,
        "estimated_value": round(
            estimated_value,
            2
        ),
        "currency": "INR",
        "prediction_method": "random_forest",
        "model": "RandomForestRegressor",
        "note": (
            "Value predicted using the trained "
            "Random Forest valuation model."
        ),
    }

# ============================================================
# VALUATION MODEL METRICS
# ============================================================

def get_valuation_metrics():

    metrics_file = (
        MODEL_DIR
        / "metrics.json"
    )

    if not metrics_file.exists():
        return {
            "available": False,
            "message": "Valuation model metrics are not available.",
        }

    try:
        import json

        metrics = json.loads(
            metrics_file.read_text(
                encoding="utf-8"
            )
        )

        return {
            "available": True,
            "mae": metrics.get("mae", 0),
            "rmse": metrics.get("rmse", 0),
            "r2_score": metrics.get("r2_score", 0),
            "training_samples": metrics.get(
                "training_samples",
                0
            ),
            "testing_samples": metrics.get(
                "testing_samples",
                0
            ),
            "model": metrics.get(
                "model",
                "RandomForestRegressor"
            ),
        }

    except Exception as exc:
        return {
            "available": False,
            "message": str(exc),
        }