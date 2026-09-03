from PIL import Image

def validate_image(path: str):
    with Image.open(path) as image:
        image.verify()
    return True
