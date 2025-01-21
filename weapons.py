import cv2
import numpy as np

__circles = None

def mode(arr: np.ndarray) -> any:
    unique, counts = np.unique(arr, return_counts=True)
    return unique[np.argmax(counts)]


def detect_weapons(image_path: str):
    global __circles
    if __circles is None:
        image = cv2.imread(image_path)
        image = image[300:-350, 10:120]
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
        circles[:, 0] = mode(circles[:, 0])
        circles[:, 2] = mode(circles[:, 2])
        __circles = [(int(x), int(y), int(r)) for x, y, r in circles]
    return __circles

if __name__ == "__main__":
    for i in range(1, 6):
        weapons = detect_weapons(f"screenshots/{i}.jpg")
        print(weapons)
