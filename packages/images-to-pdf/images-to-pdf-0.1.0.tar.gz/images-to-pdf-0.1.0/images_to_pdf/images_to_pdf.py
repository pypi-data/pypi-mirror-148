from typing import List

from PIL import Image


def execute(name: str, image_files: List[str]):

    images = []
    for path in image_files:
        img = Image.open(path)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        images.append(img)

    images[0].save(f"{name}", "pdf", save_all=True, append_images=images[1:])
