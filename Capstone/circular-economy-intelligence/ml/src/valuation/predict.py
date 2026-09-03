from ml.src.valuation.features import (
    calculate_recycling_value
)


def predict_value(
    material: str,
    quantity_kg: float
):

    return calculate_recycling_value(
        material=material,
        quantity_kg=quantity_kg
    )


def main():

    print("=" * 60)

    print(
        "RECYCLING VALUE ESTIMATION TEST"
    )

    print("=" * 60)

    examples = [
        ("plastic", 2.0),
        ("metal", 3.0),
        ("paper", 5.0),
        ("cardboard", 10.0),
        ("battery", 1.0),
    ]

    for material, quantity in examples:

        result = predict_value(
            material,
            quantity
        )

        print(
            f"\nMaterial: "
            f"{result['material']}"
        )

        print(
            f"Quantity: "
            f"{result['quantity_kg']} kg"
        )

        print(
            f"Rate: "
            f"{result['currency']} "
            f"{result['rate_per_kg']}/kg"
        )

        print(
            f"Estimated value: "
            f"{result['currency']} "
            f"{result['estimated_value']}"
        )


if __name__ == "__main__":

    main()