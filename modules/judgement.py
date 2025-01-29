import cv2
import numpy as np
import os
import sys
from typing import Literal
# fmt: off
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from modules.image import get_features, compare_features, calculate_overall_similarity
# fmt: on

JUDGEMENT_PATHS = {
    "win": "./resource/judgement/win.jpg",
    "lose": "./resource/judgement/lose.jpg",
}


def __crop_judgement(image: cv2.Mat):
    return image[170:220, 250:450]


def get_judgement(image) -> Literal["win", "lose", "unknown"]:
    image = __crop_judgement(image)
    image = cv2.resize(image, (0, 0), fx=3, fy=3)
    threshold = 30
    mask = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) < threshold
    image[mask] = [0, 0, 0]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    for name, path in JUDGEMENT_PATHS.items():
        judgement = cv2.imread(path)
        features = get_features(image), get_features(judgement)
        shape_similarity, color_similarity = compare_features(*features)
        similarity = calculate_overall_similarity(
            shape_similarity, color_similarity)
        # print(
        #     f"{name:5}: {similarity:.3} (shape: {shape_similarity:.2}, color: {color_similarity:.3})")
        if similarity > 0.7:
            return name
    return "unknown"


if __name__ == "__main__":
    for i in range(9):
        image = cv2.imread(f"./screenshots/{i+1}.jpg")
        print(f"\n\nScreenshot {i+1}")
        print(get_judgement(image))
