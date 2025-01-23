import pytest
import cv2

from modules.xp import get_xp
from modules.results import get_result
# from modules.weapons import get_icon_features
from modules.rule import get_rule_name


@pytest.mark.parametrize(("image", "expected"), [
    (cv2.imread(f'./screenshots/1.jpg'), 2368.9),
    (cv2.imread(f'./screenshots/6.jpg'), 2099.0),
    (cv2.imread(f'./screenshots/7.jpg'), 2288.9),
    (cv2.imread(f'./screenshots/9.jpg'), 2255.2),
])
def test_get_xp(image, expected):
    assert get_xp(image) == expected


@pytest.mark.parametrize(("image", "expected"), [
    (cv2.imread('./screenshots/1.jpg'), (
        (12, 5, 8, 4, 1335),
        (14, 2, 9, 2, 1020),
        (8, 3, 6, 6, 1562),
        (13, 6, 8, 3, 1051),
        (14, 2, 8, 5, 1232),
        (13, 6, 8, 3, 980),
        (9, 4, 8, 4, 1204),
        (8, 1, 7, 6, 1465)
    )),
    (cv2.imread('./screenshots/2.jpg'), (
        (11, 3, 4, 5, 1541),
        (15, 3, 7, 4, 1294),
        (15, 5, 9, 2, 822),
        (11, 5, 10, 2, 1270),
        (15, 1, 9, 4, 1425),
        (8, 5, 9, 3, 1365),
        (9, 1, 8, 3, 1415),
        (7, 2, 10, 0, 508)
    )),
    (cv2.imread('./screenshots/3.jpg'), (
        (17, 6, 3, 5, 1204),
        (15, 2, 5, 4, 1258),
        (15, 8, 9, 3, 1278),
        (10, 1, 10, 2, 1222),
        (15, 6, 7, 3, 1256),
        (13, 2, 11, 4, 1340),
        (6, 2, 10, 2, 989),
        (6, 3, 12, 4, 1173)
    )),
])
def test_get_result_from_image_path(image, expected):
    assert get_result(image) == expected


@pytest.mark.parametrize(("image", "expected"), [
    (cv2.imread(f'./screenshots/1.jpg'), "rainmaker"),
    (cv2.imread(f'./screenshots/6.jpg'), "zone"),
    (cv2.imread(f'./screenshots/7.jpg'), "rainmaker"),
    (cv2.imread(f'./screenshots/9.jpg'), "tower"),
])
def test_get_rule_name(image, expected):
    assert get_rule_name(image) == expected
