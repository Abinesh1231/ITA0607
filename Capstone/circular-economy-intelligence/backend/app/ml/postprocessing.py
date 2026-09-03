RECYCLABLE = {
    "paper", "cardboard", "plastic", "metal",
    "white-glass", "green-glass", "brown-glass",
    "battery", "clothes", "shoes"
}

def postprocess(label, confidence):
    recyclable = label in RECYCLABLE
    return {
        "material": label,
        "confidence": confidence,
        "recyclable": recyclable,
        "recommendation": "Recycle/recover material" if recyclable else "Use appropriate waste disposal route",
    }
