from ml.src.valuation.features import (
    load_recycling_rates
)


def main():

    print("=" * 60)

    print(
        "CIRCULAR ECONOMY INTELLIGENCE"
    )

    print(
        "RECYCLING VALUE DATASET"
    )

    print("=" * 60)

    df = load_recycling_rates()

    print(
        f"\nMaterials available: "
        f"{len(df)}"
    )

    print(
        "\nReference rates:"
    )

    print(
        df[
            [
                "material",
                "rate_per_kg",
                "currency"
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "\nNo regression model is trained."
    )

    print(
        "The current dataset contains"
        " one reference rate per material."
    )

    print(
        "Valuation uses:"
    )

    print(
        "estimated_value = quantity_kg × rate_per_kg"
    )


if __name__ == "__main__":

    main()