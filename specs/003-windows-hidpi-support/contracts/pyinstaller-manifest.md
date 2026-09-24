# Contract: PyInstaller HiDPI Manifest

**Files**: `assets/app.manifest`, `build.spec`  
**Feature**: 003-windows-hidpi-support | **Requirement**: FR-004, SC-004

## Manifest Content

Application manifest MUST include:

```xml
<application xmlns="urn:schemas-microsoft-com:asm.v3">
  <windowsSettings>
    <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>
    <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
  </windowsSettings>
</application>
```

Embedded in assembly manifest (standard PyInstaller `manifest=` on `EXE`).

---

## build.spec

`EXE(..., manifest='assets/app.manifest', ...)` — path relative to project root.

---

## Verification

After `build.bat` / `pyinstaller build.spec`:

1. Run `dist/단축어프로그램.exe` on 150% display
2. Compare visually with `python main.py` (SC-004)
3. Text MUST NOT appear system-stretched blurry (bitmap upscale)

---

## Regression

- Existing `hiddenimports` unchanged
- `console=False` unchanged
- exe name `단축어프로그램` unchanged
