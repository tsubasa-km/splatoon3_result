from dotenv import load_dotenv
from glob import glob
from PIL import Image
import pyocr
import pyocr.builders
import shutil
import os

load_dotenv()
print(os.getenv("TESSERACT_DIR"))
pyocr.tesseract.TESSERACT_CMD = os.path.join(
    os.getenv("TESSERACT_DIR"), "tesseract.exe"
)

for file in glob(os.path.join("tessdata", "*.traineddata")):
    if not os.path.exists(os.path.join(os.getenv("TESSERACT_DIR"), file)):
        shutil.copy2(file, os.path.join(os.getenv("TESSERACT_DIR"), "tessdata"))
        print(f"Copying {file} to {os.path.join(os.getenv('TESSERACT_DIR'), 'tessdata')}")

def ocr(img: Image.Image, lang) -> str:
    engines = pyocr.get_available_tools()
    engine = engines[0]

    langs = engine.get_available_languages()
    if lang not in langs:
        raise Exception("Language not supported")
    txt = engine.image_to_string(
        img, lang=lang, builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    return txt
