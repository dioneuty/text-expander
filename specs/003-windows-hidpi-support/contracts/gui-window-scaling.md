# Contract: GUI Window Scaling

**Module**: `src/gui/main_window.py`, `src/gui/dpi.py`  
**Feature**: 003-windows-hidpi-support

## Main Window

**100% baseline** (FR-007):

| Property | Base @ 1.0 | Applied |
|----------|------------|---------|
| `geometry` | `720x540` | `scale_geometry(720, 540, sf)` |
| `minsize` | `560x420` | `scale_geometry(560, 420, sf)` |

**Scaled layout tokens**:
- Info labels `wraplength`: `scale_int(680, sf)`
- Frame `padding`: `scale_int(12, sf)`

At `scale_factor == 1.0`, pixel output MUST match pre-feature behavior (FR-006).

---

## Add/Edit Dialog (FR-009)

**100% baseline** (new explicit geometry):

| Property | Base @ 1.0 |
|----------|------------|
| `geometry` | `480x420` |
| `minsize` | `400x360` |

Dialog MUST set geometry after widgets packed/gridded (or use `update_idletasks()` before center).

**Scaled widgets**:
- `padding=12` → scaled
- Entry `width=40`, Text `width=40`, `height=8` → scaled char units per data-model

All fields (trigger, expansion, save/cancel) visible without clipping at 150% and 200% (FR-003).

---

## Helper Functions (`src/gui/dpi.py`)

```text
scale_geometry(w: int, h: int, factor: float) -> tuple[int, int]
scale_int(value: int, factor: float) -> int
```

- Results are positive integers
- `factor < 1.0` treated as `1.0`

---

## Out of Scope

- User-resized window persistence across sessions
- Live DPI change without restart
- System tray / unimplemented UI
