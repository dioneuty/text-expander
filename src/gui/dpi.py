"""Windows HiDPI support for tkinter GUI."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any

# 100% baseline layout (data-model.md)
MAIN_DEFAULT_SIZE = (720, 540)
MAIN_MIN_SIZE = (560, 420)
DIALOG_DEFAULT_SIZE = (480, 420)
DIALOG_MIN_SIZE = (400, 360)
BASE_PADDING = 12
BASE_SETTINGS_PADDING = 8
BASE_WRAPLENGTH = 680
BASE_ENTRY_WIDTH = 40
BASE_TEXT_WIDTH = 40
BASE_TEXT_HEIGHT = 8
BASE_TREE_TRIGGER_WIDTH = 160
BASE_TREE_EXPANSION_WIDTH = 480
BASE_FONT_SIZE = 9
BASE_TREE_ROW_HEIGHT = 24
# Prefer Malgun Gothic on Korean Windows — avoids Gulim (굴림) fallback from MS Shell Dlg.
_WIN_FONT_CANDIDATES = ("Malgun Gothic", "맑은 고딕", "Segoe UI")
_TK_NAMED_FONTS = (
    "TkDefaultFont",
    "TkTextFont",
    "TkFixedFont",
    "TkMenuFont",
    "TkHeadingFont",
    "TkCaptionFont",
)

PROCESS_PER_MONITOR_DPI_AWARE = 2


@dataclass(frozen=True)
class UiScaleContext:
    scale_factor: float
    dpi: int
    source: str


def enable_dpi_awareness() -> None:
    if sys.platform != "win32":
        return
    import ctypes

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


def _get_system_dpi() -> tuple[int, str]:
    if sys.platform != "win32":
        return 96, "default"
    import ctypes

    try:
        dpi = int(ctypes.windll.user32.GetDpiForSystem())
        if dpi > 0:
            return dpi, "win32_api"
    except (AttributeError, OSError):
        pass

    try:
        hdc = ctypes.windll.user32.GetDC(0)
        log_pixels_x = 88
        dpi = int(ctypes.windll.gdi32.GetDeviceCaps(hdc, log_pixels_x))
        ctypes.windll.user32.ReleaseDC(0, hdc)
        if dpi > 0:
            return dpi, "win32_api"
    except (AttributeError, OSError):
        pass

    return 96, "default"


def _clamp_scale_factor(factor: float) -> float:
    return round(max(1.0, min(3.0, factor)), 2)


def get_ui_scale_context(root: Any | None = None) -> UiScaleContext:
    dpi, source = _get_system_dpi()

    if root is not None:
        try:
            tk_dpi = float(root.winfo_fpixels("1i"))
            if tk_dpi > 0:
                dpi = int(round(tk_dpi))
                source = "tk_fallback"
        except Exception:
            pass

    factor = _clamp_scale_factor(dpi / 96.0)
    return UiScaleContext(scale_factor=factor, dpi=dpi, source=source)


def scale_geometry(width: int, height: int, factor: float) -> tuple[int, int]:
    f = max(1.0, factor)
    return int(width * f), int(height * f)


def scale_int(value: int, factor: float) -> int:
    f = max(1.0, factor)
    return max(1, int(value * f))


def geometry_string(width: int, height: int, factor: float) -> str:
    w, h = scale_geometry(width, height, factor)
    return f"{w}x{h}"


def font_pixel_size(dpi: int) -> int:
    """Pixel height for ``BASE_FONT_SIZE`` pt at the given DPI (no double scaling)."""
    return max(12, round(BASE_FONT_SIZE * dpi / 72.0))


def resolve_ui_font_family(root: Any) -> str:
    """Pick a modern UI font available on this system (not Gulim)."""
    if sys.platform != "win32":
        return "TkDefaultFont"

    import tkinter.font as tkfont

    available = {name.lower(): name for name in tkfont.families(root)}
    for candidate in _WIN_FONT_CANDIDATES:
        resolved = available.get(candidate.lower())
        if resolved is not None:
            return resolved
    return "Segoe UI"


def ui_font(dpi: int, family: str | None = None) -> tuple[str, int]:
    """Font tuple for tk/ttk; negative size = pixels."""
    if family is None:
        family = "Segoe UI" if sys.platform == "win32" else "TkDefaultFont"
    return family, -font_pixel_size(dpi)


def _configure_named_tk_fonts(family: str, pixel_size: int) -> None:
    import tkinter.font as tkfont

    for name in _TK_NAMED_FONTS:
        try:
            tkfont.nametofont(name).configure(family=family, size=-pixel_size)
        except Exception:
            pass


def _apply_ttk_theme(style: Any) -> None:
    if sys.platform != "win32":
        return
    # clam respects custom fonts; vista/winnative often keeps Gulim on Korean Windows.
    if "clam" in style.theme_names():
        style.theme_use("clam")


def configure_ui_fonts(root: Any, context: UiScaleContext) -> tuple[str, int]:
    """Apply HiDPI fonts to ttk/tk widgets.

    ttk on Windows ignores ``tk scaling``; use DPI-derived **pixel** fonts so
    9pt body text stays the same physical size at 100% and 150% (not 9×1.5 pt).
    """
    family = resolve_ui_font_family(root)
    pixel_size = font_pixel_size(context.dpi)
    family, font_size_px = ui_font(context.dpi, family=family)
    font = (family, font_size_px)
    _configure_named_tk_fonts(family, pixel_size)

    root.option_add("*Font", font)

    from tkinter import ttk

    style = ttk.Style(root)
    _apply_ttk_theme(style)
    heading_font = (family, font_size_px, "bold")

    for style_name in (
        ".",
        "TLabel",
        "TButton",
        "TRadiobutton",
        "TCheckbutton",
        "TCombobox",
        "TEntry",
        "TLabelframe",
        "TLabelframe.Label",
        "Treeview",
        "Treeview.Heading",
        "Treeview.Item",
    ):
        style.configure(style_name, font=font)

    style.configure(
        "Treeview",
        font=font,
        rowheight=scale_int(BASE_TREE_ROW_HEIGHT, context.scale_factor),
    )
    style.configure("Treeview.Heading", font=heading_font)

    root.tk.call("tk", "scaling", context.dpi / 72.0)

    return family, pixel_size


def apply_tk_scaling(root: Any, factor: float) -> None:
    """Deprecated: use configure_ui_fonts for full HiDPI text support."""
    root.tk.call("tk", "scaling", max(1.0, factor))
