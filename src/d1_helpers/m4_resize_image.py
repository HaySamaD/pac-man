from typing import Tuple

from PIL import Image
# import the pillow library to resize the curren image


class Resizer:
    def __init__(self, resolution: Tuple[int, int]) -> None:
        self.width, self.height = resolution
        self.resize()

    def resize(self) -> None:
        img = Image.open("assets/instructions/instructions_original.jpeg")
        new_image = img.resize((self.width, self.height * 95//100))
        new_image.save("assets/instructions/instructions_resized.jpeg")
