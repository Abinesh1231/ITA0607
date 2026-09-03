RECOMMENDATIONS = {
    "paper": ("Recycle", "Keep dry and send to paper recycling."),
    "cardboard": ("Recycle", "Flatten and send to paper/cardboard recycling."),
    "plastic": ("Recycle", "Clean, sort by plastic type when possible, and send to plastic recycling."),
    "metal": ("Recycle", "Separate metal from mixed waste and send to a metal recycler."),
    "white-glass": ("Recycle", "Separate glass by local collection rules."),
    "green-glass": ("Recycle", "Separate glass by local collection rules."),
    "brown-glass": ("Recycle", "Separate glass by local collection rules."),
    "battery": ("Special recycling", "Do not place batteries in normal household waste; use an authorized collection point."),
    "clothes": ("Reuse / textile recovery", "Donate, repair, reuse or send to textile recovery."),
    "shoes": ("Reuse / textile recovery", "Donate, repair, reuse or send to footwear/textile recovery."),
    "biological": ("Compost / organic processing", "Use composting or an appropriate organic-waste collection system."),
    "trash": ("General disposal", "Check whether any components can be separated before disposal."),
}

def recommendation_for(material: str):
    key = material.lower().strip()
    action, detail = RECOMMENDATIONS.get(key, ("Review manually", "Material was not recognized."))
    return {"material": key, "action": action, "detail": detail}
