import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from src.gui import constants as C
from src.gui.main_window import MainWindow
from src.keyboard_hook import KeyboardHook
from src.paths import get_data_path
from src.repository import RepositoryError, ShortcutRepository
from src.service import ShortcutService


class Application:
    def __init__(self, data_path: Path | None = None) -> None:
        if data_path is None:
            data_path = get_data_path()

        self._repository = ShortcutRepository(data_path)
        self._hook: KeyboardHook | None = None
        self._service: ShortcutService | None = None
        self.root = tk.Tk()

    def run(self) -> None:
        self._service = ShortcutService(
            self._repository,
            on_change=self._on_shortcuts_changed,
        )
        try:
            self._service.load()
        except RepositoryError as exc:
            messagebox.showerror(C.APP_TITLE, f"{C.ERR_REPOSITORY}\n{exc}")

        self._hook = KeyboardHook(self._service.get_all())

        self._hook.start()
        if self._hook.get_error():
            messagebox.showwarning(C.APP_TITLE, C.ERR_HOOK_FAILED)

        self._main_window = MainWindow(self.root, self._service, self._hook)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_shortcuts_changed(self, shortcuts: dict[str, str]) -> None:
        if self._hook is not None:
            self._hook.reload(shortcuts)

    def _on_close(self) -> None:
        if self._hook is not None:
            self._hook.stop()
        self.root.destroy()
