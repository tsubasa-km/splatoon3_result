import cv2

from modules.xp import get_xp
from modules.results import get_result
from modules.weapons import get_icon_features
from modules.rule import get_rule_name
from modules.judgement import get_judgement
from modules.times import get_time


def get_all_data(image):
    date_time, game_time = get_time(image)
    return {
        "xp": get_xp(image),
        "rule": get_rule_name(image),
        "judgement": get_judgement(image),
        "datetime": date_time,
        "game_time": game_time,
        "result": get_result(image),
        "weapons": get_icon_features(image)
    }


if __name__ == '__main__':
    for i in range(1, 10, 2):
        image = cv2.imread(f'./screenshots/{i}.jpg')
        data = get_all_data(image)
        print(
            data["xp"],
            data["rule"],
            data["judgement"],
            data["datetime"],
            data["game_time"],
            [r[0] for r in data["result"]],
        )
