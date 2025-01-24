import cv2
import numpy as np
from PIL import Image
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from modules.ocr import ocr


def get_xp(image) -> float:
    image = image[-350:-310, 315:500]
    image = cv2.resize(image, (0, 0), fx=3, fy=3)
    ocr_text = ocr(Image.fromarray(image), "spl_xp")
    if re.match(r"Xパワー \d*", ocr_text) is None:
        raise Exception(f"Invalid image: {ocr_text}")
    return float(ocr_text.replace("Xパワー", ""))


if __name__ == "__main__":
    for i in range(1, 10, 2):
        image = cv2.imread(f"./screenshots/{i}.jpg")
        power = get_xp(image)
        print(power)
