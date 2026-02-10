import cv2
import numpy as np

from modules.weapons import get_weapon_icon_circles

_YELLOW_LOWER = np.array([15, 120, 120], dtype=np.uint8)
_YELLOW_UPPER = np.array([40, 255, 255], dtype=np.uint8)


def _crop_player_left_area(image: np.ndarray) -> np.ndarray:
    # プレイヤー一覧の左側(矢印がある帯)
    return image[300:-350, 10:120]


def get_my_position(image: np.ndarray, threshold: int = 40) -> int | None:
    """自分の行インデックス(0-7)を返す。検出失敗時はNone。"""
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be numpy.ndarray")

    circles = get_weapon_icon_circles(image)
    if not circles:
        return None

    cropped = _crop_player_left_area(image)
    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, _YELLOW_LOWER, _YELLOW_UPPER)

    scores: list[int] = []
    for _, y, _ in circles:
        y0 = max(0, y - 22)
        y1 = min(yellow_mask.shape[0], y + 22)
        band = yellow_mask[y0:y1, :40]
        scores.append(int(np.count_nonzero(band)))

    best_idx = int(np.argmax(scores))
    if scores[best_idx] < threshold:
        return None
    return best_idx


def get_is_me_flags(image: np.ndarray) -> list[bool]:
    """8人分の行に対し、自分の行だけTrueの配列を返す。"""
    circles = get_weapon_icon_circles(image)
    result = [False] * len(circles)
    my_index = get_my_position(image)
    if my_index is None:
        return result
    result[my_index] = True
    return result
