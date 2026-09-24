import logging
import threading
import time

import pyperclip
from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

PASTE_THRESHOLD_LEN = 200


class TextInjector:
    def __init__(self, delay: float = 0.03) -> None:
        self._controller = Controller()
        self._delay = delay

    def replace_trigger(
        self,
        trigger: str,
        expansion: str,
        extra_backspaces: int = 0,
    ) -> None:
        threading.Thread(
            target=self._replace_trigger,
            args=(trigger, expansion, extra_backspaces),
            daemon=True,
            name="TextInjector",
        ).start()

    def _replace_trigger(
        self,
        trigger: str,
        expansion: str,
        extra_backspaces: int = 0,
    ) -> None:
        # OS가 방금 입력한 글자를 화면에 반영할 시간을 줍니다.
        time.sleep(self._delay)

        delete_count = len(trigger) + max(0, extra_backspaces)
        for _ in range(delete_count):
            self._controller.press(Key.backspace)
            self._controller.release(Key.backspace)
            time.sleep(self._delay / 2)

        time.sleep(self._delay)
        if expansion:
            self._insert_expansion(expansion)

    def _insert_expansion(self, expansion: str) -> None:
        use_paste = "\n" in expansion or len(expansion) > PASTE_THRESHOLD_LEN
        if not use_paste:
            self._controller.type(expansion)
            return

        previous: str | None = None
        try:
            previous = pyperclip.paste()
        except pyperclip.PyperclipException:
            logger.debug("clipboard read failed before paste", exc_info=True)

        try:
            pyperclip.copy(expansion)
            time.sleep(self._delay)
            with self._controller.pressed(Key.ctrl):
                self._controller.press("v")
                self._controller.release("v")
        except pyperclip.PyperclipException:
            logger.warning("clipboard paste failed; falling back to type()", exc_info=True)
            self._type_multiline_fallback(expansion)
        finally:
            if previous is not None:
                try:
                    time.sleep(self._delay)
                    pyperclip.copy(previous)
                except pyperclip.PyperclipException:
                    logger.debug("clipboard restore failed", exc_info=True)

    def _type_multiline_fallback(self, expansion: str) -> None:
        lines = expansion.split("\n")
        for index, line in enumerate(lines):
            if line:
                self._controller.type(line)
            if index < len(lines) - 1:
                self._controller.press(Key.enter)
                self._controller.release(Key.enter)
                time.sleep(self._delay / 2)
