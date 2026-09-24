from pathlib import Path

import pytest

from src.buffer_chars import is_valid_trigger
from src.repository import ShortcutRepository
from src.service import ShortcutService, ValidationError


def test_is_valid_trigger_ascii() -> None:
    assert is_valid_trigger("addr")
    assert is_valid_trigger("my-email_1")


def test_is_valid_trigger_rejects_hangul_and_space() -> None:
    assert not is_valid_trigger("회사")
    assert not is_valid_trigger("my addr")
    assert not is_valid_trigger("")


def test_service_rejects_hangul_trigger(tmp_path: Path) -> None:
    repo = ShortcutRepository(tmp_path / "shortcuts.json")
    service = ShortcutService(repo)
    service.load()

    with pytest.raises(ValidationError, match="한글"):
        service.add("회사서명", "hello")


def test_service_allows_legacy_hangul_trigger_on_update(tmp_path: Path) -> None:
    path = tmp_path / "shortcuts.json"
    path.write_text(
        '{"version": 1, "shortcuts": {"회사서명": "old"}}',
        encoding="utf-8",
    )
    service = ShortcutService(ShortcutRepository(path))
    service.load()

    service.update("회사서명", "회사서명", "new text")
    assert service.get_all()["회사서명"] == "new text"

    service.update("회사서명", "sig1", "new text")
    assert service.get_all()["sig1"] == "new text"

    with pytest.raises(ValidationError, match="한글"):
        service.update("sig1", "새한글", "new text")
