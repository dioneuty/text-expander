import threading

from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Listener

from src.buffer_chars import is_buffer_char
from src.expander import find_expansion
from src.injector import TextInjector
from src.settings import ExpansionKey, ExpansionSettings

BUFFER_MAX = 256

EXPANSION_KEY_MAP: dict[ExpansionKey, Key] = {
    "space": Key.space,
    "enter": Key.enter,
    "tab": Key.tab,
}

# on_key 모드: 확장 키는 OS에 먼저 전달되므로 치환 시 추가 삭제 필요
EXPANSION_KEY_EXTRA_BACKSPACES: dict[ExpansionKey, int] = {
    "space": 1,
    "enter": 1,
    "tab": 1,
}


class KeyboardHook:
    def __init__(
        self,
        shortcuts: dict[str, str],
        settings: ExpansionSettings | None = None,
        injector: TextInjector | None = None,
    ) -> None:
        self._lock = threading.Lock()
        self._shortcuts = dict(shortcuts)
        self._settings = settings or ExpansionSettings()
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

    def set_settings(self, settings: ExpansionSettings) -> None:
        with self._lock:
            self._settings = settings

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

    def _get_settings(self) -> ExpansionSettings:
        with self._lock:
            return self._settings

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

    def _apply_expansion(
        self,
        trigger: str,
        expansion: str,
        *,
        extra_backspaces: int = 0,
    ) -> None:
        self._trim_buffer(len(trigger))
        self._injector.replace_trigger(trigger, expansion, extra_backspaces)

    def _try_immediate_expansion(self) -> None:
        shortcuts = self._get_shortcuts()
        match = find_expansion(self._buffer, shortcuts)
        if match:
            trigger, expansion = match
            self._apply_expansion(trigger, expansion)

    def _is_configured_expansion_key(self, key: keyboard.Key | KeyCode) -> bool:
        settings = self._get_settings()
        configured = EXPANSION_KEY_MAP.get(settings.expansion_key)
        return configured is not None and key == configured

    def _on_press(self, key: keyboard.Key | KeyCode) -> None:
        if key == Key.backspace:
            self._trim_buffer(1)
            return

        if not self._enabled or self._paused:
            return

        settings = self._get_settings()
        char = self._char_from_key(key)
        is_whitespace_key = key in EXPANSION_KEY_MAP.values()

        if settings.mode == "on_key" and self._is_configured_expansion_key(key):
            shortcuts = self._get_shortcuts()
            match = find_expansion(self._buffer, shortcuts)
            if match:
                trigger, expansion = match
                extra = EXPANSION_KEY_EXTRA_BACKSPACES.get(settings.expansion_key, 0)
                self._apply_expansion(trigger, expansion, extra_backspaces=extra)
            elif char is not None:
                self._append_buffer(char)
            return

        if char and is_buffer_char(char):
            self._append_buffer(char)
            if settings.mode == "immediate":
                self._try_immediate_expansion()
            return

        if char is not None and is_whitespace_key:
            self._append_buffer(char)
