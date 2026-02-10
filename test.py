import os
import shutil
import pytest

try:
    import cv2
except ModuleNotFoundError:
    cv2 = None

HAS_CV2 = cv2 is not None
HAS_TESSERACT = bool(
    os.getenv("TESSERACT_CMD")
    or os.getenv("TESSERACT_DIR")
    or shutil.which("tesseract")
)

if HAS_CV2:
    from modules.xp import get_xp
    from modules.results import get_result
    from modules.rule import get_rule_name
    from modules.player_position import get_my_position
    from modules.count import get_count
else:
    get_xp = None
    get_result = None
    get_rule_name = None
    get_my_position = None
    get_count = None


def _imread(path: str):
    if not HAS_CV2:
        return None
    return cv2.imread(path)


def _assert_result_close(actual, expected, splat_point_tolerance: int = 3):
    assert len(actual) == len(expected)
    for actual_row, expected_row in zip(actual, expected):
        assert actual_row[:4] == expected_row[:4]
        assert abs(actual_row[4] - expected_row[4]) <= splat_point_tolerance


@pytest.mark.parametrize(("image", "expected"), [
    (_imread(f'./screenshots/1.jpg'), 2368.9),
    (_imread(f'./screenshots/6.jpg'), 2099.0),
    (_imread(f'./screenshots/7.jpg'), 2288.9),
    (_imread(f'./screenshots/9.jpg'), 2255.2),
])
@pytest.mark.skipif(not HAS_CV2, reason="cv2 is not available in this environment.")
@pytest.mark.skipif(
    not HAS_TESSERACT,
    reason="tesseract command is not available in this environment.",
)
def test_get_xp(image, expected):
    assert get_xp(image) == expected


@pytest.mark.parametrize(("image", "expected"), [
    (_imread('./screenshots/1.jpg'), (
        (12, 5, 8, 4, 1335),
        (14, 2, 9, 2, 1020),
        (8, 3, 6, 6, 1562),
        (13, 6, 8, 3, 1051),
        (14, 2, 8, 5, 1232),
        (13, 6, 8, 3, 980),
        (9, 4, 8, 4, 1204),
        (8, 1, 7, 6, 1465)
    )),
    (_imread('./screenshots/2.jpg'), (
        (11, 3, 4, 5, 1541),
        (15, 3, 7, 4, 1294),
        (15, 5, 9, 2, 822),
        (11, 5, 10, 2, 1270),
        (15, 1, 9, 4, 1425),
        (8, 5, 9, 3, 1365),
        (9, 1, 8, 3, 1415),
        (7, 2, 10, 0, 508)
    )),
    (_imread('./screenshots/3.jpg'), (
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
@pytest.mark.skipif(not HAS_CV2, reason="cv2 is not available in this environment.")
@pytest.mark.skipif(
    not HAS_TESSERACT,
    reason="tesseract command is not available in this environment.",
)
def test_get_result_from_image_path(image, expected):
    _assert_result_close(get_result(image), expected)


@pytest.mark.parametrize(("image", "expected"), [
    (_imread(f'./screenshots/1.jpg'), "rainmaker"),
    (_imread(f'./screenshots/6.jpg'), "zone"),
    (_imread(f'./screenshots/7.jpg'), "rainmaker"),
    (_imread(f'./screenshots/9.jpg'), "tower"),
])
@pytest.mark.skipif(not HAS_CV2, reason="cv2 is not available in this environment.")
def test_get_rule_name(image, expected):
    assert get_rule_name(image) == expected


@pytest.mark.parametrize(("image", "expected"), [
    (_imread('./screenshots/1.jpg'), 4),
    (_imread('./screenshots/2.jpg'), 2),
    (_imread('./screenshots/6.jpg'), 3),
    (_imread('./screenshots/7.jpg'), 5),
    (_imread('./screenshots/9.jpg'), 1),
])
@pytest.mark.skipif(not HAS_CV2, reason="cv2 is not available in this environment.")
def test_get_my_position(image, expected):
    assert get_my_position(image) == expected


@pytest.mark.parametrize(("image"), [
    _imread('./screenshots/1.jpg'),
    _imread('./screenshots/6.jpg'),
    _imread('./screenshots/9.jpg'),
])
@pytest.mark.skipif(not HAS_CV2, reason="cv2 is not available in this environment.")
def test_get_count_shape(image):
    count = get_count(image)
    assert set(count.keys()) == {"left", "right"}
    assert count["left"] is None or isinstance(count["left"], int)
    assert count["right"] is None or isinstance(count["right"], int)
