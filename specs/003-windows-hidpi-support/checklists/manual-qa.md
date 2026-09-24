# Manual QA: Windows HiDPI 표시 지원

**Feature**: 003-windows-hidpi-support  
**Reference**: [quickstart.md](../quickstart.md)  
**Date**: 2026-09-24

| ID | Scenario | Scale | Expected | Status |
|----|----------|-------|----------|--------|
| M1 | Main window readable, not blurry | 150% | SC-001 | **PASS** (user verified after font/DPI fixes) |
| M2 | Main window no horizontal scroll | 200% | SC-002 | **PASS** (user verified) |
| M3 | Add dialog save flow | 150%+ | SC-003 | **PASS** (user verified) |
| M4 | exe vs source visual parity | 150% | SC-004 | **PASS** (user verified) |
| M5 | 100% regression CRUD + service | 100% | SC-005 | **PASS** (user verified) |
| M6 | Mixed DPI restart | dual monitor | FR-008 | **PASS** (user verified) |
| M7 | 125% scale sweep | 125% | Edge case | **PASS** (user verified) |

## Automated / Static

| ID | Check | Status |
|----|-------|--------|
| A1 | `pytest tests/unit/test_dpi_scaling.py` | **PASS** (26/26 unit suite, 2026-09-24) |
| A2 | `assets/app.manifest` PerMonitorV2 embedded in exe | **PASS** (`build.bat` log: Embedding manifest in EXE) |
| A3 | `enable_dpi_awareness()` before `Tk()` in `main.py` | PASS (static) |
| A4 | FR-005 — no Hook/settings logic changes | PASS (static) |
| A5 | `build.bat` on venv with `requirements-dev.txt` | **PASS** (pyinstaller 6.22.3, exe built) |

## Sign-off

- [x] Scenarios M1–M5, M7 verified on Windows HiDPI display
- [x] Scenario M4 verified after `build.bat` (build + manifest embed)
- [x] Full unit suite green
