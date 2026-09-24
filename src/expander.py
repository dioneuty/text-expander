EXPANSION_TRIGGER_CHARS = {".", ",", "!", "?"}


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
