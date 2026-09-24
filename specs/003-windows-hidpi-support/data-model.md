# Data Model: Windows HiDPI 표시 지원

**Feature**: 003-windows-hidpi-support

## Overview

HiDPI 기능은 **새 영속 JSON 필드 없음**. 런타임에 Windows 디스플레이 DPI에서 파생되는 **표시 컨텍스트**와 **100% 기준 레이아웃 상수**만 다룬다.

---

## Runtime Entities

### UiScaleContext

프로그램 시작 시 1회 계산(재시작 전 고정).

| Field | Type | Description |
|-------|------|-------------|
| `scale_factor` | `float` | 96 DPI 대비 배율 (1.0 = 100%, 1.5 = 150%) |
| `dpi` | `int` | 시스템(또는 primary) DPI, px per inch |
| `source` | `str` | `"win32_api"` \| `"tk_fallback"` \| `"default"` |

**Derivation**:
```
scale_factor = clamp(round(dpi / 96.0, 2), min=1.0, max=3.0)
```

**Lifecycle**: `enable_dpi_awareness()` → `get_ui_scale_context()` → `Application` / `MainWindow`에 전달. 실행 중 변경·저장 없음(FR-008).

---

### WindowGeometry (100% baseline → scaled)

| Surface | Field | 100% Value | Scaled |
|---------|-------|------------|--------|
| Main | `default_size` | `(720, 540)` | `(720*sf, 540*sf)` int |
| Main | `min_size` | `(560, 420)` | `(560*sf, 420*sf)` int |
| Dialog | `default_size` | `(480, 420)` | `(480*sf, 420*sf)` int |
| Dialog | `min_size` | `(400, 360)` | `(400*sf, 360*sf)` int |

`sf` = `scale_factor`.

**Validation**:
- Width/height ≥ min after scale
- Integer pixels only

---

### LayoutTokens (scaled integers)

| Token | 100% base | Usage |
|-------|-----------|-------|
| `padding` | `12` | ttk.Frame padding |
| `wraplength_info` | `680` | info label wraplength |
| `entry_width` | `40` | dialog Entry width (chars) |
| `text_width` | `40` | dialog Text width |
| `text_height` | `8` | dialog Text height (lines) |

Scaled: `max(1, int(base * scale_factor))` (wraplength/padding); char widths는 `max(base, int(base * scale_factor))`.

---

## Unchanged Persistent Entities

| Entity | File | Notes |
|--------|------|-------|
| `Shortcut` | `data/shortcuts.json` | 변경 없음 (FR-005) |
| `ExpansionSettings` | `data/settings.json` | 변경 없음 |

---

## Module Ownership

| Module | Responsibility |
|--------|----------------|
| `src/gui/dpi.py` | DPI awareness, scale context, geometry helpers |
| `src/gui/app.py` | bootstrap order, `tk scaling` |
| `src/gui/main_window.py` | apply scaled geometry/tokens |
| `main.py` | earliest `enable_dpi_awareness()` call |
| `assets/app.manifest` | exe DPI manifest |
| `build.spec` | manifest embed |

---

## State Diagram (startup)

```text
[Process start]
    → enable_dpi_awareness()
    → get_ui_scale_context()
    → tk.Tk()
    → tk scaling = scale_factor
    → MainWindow.apply_scale(context)
    → [GUI ready]
```

**No transitions** during runtime in v1 (restart required for DPI setting change).
