from pathlib import Path

import pandas as pd


# ============================================================
# PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

RATES_FILE = (
    PROJECT_ROOT /
    "database" /
    "recycling_rates.csv"
)


# ============================================================
# LOAD RATES
# ============================================================

def load_recycling_rates():
    """
    Load recycling reference rates from CSV.
    """

    if not RATES_FILE.exists():

        raise FileNotFoundError(
            f"Recycling rates file not found:\n"
            f"{RATES_FILE}"
        )

    df = pd.read_csv(
        RATES_FILE
    )

    required_columns = {
        "material",
        "rate_per_kg",
        "currency",
        "source_note"
    }

    missing = (
        required_columns
        - set(df.columns)
    )

    if missing:

        raise ValueError(
            "Missing required columns: "
            f"{sorted(missing)}"
        )

    df["material"] = (
        df["material"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["rate_per_kg"] = pd.to_numeric(
        df["rate_per_kg"],
        errors="raise"
    )

    return df


# ============================================================
# MATERIAL LOOKUP
# ============================================================

def get_material_rate(
    material: str
):

    df = load_recycling_rates()

    material = (
        material
        .strip()
        .lower()
    )

    matches = df[
        df["material"] == material
    ]

    if matches.empty:

        raise ValueError(
            f"Material '{material}' "
            "not found in recycling rates."
        )

    row = matches.iloc[0]

    return {
        "material":
            row["material"],

        "rate_per_kg":
            float(row["rate_per_kg"]),

        "currency":
            row["currency"],

        "source_note":
            row["source_note"]
    }


# ============================================================
# VALUE CALCULATION
# ============================================================

def calculate_recycling_value(
    material: str,
    quantity_kg: float
):

    if quantity_kg < 0:

        raise ValueError(
            "Quantity cannot be negative."
        )

    rate_info = get_material_rate(
        material
    )

    estimated_value = (
        rate_info["rate_per_kg"]
        * quantity_kg
    )

    return {
        "material":
            rate_info["material"],

        "quantity_kg":
            float(quantity_kg),

        "rate_per_kg":
            rate_info["rate_per_kg"],

        "currency":
            rate_info["currency"],

        "estimated_value":
            round(
                estimated_value,
                2
            ),

        "source_note":
            rate_info["source_note"]
    }