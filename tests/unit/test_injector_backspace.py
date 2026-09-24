from unittest.mock import MagicMock, patch

from pynput.keyboard import Key

from src.injector import TextInjector


def _backspace_press_count(controller: MagicMock) -> int:
    return sum(
        1
        for call in controller.press.call_args_list
        if call.args and call.args[0] == Key.backspace
    )


@patch("src.injector.time.sleep")
def test_replace_trigger_deletes_trigger_only(_sleep: MagicMock) -> None:
    injector = TextInjector(delay=0)
    controller = MagicMock()
    injector._controller = controller

    injector._replace_trigger("sd", "hello", 0)

    assert _backspace_press_count(controller) == 2


@patch("src.injector.time.sleep")
def test_replace_trigger_includes_expansion_key_backspace(_sleep: MagicMock) -> None:
    injector = TextInjector(delay=0)
    controller = MagicMock()
    injector._controller = controller

    injector._replace_trigger("sd", "hello", 1)

    assert _backspace_press_count(controller) == 3
