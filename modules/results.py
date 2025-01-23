from PIL import Image
import numpy as np
import cv2
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from modules.ocr import ocr

SCREENSHOT_DIR = "screenshots"


def __format_result(txt: str):
    lines = txt.replace(" ", "").split("\n")
    pattern = re.compile(r"^\d*px\d*(<\d*>)?x\d*x\d*")
    value = []
    for line in lines:
        if pattern.match(line):
            splat, ka, d, sp = line.replace("p", "").split("x")
            k, a = ka.replace(">", "").split("<") if "<" in ka else (ka, "0")
            value.append((int(k), int(a), int(d), int(sp), int(splat)))
    return tuple(value)


def __crop_result(img: np.ndarray):
    img = img[300:-350, -280:-25]
    _, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    return img


def get_result(image):
    if type(image) != np.ndarray:
        raise Exception("Invalid image type")
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = __crop_result(gray_img)
    txt = ocr(Image.fromarray(results), "spl_result")
    return __format_result(txt)


if __name__ == '__main__':
    for i in range(1, 6):
        result = get_result(cv2.imread(f"{SCREENSHOT_DIR}/{i}.jpg"))
        print(result)
