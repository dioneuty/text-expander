import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from src.buffer_chars import is_valid_trigger
from src.gui import constants as C
from src.keyboard_hook import KeyboardHook
from src.repository import RepositoryError
from src.service import ShortcutService, ValidationError
from src.settings import ExpansionSettings

PREVIEW_MAX = 30


class MainWindow:
    def __init__(
        self,
        root: tk.Tk,
        service: ShortcutService,
        hook: KeyboardHook,
        settings: ExpansionSettings,
        on_settings_save: Callable[[ExpansionSettings], None],
    ) -> None:
        self.root = root
        self.service = service
        self.hook = hook
        self._settings = settings
        self._on_settings_save = on_settings_save

        self._service_var = tk.BooleanVar(value=hook.is_enabled())
        self._status_var = tk.StringVar()
        self._mode_var = tk.StringVar(value=settings.mode)
        self._key_var = tk.StringVar(
            value=C.EXPANSION_KEY_LABELS[settings.expansion_key]
        )

        self._immediate_warning_label: ttk.Label | None = None
        self._key_combobox: ttk.Combobox | None = None

        self._build_ui()
        self._bind_events()
        self.refresh_list()
        self._update_status()
        self._update_mode_ui()

    def _build_ui(self) -> None:
        self.root.title(C.APP_TITLE)
        self.root.geometry("720x540")
        self.root.minsize(560, 420)

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        info_frame = ttk.Frame(main)
        info_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(info_frame, text=C.INFO_TRIGGER_TIP, wraplength=680).pack(
            anchor=tk.W
        )
        ttk.Label(info_frame, text=C.INFO_ENGLISH_ONLY, wraplength=680).pack(
            anchor=tk.W, pady=(4, 0)
        )

        self._immediate_warning_label = ttk.Label(
            info_frame,
            text=C.INFO_IMMEDIATE_MODE_WARNING,
            wraplength=680,
        )

        list_frame = ttk.Frame(main)
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("trigger", "expansion")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("trigger", text=C.COL_TRIGGER)
        self.tree.heading("expansion", text=C.COL_EXPANSION)
        self.tree.column("trigger", width=160, stretch=False)
        self.tree.column("expansion", width=480, stretch=True)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(8, 0))

        ttk.Button(btn_frame, text=C.BTN_ADD, command=self._on_add).pack(
            side=tk.LEFT
        )
        ttk.Button(btn_frame, text=C.BTN_EDIT, command=self._on_edit).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        ttk.Button(btn_frame, text=C.BTN_DELETE, command=self._on_delete).pack(
            side=tk.LEFT, padx=(8, 0)
        )

        settings_frame = ttk.LabelFrame(main, text=C.LBL_EXPANSION_MODE, padding=8)
        settings_frame.pack(fill=tk.X, pady=(12, 0))

        mode_row = ttk.Frame(settings_frame)
        mode_row.pack(fill=tk.X)

        ttk.Radiobutton(
            mode_row,
            text=C.MODE_IMMEDIATE,
            variable=self._mode_var,
            value="immediate",
            command=self._update_mode_ui,
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            mode_row,
            text=C.MODE_ON_KEY,
            variable=self._mode_var,
            value="on_key",
            command=self._update_mode_ui,
        ).pack(side=tk.LEFT, padx=(16, 0))

        key_row = ttk.Frame(settings_frame)
        key_row.pack(fill=tk.X, pady=(8, 0))

        ttk.Label(key_row, text=C.LBL_EXPANSION_KEY).pack(side=tk.LEFT)
        self._key_combobox = ttk.Combobox(
            key_row,
            textvariable=self._key_var,
            values=C.EXPANSION_KEY_COMBO_VALUES,
            state="readonly",
            width=12,
        )
        self._key_combobox.pack(side=tk.LEFT, padx=(8, 0))
        self._key_combobox.bind("<<ComboboxSelected>>", lambda _e: None)

        ttk.Button(
            key_row,
            text=C.BTN_SAVE_SETTINGS,
            command=self._on_save_settings,
        ).pack(side=tk.RIGHT)

        control_frame = ttk.Frame(main)
        control_frame.pack(fill=tk.X, pady=(12, 0))

        ttk.Checkbutton(
            control_frame,
            text=C.LBL_SERVICE,
            variable=self._service_var,
            command=self._on_toggle_service,
        ).pack(side=tk.LEFT)

        ttk.Label(control_frame, textvariable=self._status_var).pack(
            side=tk.RIGHT
        )

    def _bind_events(self) -> None:
        self.root.bind("<FocusIn>", self._on_focus_in)
        self.root.bind("<FocusOut>", self._on_focus_out)
        self.tree.bind("<Double-1>", lambda _event: self._on_edit())

    def _update_mode_ui(self) -> None:
        is_immediate = self._mode_var.get() == "immediate"
        if self._immediate_warning_label is not None:
            if is_immediate:
                self._immediate_warning_label.pack(anchor=tk.W, pady=(4, 0))
            else:
                self._immediate_warning_label.pack_forget()
        if self._key_combobox is not None:
            self._key_combobox.configure(
                state="disabled" if is_immediate else "readonly"
            )

    def _on_save_settings(self) -> None:
        expansion_key = C.EXPANSION_KEY_BY_LABEL[self._key_var.get()]
        settings = ExpansionSettings(
            mode=self._mode_var.get(),
            expansion_key=expansion_key,
        )
        self._settings = settings
        self._on_settings_save(settings)
        messagebox.showinfo(C.APP_TITLE, C.MSG_SETTINGS_SAVED)

    def _on_focus_in(self, _event: tk.Event) -> None:
        self.hook.set_paused(True)

    def _on_focus_out(self, _event: tk.Event) -> None:
        self.hook.set_paused(False)

    def _update_status(self) -> None:
        error = self.hook.get_error()
        if error:
            self._status_var.set(f"{C.LBL_STATUS_ERROR}: {error}")
            return

        if self._service_var.get():
            self._status_var.set(C.LBL_STATUS_RUNNING)
        else:
            self._status_var.set(C.LBL_STATUS_STOPPED)

    def _on_toggle_service(self) -> None:
        enabled = self._service_var.get()
        self.hook.set_enabled(enabled)
        self._update_status()

    def refresh_list(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for shortcut in self.service.list_all():
            preview = shortcut.expansion.replace("\n", " ")
            if len(preview) > PREVIEW_MAX:
                preview = preview[: PREVIEW_MAX - 3] + "..."
            self.tree.insert(
                "",
                tk.END,
                iid=shortcut.trigger,
                values=(shortcut.trigger, preview),
            )

    def _get_selected_trigger(self) -> str | None:
        selection = self.tree.selection()
        if not selection:
            return None
        return str(selection[0])

    def _on_add(self) -> None:
        self._open_dialog(C.DLG_ADD_TITLE)

    def _on_edit(self) -> None:
        trigger = self._get_selected_trigger()
        if not trigger:
            messagebox.showwarning(C.APP_TITLE, C.ERR_NO_SELECTION)
            return

        shortcuts = self.service.get_all()
        expansion = shortcuts.get(trigger, "")
        self._open_dialog(C.DLG_EDIT_TITLE, trigger, expansion)

    def _on_delete(self) -> None:
        trigger = self._get_selected_trigger()
        if not trigger:
            messagebox.showwarning(C.APP_TITLE, C.ERR_NO_SELECTION)
            return

        if not messagebox.askyesno(C.DLG_DELETE_TITLE, C.DLG_DELETE_CONFIRM):
            return

        try:
            self.service.remove(trigger)
        except ValidationError as exc:
            messagebox.showerror(C.APP_TITLE, str(exc))
            return
        except RepositoryError:
            messagebox.showerror(C.APP_TITLE, C.ERR_REPOSITORY)
            return

        self.hook.reload(self.service.get_all())
        self.refresh_list()
        messagebox.showinfo(C.APP_TITLE, C.MSG_DELETED)

    def _open_dialog(
        self,
        title: str,
        trigger: str = "",
        expansion: str = "",
    ) -> None:
        is_edit = bool(trigger)
        old_trigger = trigger

        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)

        self.hook.set_paused(True)

        frame = ttk.Frame(dialog, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=C.LBL_TRIGGER).grid(row=0, column=0, sticky=tk.W)
        trigger_entry = ttk.Entry(frame, width=40)
        trigger_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 4))
        trigger_entry.insert(0, trigger)

        def validate_trigger_input(proposed: str) -> bool:
            if not proposed:
                return True
            return is_valid_trigger(proposed)

        vcmd = (dialog.register(validate_trigger_input), "%P")
        trigger_entry.configure(validate="key", validatecommand=vcmd)

        ttk.Label(frame, text=C.INFO_TRIGGER_ENGLISH).grid(
            row=1, column=1, sticky=tk.W, pady=(0, 8)
        )

        ttk.Label(frame, text=C.LBL_EXPANSION).grid(row=2, column=0, sticky=tk.NW)
        expansion_text = tk.Text(frame, width=40, height=8, wrap=tk.WORD)
        expansion_text.grid(row=2, column=1, sticky=tk.NSEW)
        expansion_text.insert("1.0", expansion)

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)

        btn_row = ttk.Frame(frame)
        btn_row.grid(row=3, column=0, columnspan=2, sticky=tk.E, pady=(12, 0))

        def close_dialog() -> None:
            dialog.grab_release()
            dialog.destroy()
            if self.root.focus_get() is not None:
                self.hook.set_paused(True)
            else:
                self.hook.set_paused(False)

        def save() -> None:
            new_trigger = trigger_entry.get().strip()
            new_expansion = expansion_text.get("1.0", tk.END).strip()

            try:
                if is_edit:
                    self.service.update(old_trigger, new_trigger, new_expansion)
                else:
                    self.service.add(new_trigger, new_expansion)
            except ValidationError as exc:
                messagebox.showerror(C.APP_TITLE, str(exc), parent=dialog)
                return
            except RepositoryError:
                messagebox.showerror(C.APP_TITLE, C.ERR_REPOSITORY, parent=dialog)
                return

            self.hook.reload(self.service.get_all())
            self.refresh_list()
            close_dialog()
            messagebox.showinfo(C.APP_TITLE, C.MSG_SAVED)

        ttk.Button(btn_row, text=C.BTN_SAVE, command=save).pack(side=tk.LEFT)
        ttk.Button(btn_row, text=C.BTN_CANCEL, command=close_dialog).pack(
            side=tk.LEFT, padx=(8, 0)
        )

        trigger_entry.focus_set()
        dialog.protocol("WM_DELETE_WINDOW", close_dialog)
