import os
from PIL import Image


def save_texture(image, path, filename):
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    image.save(file_path)
    print(f"Texture saved to {file_path}")
