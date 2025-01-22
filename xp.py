import cv2
import numpy as np
from PIL import Image

from ocr import ocr


def get_xp(image) -> float:
    image = image[-350:-310, 315:500]
    ocr_text = ocr(Image.fromarray(image), "spl_xp")
    return float(ocr_text.replace('Xパワー', ''))


if __name__ == '__main__':
    for i in range(1, 10, 2):
        image = cv2.imread(f'./screenshots/{i}.jpg')
        power = get_xp(image)
        print(power)
