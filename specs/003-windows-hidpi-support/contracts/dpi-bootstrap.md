# Contract: DPI Bootstrap

**Modules**: `main.py`, `src/gui/dpi.py`, `src/gui/app.py`  
**Feature**: 003-windows-hidpi-support

## Call Order (MUST)

1. `enable_dpi_awareness()` — **before** `tk.Tk()`
2. `context = get_ui_scale_context()` — may run before or after Tk; if Tk exists, may refine via `winfo_fpixels`
3. `root = tk.Tk()`
4. `configure_ui_fonts(root, context)` — ttk Style + named fonts + `tk scaling`
5. `MainWindow(..., scale_context=context)`

Violating order (Tk before awareness) is a **contract breach** — may cause blur on HiDPI.

---

## `enable_dpi_awareness()`

| Platform | Behavior |
|----------|----------|
| `win32` | Try `SetProcessDpiAwareness(2)`; fallback `SetProcessDPIAware()` |
| other | no-op |

Must not raise to caller; failures are silent (scale falls back to 1.0).

---

## `get_ui_scale_context() -> UiScaleContext`

| Field | Rule |
|-------|------|
| `scale_factor` | `dpi/96`, clamp `[1.0, 3.0]`, round 2 decimals |
| `dpi` | Win API or 96 default |
| `source` | documents which path succeeded |

---

## `configure_ui_fonts(root, context: UiScaleContext)`

- Resolves UI font family (`Malgun Gothic` → `맑은 고딕` → `Segoe UI` on Windows)
- Sets pixel font size from `font_pixel_size(context.dpi)` (9pt @ 96 DPI baseline)
- Configures ttk `Style` for all widget classes; uses `clam` theme on Windows
- Sets `root.option_add("*Font", ...)` and named Tk fonts
- Invokes `tk scaling = context.dpi / 72.0` (pt→px; **not** `scale_factor` again)

---

## `apply_tk_scaling(root, factor: float)` *(deprecated)*

- Legacy helper only; **do not** call from `Application` — use `configure_ui_fonts`
- Invokes `root.tk.call('tk', 'scaling', factor)`

---

## Regression

- Must not import or modify `KeyboardHook`, `ShortcutService`, `SettingsRepository` behavior
- `main.py --debug` path unchanged except earlier DPI call
