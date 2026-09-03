ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

def is_allowed_image_type(content_type: str):
    return content_type in ALLOWED_IMAGE_TYPES
