# Contract: DPI Bootstrap

**Modules**: `main.py`, `src/gui/dpi.py`, `src/gui/app.py`  
**Feature**: 003-windows-hidpi-support

## Call Order (MUST)

1. `enable_dpi_awareness()` — **before** `tk.Tk()`
2. `context = get_ui_scale_context()` — may run before or after Tk; if Tk exists, may refine via `winfo_fpixels`
3. `root = tk.Tk()`
4. `apply_tk_scaling(root, context.scale_factor)`
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

## `apply_tk_scaling(root, factor: float)`

- Invokes `root.tk.call('tk', 'scaling', factor)`
- Called once per root at startup

---

## Regression

- Must not import or modify `KeyboardHook`, `ShortcutService`, `SettingsRepository` behavior
- `main.py --debug` path unchanged except earlier DPI call
