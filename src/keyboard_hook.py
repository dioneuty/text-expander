import threading

from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Listener

from src.expander import (
    EXPANSION_TRIGGER_CHARS,
    find_expansion,
    find_immediate_expansion,
)
from src.injector import TextInjector

BUFFER_MAX = 256

EXPANSION_KEYS = frozenset({Key.space, Key.enter, Key.tab})


def _is_buffer_char(char: str) -> bool:
    return (
        len(char) == 1
        and char.isascii()
        and char.isprintable()
        and not char.isspace()
    )


class KeyboardHook:
    def __init__(
        self,
        shortcuts: dict[str, str],
        injector: TextInjector | None = None,
    ) -> None:
        self._lock = threading.Lock()
        self._shortcuts = dict(shortcuts)
        self._buffer = ""
        self._enabled = True
        self._paused = False
        self._injector = injector or TextInjector()
        self._listener: Listener | None = None
        self._thread: threading.Thread | None = None
        self._error: str | None = None
        self._started = threading.Event()

    def start(self) -> None:
        def run() -> None:
            try:
                with Listener(on_press=self._on_press) as listener:
                    self._listener = listener
                    self._started.set()
                    listener.join()
            except Exception as exc:
                self._error = str(exc)
                self._started.set()

        self._thread = threading.Thread(target=run, daemon=True, name="KeyboardHook")
        self._thread.start()
        self._started.wait(timeout=2)

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
        if self._thread is not None:
            self._thread.join(timeout=2)

    def reload(self, shortcuts: dict[str, str]) -> None:
        with self._lock:
            self._shortcuts = dict(shortcuts)

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def set_paused(self, paused: bool) -> None:
        self._paused = paused

    def is_enabled(self) -> bool:
        return self._enabled

    def get_error(self) -> str | None:
        return self._error

    def _get_shortcuts(self) -> dict[str, str]:
        with self._lock:
            return dict(self._shortcuts)

    def _append_buffer(self, char: str) -> None:
        self._buffer = (self._buffer + char)[-BUFFER_MAX:]

    def _trim_buffer(self, count: int = 1) -> None:
        if count <= 0:
            return
        if count >= len(self._buffer):
            self._buffer = ""
        else:
            self._buffer = self._buffer[:-count]

    def _char_from_key(self, key: keyboard.Key | KeyCode) -> str | None:
        if key == Key.space:
            return " "
        if isinstance(key, KeyCode) and key.char:
            return key.char
        return None

    def _apply_expansion(self, trigger: str, expansion: str) -> None:
        self._trim_buffer(len(trigger))
        self._injector.replace_trigger(trigger, expansion)

    def _try_immediate_expansion(self) -> None:
        shortcuts = self._get_shortcuts()
        match = find_immediate_expansion(self._buffer, shortcuts)
        if match:
            trigger, expansion = match
            self._apply_expansion(trigger, expansion)

    def _on_press(self, key: keyboard.Key | KeyCode) -> None:
        if key == Key.backspace:
            self._trim_buffer(1)
            return

        if not self._enabled or self._paused:
            return

        char = self._char_from_key(key)
        is_expansion_key = key in EXPANSION_KEYS or (
            char is not None and char in EXPANSION_TRIGGER_CHARS
        )

        if is_expansion_key:
            shortcuts = self._get_shortcuts()
            match = find_expansion(self._buffer, shortcuts)
            if match:
                trigger, expansion = match
                self._apply_expansion(trigger, expansion)

            if char is not None:
                self._append_buffer(char)
            return

        if char and _is_buffer_char(char):
            self._append_buffer(char)
            self._try_immediate_expansion()
