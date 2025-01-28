import cv2
import numpy as np
from PIL import Image
import re
import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from modules.ocr import ocr


def get_time(image) -> tuple[datetime, timedelta]:
    image = image[-300:-270, 230:500]
    image = cv2.resize(image, (0, 0), fx=3, fy=3)
    _, image = cv2.threshold(image, 90, 255, cv2.THRESH_BINARY)
    ocr_text = ocr(Image.fromarray(image), "spl_datetime")
    ocr_text = ocr_text.replace(" ", "")
    game_time = ocr_text[-4:]
    time = ocr_text[-4 + -5 : -4]
    date = ocr_text[: -4 + -5]
    if (
        not re.match(r"\d{4}/\d{2}/\d{2}", date)
        or not re.match(r"\d{2}:\d{2}", time)
        or not re.match(r"\d{1}:\d{2}", game_time)
    ):
        raise ValueError("OCR failed to recognize the date and time")
    date_time = datetime.strptime(f"{date} {time}", "%Y/%m/%d %H:%M")
    game_time = timedelta(
        minutes=int(game_time.split(":")[0]), seconds=int(game_time.split(":")[1])
    )
    return date_time, game_time


if __name__ == "__main__":
    for i in range(1, 10):
        image = cv2.imread(f"./screenshots/{i}.jpg")
        power = get_time(image)
        print(power)
