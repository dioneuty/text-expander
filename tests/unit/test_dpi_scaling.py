from src.gui.dpi import (
    DIALOG_DEFAULT_SIZE,
    DIALOG_MIN_SIZE,
    MAIN_DEFAULT_SIZE,
    MAIN_MIN_SIZE,
    geometry_string,
    scale_geometry,
    scale_int,
    font_pixel_size,
    ui_font,
)


def test_scale_geometry_at_100_percent() -> None:
    assert scale_geometry(*MAIN_DEFAULT_SIZE, 1.0) == MAIN_DEFAULT_SIZE
    assert scale_geometry(*MAIN_MIN_SIZE, 1.0) == MAIN_MIN_SIZE


def test_scale_geometry_at_150_percent() -> None:
    assert scale_geometry(720, 540, 1.5) == (1080, 810)
    assert scale_geometry(560, 420, 1.5) == (840, 630)


def test_scale_geometry_at_200_percent() -> None:
    assert scale_geometry(720, 540, 2.0) == (1440, 1080)


def test_scale_geometry_at_125_percent() -> None:
    assert scale_geometry(720, 540, 1.25) == (900, 675)


def test_scale_int_wraplength() -> None:
    assert scale_int(680, 1.0) == 680
    assert scale_int(680, 1.5) == 1020
    assert scale_int(12, 2.0) == 24


def test_font_pixel_size_matches_pt_at_dpi() -> None:
    assert font_pixel_size(96) == 12
    assert font_pixel_size(144) == 18
    assert font_pixel_size(192) == 24


def test_ui_font_uses_negative_pixel_size() -> None:
    family, size = ui_font(144, family="Malgun Gothic")
    assert size == -18
    assert family == "Malgun Gothic"


def test_geometry_string_matches_pre_feature_at_100_percent() -> None:
    assert geometry_string(720, 540, 1.0) == "720x540"
    assert geometry_string(560, 420, 1.0) == "560x420"
    assert geometry_string(*DIALOG_DEFAULT_SIZE, 1.0) == "480x420"
    assert geometry_string(*DIALOG_MIN_SIZE, 1.0) == "400x360"
