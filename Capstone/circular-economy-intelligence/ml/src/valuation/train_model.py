from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "valuation"
    / "valuation_dataset.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "valuation"
)

MODEL_FILE = MODEL_DIR / "recycling_value_model.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"
METRICS_FILE = MODEL_DIR / "metrics.json"


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("CIRCULAR ECONOMY INTELLIGENCE")
    print("RECYCLING VALUE MODEL TRAINING")
    print("=" * 60)

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    print("\nLoading dataset:")

    df = pd.read_csv(DATA_FILE)

    print(f"Dataset: {DATA_FILE}")
    print(f"Rows: {len(df)}")

    # --------------------------------------------------------
    # FEATURES / TARGET
    # --------------------------------------------------------

    features = [
        "weight_kg",
        "rate_per_kg",
        "quality_factor",
    ]

    target = "value"

    X = df[features]
    y = df[target]

    # --------------------------------------------------------
    # TRAIN / TEST SPLIT
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # --------------------------------------------------------
    # SCALER
    # --------------------------------------------------------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=8,
        min_samples_leaf=1,
    )

    print("\nTraining Random Forest...")

    model.fit(
        X_train_scaled,
        y_train,
    )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    predictions = model.predict(
        X_test_scaled
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions,
    )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"\nMAE      : ₹{mae:.2f}")
    print(f"RMSE     : ₹{rmse:.2f}")
    print(f"R² Score : {r2:.4f}")

    # --------------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_FILE,
    )

    joblib.dump(
        scaler,
        SCALER_FILE,
    )

    # --------------------------------------------------------
    # SAVE METRICS
    # --------------------------------------------------------

    import json

    metrics = {
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "r2_score": round(float(r2), 4),
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "model": "RandomForestRegressor",
    }

    METRICS_FILE.write_text(
        json.dumps(
            metrics,
            indent=4,
        ),
        encoding="utf-8",
    )

    print("\nSaved files:")

    print(
        f"Model  : {MODEL_FILE}"
    )

    print(
        f"Scaler : {SCALER_FILE}"
    )

    print(
        f"Metrics: {METRICS_FILE}"
    )

    print("\nTraining completed successfully.")


if __name__ == "__main__":
    main()