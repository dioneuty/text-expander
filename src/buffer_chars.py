"""InputBuffer에 허용되는 문자 판별."""


def is_buffer_char(char: str) -> bool:
    """트리거 매칭 버퍼에 append 가능한 단일 ASCII printable 문자인지 반환."""
    return (
        len(char) == 1
        and char.isascii()
        and char.isprintable()
        and not char.isspace()
    )


def is_valid_trigger(trigger: str) -> bool:
    """등록 가능한 트리거 문자열인지 반환 (영문·숫자·ASCII 기호, 공백·한글 불가)."""
    return bool(trigger) and all(is_buffer_char(char) for char in trigger)
