from src.buffer_chars import is_buffer_char


def test_ascii_buffer_chars_accepted() -> None:
    assert is_buffer_char("a")
    assert is_buffer_char("Z")
    assert is_buffer_char("9")
    assert is_buffer_char("_")


def test_ascii_whitespace_rejected() -> None:
    assert not is_buffer_char(" ")
    assert not is_buffer_char("\t")


def test_hangul_rejected() -> None:
    assert not is_buffer_char("회")
    assert not is_buffer_char("사")
    assert not is_buffer_char("명")


def test_non_ascii_unicode_rejected() -> None:
    assert not is_buffer_char("あ")
    assert not is_buffer_char("中")
