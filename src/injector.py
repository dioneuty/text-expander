import threading
import time

from pynput.keyboard import Controller, Key


class TextInjector:
    def __init__(self, delay: float = 0.03) -> None:
        self._controller = Controller()
        self._delay = delay

    def replace_trigger(self, trigger: str, expansion: str) -> None:
        threading.Thread(
            target=self._replace_trigger,
            args=(trigger, expansion),
            daemon=True,
            name="TextInjector",
        ).start()

    def _replace_trigger(self, trigger: str, expansion: str) -> None:
        # OS가 방금 입력한 글자를 화면에 반영할 시간을 줍니다.
        time.sleep(self._delay)

        for _ in range(len(trigger)):
            self._controller.press(Key.backspace)
            self._controller.release(Key.backspace)
            time.sleep(self._delay / 2)

        time.sleep(self._delay)
        if expansion:
            self._controller.type(expansion)
