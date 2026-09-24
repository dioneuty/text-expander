from unittest.mock import MagicMock

from pynput.keyboard import Key, KeyCode

from src.keyboard_hook import KeyboardHook
from src.settings import ExpansionSettings


def _char_key(char: str) -> KeyCode:
    return KeyCode.from_char(char)


def test_immediate_mode_expands_on_last_trigger_char() -> None:
    injector = MagicMock()
    hook = KeyboardHook(
        {"sd": "hello"},
        settings=ExpansionSettings(mode="immediate"),
        injector=injector,
    )

    hook._on_press(_char_key("s"))
    hook._on_press(_char_key("d"))

    injector.replace_trigger.assert_called_once_with("sd", "hello", 0)


def test_immediate_mode_does_not_expand_on_partial_match() -> None:
    injector = MagicMock()
    hook = KeyboardHook(
        {"addr": "x"},
        settings=ExpansionSettings(mode="immediate"),
        injector=injector,
    )

    hook._on_press(_char_key("a"))
    hook._on_press(_char_key("d"))
    hook._on_press(_char_key("d"))

    injector.replace_trigger.assert_not_called()


def test_on_key_mode_waits_for_expansion_key() -> None:
    injector = MagicMock()
    hook = KeyboardHook(
        {"sd": "hello"},
        settings=ExpansionSettings(mode="on_key", expansion_key="space"),
        injector=injector,
    )

    hook._on_press(_char_key("s"))
    hook._on_press(_char_key("d"))
    injector.replace_trigger.assert_not_called()

    hook._on_press(Key.space)
    injector.replace_trigger.assert_called_once_with("sd", "hello", 1)


def test_on_key_mode_ignores_non_configured_whitespace() -> None:
    injector = MagicMock()
    hook = KeyboardHook(
        {"sd": "hello"},
        settings=ExpansionSettings(mode="on_key", expansion_key="space"),
        injector=injector,
    )

    hook._on_press(_char_key("s"))
    hook._on_press(_char_key("d"))
    hook._on_press(Key.enter)

    injector.replace_trigger.assert_not_called()
    assert hook._buffer.endswith("\n") or "d" in hook._buffer


def test_immediate_mode_does_not_expand_on_space_after_match() -> None:
    injector = MagicMock()
    hook = KeyboardHook(
        {"sd": "hello"},
        settings=ExpansionSettings(mode="immediate"),
        injector=injector,
    )

    hook._on_press(_char_key("s"))
    hook._on_press(_char_key("d"))
    injector.reset_mock()

    hook._on_press(Key.space)

    injector.replace_trigger.assert_not_called()
