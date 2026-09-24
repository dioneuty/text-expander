from pynput.keyboard import Key

from src.buffer_chars import is_buffer_char

EXPANSION_TRIGGER_CHARS = {".", ",", "!", "?"}


def _has_trigger_boundary(buffer: str, trigger: str) -> bool:
    """트리거 직전이 버퍼 문자가 아니면 독립 트리거로 간주 (예: sd에서 d 단독 매칭 방지)."""
    if buffer == trigger:
        return True
    prefix_len = len(buffer) - len(trigger)
    if prefix_len <= 0:
        return False
    return not is_buffer_char(buffer[prefix_len - 1])


def match_scope_for_expansion(text: str, key: Key | None = None, trigger_char: str | None = None) -> str:
    """입력창 전체 텍스트에서 현재 줄 suffix만 추출 (다중 줄 누적 방지)."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")

    if key == Key.enter:
        normalized = normalized.rstrip("\n")
    elif trigger_char == " ":
        normalized = normalized.rsplit("\n", 1)[-1].rstrip(" ")
    elif trigger_char and trigger_char in EXPANSION_TRIGGER_CHARS:
        line = normalized.rsplit("\n", 1)[-1]
        if line.endswith(trigger_char):
            line = line[: -len(trigger_char)]
        return line

    line = normalized.rsplit("\n", 1)[-1] if normalized else ""
    if trigger_char and line.endswith(trigger_char):
        line = line[: -len(trigger_char)]
    return line.rstrip()


def find_expansion(
    buffer: str, shortcuts: dict[str, str]
) -> tuple[str, str] | None:
    """buffer suffix가 트리거와 일치하면 (trigger, expansion) 반환."""
    if not buffer or not shortcuts:
        return None

    matches: list[tuple[str, str]] = []
    for trigger, expansion in shortcuts.items():
        if buffer.endswith(trigger):
            matches.append((trigger, expansion))

    if not matches:
        return None

    trigger, expansion = max(matches, key=lambda item: len(item[0]))
    return trigger, expansion


def find_immediate_expansion(
    buffer: str, shortcuts: dict[str, str]
) -> tuple[str, str] | None:
    """트리거 입력 완료 시 즉시 확장할 매칭을 반환."""
    return find_expansion(buffer, shortcuts)
