import cv2

from modules.xp import get_xp
from modules.results import get_result
from modules.weapons import get_icon_features
from modules.rule import get_rule_name


def get_all_data(image):
    return {
        "xp": get_xp(image),
        "rule": get_rule_name(image),
        "result": get_result(image),
        "weapons": get_icon_features(image)
    }


if __name__ == '__main__':
    for i in range(1, 10, 2):
        image = cv2.imread(f'./screenshots/{i}.jpg')
        data = get_all_data(image)
        print(data["xp"], data["rule"], [r[0] for r in data["result"]])
