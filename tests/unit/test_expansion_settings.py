import json
from pathlib import Path

from src.settings import (
    DEFAULT_SETTINGS,
    ExpansionSettings,
    SettingsRepository,
)


def test_load_missing_file_returns_defaults(tmp_path: Path) -> None:
    repo = SettingsRepository(tmp_path / "settings.json")
    assert repo.load() == DEFAULT_SETTINGS


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    repo = SettingsRepository(path)
    settings = ExpansionSettings(mode="immediate", expansion_key="enter")
    repo.save(settings)

    loaded = repo.load()
    assert loaded == settings
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["expansion_mode"] == "immediate"
    assert data["expansion_key"] == "enter"


def test_load_invalid_enums_fall_back_to_defaults(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text(
        json.dumps({"version": 1, "expansion_mode": "bad", "expansion_key": "x"}),
        encoding="utf-8",
    )
    repo = SettingsRepository(path)
    assert repo.load() == DEFAULT_SETTINGS
