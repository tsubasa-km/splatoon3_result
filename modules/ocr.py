import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image
import pyocr
import pyocr.builders

load_dotenv()

_IS_CONFIGURED = False
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PROJECT_TESSDATA = _PROJECT_ROOT / "tessdata"


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
    tessdata_prefix = os.getenv("TESSDATA_PREFIX")
    os.environ["TESSDATA_PREFIX"] = (
        tessdata_prefix if tessdata_prefix else str(_PROJECT_TESSDATA)
    )
    _IS_CONFIGURED = True


def _find_system_tessdata() -> str | None:
    candidates = [
        "/usr/share/tesseract-ocr/5/tessdata",
        "/usr/share/tesseract-ocr/4.00/tessdata",
        "/usr/share/tesseract-ocr/tessdata",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def _set_tessdata_prefix_for_lang(lang: str) -> None:
    custom_prefix = os.getenv("TESSDATA_PREFIX")
    custom_path = Path(custom_prefix) if custom_prefix else None
    system_prefix = _find_system_tessdata()

    if lang.startswith("spl_"):
        os.environ["TESSDATA_PREFIX"] = str(_PROJECT_TESSDATA)
        return

    if custom_path and (custom_path / f"{lang}.traineddata").exists():
        os.environ["TESSDATA_PREFIX"] = str(custom_path)
        return

    if system_prefix and Path(system_prefix, f"{lang}.traineddata").exists():
        os.environ["TESSDATA_PREFIX"] = system_prefix
        return


def ocr(img: Image.Image, lang: str) -> str:
    _configure_tesseract()
    _set_tessdata_prefix_for_lang(lang)
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
