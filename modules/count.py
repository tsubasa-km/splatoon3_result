import re

import cv2
import numpy as np
from PIL import Image

from modules.ocr import ocr

_COUNT_PATTERN = re.compile(r"\d{1,3}")


def _extract_count_side(side_image: np.ndarray) -> int | None:
    votes: dict[int, int] = {}
    gray = cv2.cvtColor(side_image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(side_image, cv2.COLOR_BGR2HSV)

    white_mask = cv2.inRange(hsv, (0, 0, 150), (180, 80, 255))
    variants = [
        gray,
        cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)[1],
        white_mask,
    ]

    for img in variants:
        img = cv2.resize(img, (0, 0), fx=4, fy=4)
        for lang in ("eng", "spl_result"):
            try:
                txt = ocr(Image.fromarray(img), lang)
            except Exception:
                continue
            for value in _COUNT_PATTERN.findall(txt):
                n = int(value)
                if 0 <= n <= 100:
                    votes[n] = votes.get(n, 0) + 1

    if not votes:
        return None
    total_votes = sum(votes.values())
    best_value, best_score = max(votes.items(), key=lambda item: item[1])
    confidence = best_score / total_votes

    # 低信頼の誤認識を返すより、Noneで返す方を優先する。
    if best_score < 3 or confidence < 0.4:
        return None
    if best_value < 10 and best_value != 0:
        return None

    return best_value


def get_count(image: np.ndarray) -> dict[str, int | None]:
    """上部のカウント(左/右)をベストエフォートで返す。"""
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be numpy.ndarray")

    # 上部のカウント表示帯
    band = image[120:185, :]
    left_side = band[:, 0:220]
    right_side = band[:, 500:720]

    return {
        "left": _extract_count_side(left_side),
        "right": _extract_count_side(right_side),
    }
