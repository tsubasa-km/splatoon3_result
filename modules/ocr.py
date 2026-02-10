import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image
import pyocr
import pyocr.builders

load_dotenv()

_IS_CONFIGURED = False


def _resolve_tesseract_cmd() -> str:
    explicit_cmd = os.getenv("TESSERACT_CMD")
    if explicit_cmd:
        return explicit_cmd

    tesseract_dir = os.getenv("TESSERACT_DIR")
    if tesseract_dir:
        for name in ("tesseract.exe", "tesseract"):
            candidate = Path(tesseract_dir) / name
            if candidate.exists():
                return str(candidate)

    tesseract_cmd = shutil.which("tesseract")
    if tesseract_cmd:
        return tesseract_cmd

    raise RuntimeError(
        "tesseract command was not found. Set TESSERACT_CMD or install tesseract."
    )


def _configure_tesseract() -> None:
    global _IS_CONFIGURED
    if _IS_CONFIGURED:
        return

    pyocr.tesseract.TESSERACT_CMD = _resolve_tesseract_cmd()
    project_tessdata = Path(__file__).resolve().parent.parent / "tessdata"
    tessdata_prefix = os.getenv("TESSDATA_PREFIX")
    os.environ["TESSDATA_PREFIX"] = (
        tessdata_prefix if tessdata_prefix else str(project_tessdata)
    )
    _IS_CONFIGURED = True


def ocr(img: Image.Image, lang: str) -> str:
    _configure_tesseract()
    engines = pyocr.get_available_tools()
    if not engines:
        raise RuntimeError("OCR engine was not found. Check your tesseract installation.")

    engine = engines[0]
    langs = engine.get_available_languages()
    if lang not in langs:
        raise ValueError(f"Language not supported: {lang}")

    return engine.image_to_string(
        img, lang=lang, builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
