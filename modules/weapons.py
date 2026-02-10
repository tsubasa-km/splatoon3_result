import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from modules.image import get_features, is_match

__circles = None


def __mode(arr: np.ndarray) -> any:
    unique, counts = np.unique(arr, return_counts=True)
    return unique[np.argmax(counts)]


def __detect_weapons(image: np.ndarray) -> tuple:
    """武器アイコンを検出"""
    global __circles
    image = image[300:-350, 10:120]
    if __circles is None:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_image, (9, 9), 2)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30)
        if circles is None:
            raise ValueError("円が検出されませんでした。")
        circles = np.round(circles[0, :]).astype("int")
        circles[:, 0] = __mode(circles[:, 0])
        circles[:, 2] = __mode(circles[:, 2])
        __circles = [(int(x), int(y), int(r)) for x, y, r in circles]
        __circles.sort(key=lambda x: x[1])
    return image, __circles


def __crop_icons(img: np.ndarray, circles: list) -> list:
    """アイコンを切り抜く"""
    crops = []
    for x, y, r in circles:
        crop = img[y - r : y + r, x - r : x + r]
        crops.append(crop)
    return crops


def get_icon_features(image: np.ndarray) -> list:
    """アイコンの特徴量を取得"""
    weapons = __crop_icons(*__detect_weapons(image))
    return [get_features(weapon) for weapon in weapons]


def get_weapon_icon_circles(image: np.ndarray) -> list[tuple[int, int, int]]:
    """武器アイコンの円情報(x, y, r)を返す"""
    _, circles = __detect_weapons(image)
    return circles.copy()


if __name__ == "__main__":
    weapons = __crop_icons(*__detect_weapons(cv2.imread(f"screenshots/1.jpg")))
    features = [get_features(icon) for icon in weapons]

    for w1 in range(len(weapons)):
        for w2 in range(w1 + 1, len(weapons)):
            if is_match(features[w1], features[w2]):
                img = np.hstack((weapons[w1], weapons[w2]))
                cv2.imshow("Comparison", img)
                cv2.waitKey(0)
