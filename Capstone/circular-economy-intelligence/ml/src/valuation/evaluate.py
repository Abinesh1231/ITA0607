from ml.src.valuation.features import (
    load_recycling_rates
)


def main():

    print("=" * 60)

    print(
        "CIRCULAR ECONOMY INTELLIGENCE"
    )

    print(
        "VALUATION DATA VALIDATION"
    )

    print("=" * 60)

    df = load_recycling_rates()

    errors = []

    # --------------------------------------------------------
    # CHECK MATERIAL UNIQUENESS
    # --------------------------------------------------------

    duplicates = df[
        df["material"].duplicated(
            keep=False
        )
    ]

    if not duplicates.empty:

        errors.append(
            "Duplicate material entries found."
        )

    # --------------------------------------------------------
    # CHECK RATES
    # --------------------------------------------------------

    if (
        df["rate_per_kg"] < 0
    ).any():

        errors.append(
            "Negative recycling rate found."
        )

    # --------------------------------------------------------
    # CHECK CURRENCY
    # --------------------------------------------------------

    if df["currency"].isna().any():

        errors.append(
            "Missing currency values found."
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    print(
        f"\nMaterials checked: "
        f"{len(df)}"
    )

    if errors:

        print(
            "\nValidation FAILED:"
        )

        for error in errors:

            print(
                f"✗ {error}"
            )

        raise SystemExit(1)

    print(
        "\n✓ No structural validation errors."
    )

    print(
        "\nValuation data validation PASSED."
    )


if __name__ == "__main__":

    main()