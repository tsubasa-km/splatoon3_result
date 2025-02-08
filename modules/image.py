import cv2
import numpy as np
import matplotlib.pyplot as plt

orb = cv2.ORB_create(
    # nfeatures=1000,
    scaleFactor=1.2,
    edgeThreshold=15,
)


def __extract_features(image):
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return keypoints, descriptors


def __extract_color_histogram(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist(
        [hsv_image], [0, 1], None, [50, 60], [0, 180, 0, 256]
    )  # H:50, S:60
    cv2.normalize(hist, hist)
    return hist


def __display_results(image, keypoints, hist):
    keypoint_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0))

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(keypoint_image, cv2.COLOR_BGR2RGB))
    plt.title("Keypoints")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Color Histogram (Hue-Saturation)")
    plt.xlabel("Bins")
    plt.ylabel("Frequency")
    plt.imshow(hist, interpolation="nearest", aspect="auto", cmap="viridis")
    plt.colorbar(label="Frequency")
    plt.show()


def get_features(image):
    """画像の特徴量を抽出"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = __extract_features(gray_image)
    color_hist = __extract_color_histogram(image)
    # display_results(image, keypoints, color_hist)
    return keypoints, descriptors, color_hist


def compare_features(features_a, features_b):
    """2つの画像の特徴量を比較し、形状と色の類似度を計算"""
    keypoints_a, descriptors_a, color_hist_a = features_a
    keypoints_b, descriptors_b, color_hist_b = features_b
    if descriptors_a is not None and descriptors_b is not None:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors_a, descriptors_b)
        shape_similarity = len(matches) / max(len(keypoints_a), len(keypoints_b))
    else:
        shape_similarity = 0.0
    color_similarity = cv2.compareHist(color_hist_a, color_hist_b, cv2.HISTCMP_CORREL)
    return shape_similarity, color_similarity


def calculate_overall_similarity(
    shape_similarity, color_similarity, weight_shape=0.5, weight_color=0.5
):
    """形状と色の類似度を統合スコアとして計算"""
    normalized_color_similarity = (color_similarity + 1) / 2
    overall_similarity = (
        weight_shape * shape_similarity + weight_color * normalized_color_similarity
    )
    return overall_similarity


def is_match(features_a, features_b, threshold=0.9):
    """2つの画像が一致するかどうかを判定"""
    shape_similarity, color_similarity = compare_features(features_a, features_b)
    overall_similarity = calculate_overall_similarity(
        shape_similarity, color_similarity
    )
    return overall_similarity >= threshold
