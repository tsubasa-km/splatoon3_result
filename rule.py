import cv2

from image import get_features, compare_features, calculate_overall_similarity


RULE_PATHS = {
    "zone": "./resource/rules/zone.jpg",
    "tower": "./resource/rules/tower.jpg",
    "rainmaker": "./resource/rules/rainmaker.jpg",
    "blitz": "./resource/rules/blitz.jpg",
}


def crop_rule(image: cv2.Mat):
    return image[50:130, 200:540]


def get_rule_name(image):
    image = crop_rule(image)
    for name, path in RULE_PATHS.items():
        rule = cv2.imread(path)
        features = get_features(image), get_features(rule)
        shape_similarity, color_similarity = compare_features(*features)
        overall_similarity = calculate_overall_similarity(
            shape_similarity, color_similarity)
        if overall_similarity > 0.9:
            return name
    return "unknown"


if __name__ == "__main__":
    image = cv2.imread("./screenshots/1.jpg")
    print(get_rule_name(image))
