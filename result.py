from dotenv import load_dotenv
import pyocr.builders
from glob import glob
from PIL import Image
import numpy as np
import shutil
import pyocr
import cv2
import os
import re


SCREENSHOT_DIR = "screenshots"

load_dotenv()

pyocr.tesseract.TESSERACT_CMD = os.getenv(
    'TESSERACT_DIR')+"\\tesseract.exe"

for file in glob("tessdata\\*.traineddata"):
    if not os.path.exists(os.getenv('TESSERACT_DIR')+file):
        shutil.copy2(file, f"{os.getenv('TESSERACT_DIR')}tessdata\\")
        print(f"Copying {file} to {os.getenv('TESSERACT_DIR')}tessdata\\")


def __result_ocr(img: Image.Image):
    engines = pyocr.get_available_tools()
    engine = engines[0]

    langs = engine.get_available_languages()
    if "spl" not in langs:
        raise Exception("Language not supported")
    txt = engine.image_to_string(
        img,
        lang="spl",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    return txt


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


def get_result_from_image_path(img_path: str):
    img = cv2.imread(img_path, 0)
    if img is None:
        raise Exception("Path is invalid")
    results = __crop_result(img)
    txt = __result_ocr(Image.fromarray(results))
    return __format_result(txt)


if __name__ == '__main__':
    for i in range(1, 6):
        result = get_result_from_image_path(f"{SCREENSHOT_DIR}/{i}.jpg")
        if len(result) != 8:
            raise Exception(f"Invalid result. length :{len(result)}")
        print(result)
