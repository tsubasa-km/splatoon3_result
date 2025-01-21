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


def result_ocr(img: Image.Image):
    engines = pyocr.get_available_tools()
    engine = engines[0]

    langs = engine.get_available_languages()
    if "spl" not in langs:
        raise Exception("Language not supported")
    txt = engine.image_to_string(img, lang="spl")
    return txt


def format_result(txt: str):
    lines = txt.replace(" ","").split("\n")
    pattern = re.compile(r"^\d*px\d*(<\d*>)?x\d*x\d*")
    value = []
    for line in lines:
        if pattern.match(line):
            splat, ka, d, sp = line.replace("p","").split("x")
            k, a = ka.replace(">","").split("<") if "<" in ka else (ka, "0")
            value.append((int(k), int(a), int(d), int(sp), int(splat)))
    return value


def crop_result(img: np.ndarray):
    img = img[300:-350,-280:-25]
    _, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    return img


if __name__ == '__main__':
    for i in range(1,6):
        img = cv2.imread(f"{SCREENSHOT_DIR}/{i}.jpg")
        if img is None:
            raise Exception("Image not found")
        results = crop_result(img)
        txt = result_ocr(Image.fromarray(results))
        print(format_result(txt))
