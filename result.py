from dotenv import load_dotenv
import matplotlib.pyplot as plt
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


def crop_result(img: np.ndarray):
    img = img[300:-350,-280:-25]
    _, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    # return [
    #     img[83:110, :],
    #     img[181:208, :],
    #     img[278:305, :],
    #     img[376:403, :],
    #     img[530:557, :],
    #     img[627:654, :],
    #     img[725:752, :],
    #     img[822:849, :],
    # ]
    return img


if __name__ == '__main__':
    img = cv2.imread(SCREENSHOT_DIR+"/1.jpg")
    if img is None:
        raise Exception("Image not found")
    results = crop_result(img)
    # for result in results:
    #     result = Image.fromarray(result)
    #     txt = result_ocr(result)
    #     print(format_result(txt))
    txt = result_ocr(Image.fromarray(results))
    print(format_result(txt))
