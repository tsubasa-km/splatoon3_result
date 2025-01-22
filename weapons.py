import cv2
import numpy as np
import matplotlib.pyplot as plt

from image import get_icon_features, compare_icons, calculate_overall_similarity

__circles = None


def __mode(arr: np.ndarray) -> any:
    unique, counts = np.unique(arr, return_counts=True)
    return unique[np.argmax(counts)]


def detect_weapons(image_path: str):
    """武器アイコンを検出"""
    global __circles
    image = cv2.imread(image_path)
    image = image[300:-350, 10:120]
    if __circles is None:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_image, (9, 9), 2)
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=30
        )
        if circles is None:
            raise ValueError("円が検出されませんでした。")
        circles = np.round(circles[0, :]).astype("int")
        circles[:, 0] = __mode(circles[:, 0])
        circles[:, 2] = __mode(circles[:, 2])
        __circles = [(int(x), int(y), int(r)) for x, y, r in circles]
        __circles.sort(key=lambda x: x[1])
    return image, __circles


def crop_icons(img, circles):
    """アイコンを切り抜く"""
    crops = []
    for x, y, r in circles:
        crop = img[y - r:y + r, x - r:x + r]
        crops.append(crop)
    return crops


if __name__ == "__main__":
    weapons = crop_icons(*detect_weapons(f"screenshots/1.jpg"))
    img = np.vstack(weapons)
    cv2.imshow("Weapons", img)
    cv2.waitKey(0)
    features = [get_icon_features(icon) for icon in weapons]
    for w1 in range(len(weapons)):
        for w2 in range(w1 + 1, len(weapons)):
            shape_similarity, color_similarity = compare_icons(
                features[w1], features[w2])
            overall_similarity = calculate_overall_similarity(
                shape_similarity, color_similarity)
            if overall_similarity > 0.9:
                img = np.hstack((weapons[w1], weapons[w2]))
                cv2.imshow("Comparison", img)
                cv2.waitKey(0)
            print(
                f"Icon {w1+1} vs Icon {w2+1}: Similarity = {overall_similarity:.2f}")
