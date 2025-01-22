import cv2
import numpy as np
import matplotlib.pyplot as plt

__circles = None

orb = cv2.ORB_create(
    # nfeatures=1000,
    scaleFactor=1.2,
    edgeThreshold=15
)


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


def extract_features(image):
    """形状特徴量（ORB）を抽出"""
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors


def extract_color_histogram(image):
    """色ヒストグラムを抽出"""
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv_image], [0, 1], None, [50, 60], [
                        0, 180, 0, 256])  # H:50, S:60
    cv2.normalize(hist, hist)
    return hist


def display_results(image, keypoints, hist):
    """抽出結果を表示"""
    keypoint_image = cv2.drawKeypoints(
        image, keypoints, None, color=(0, 255, 0))

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(keypoint_image, cv2.COLOR_BGR2RGB))
    plt.title("Keypoints")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Color Histogram (Hue-Saturation)")
    plt.xlabel("Bins")
    plt.ylabel("Frequency")
    plt.imshow(hist, interpolation='nearest', aspect='auto', cmap='viridis')
    plt.colorbar(label="Frequency")
    plt.show()


def get_icon_features(image):
    """画像を読み込み、特徴量を抽出して表示"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = extract_features(gray_image)
    color_hist = extract_color_histogram(image)
    # display_results(image, keypoints, color_hist)
    return keypoints, descriptors, color_hist


def compare_icons(features_a, features_b):
    """2つの画像の特徴量を比較し、形状と色の類似度を計算"""
    keypoints_a, descriptors_a, color_hist_a = features_a
    keypoints_b, descriptors_b, color_hist_b = features_b
    if descriptors_a is not None and descriptors_b is not None:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors_a, descriptors_b)
        shape_similarity = len(matches) / \
            max(len(keypoints_a), len(keypoints_b))
    else:
        shape_similarity = 0.0
    color_similarity = cv2.compareHist(
        color_hist_a, color_hist_b, cv2.HISTCMP_CORREL)
    return shape_similarity, color_similarity


def calculate_overall_similarity(shape_similarity, color_similarity, weight_shape=0.5, weight_color=0.5):
    """形状と色の類似度を統合スコアとして計算"""
    normalized_color_similarity = (color_similarity + 1) / 2
    overall_similarity = (weight_shape * shape_similarity +
                          weight_color * normalized_color_similarity)
    return overall_similarity


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
