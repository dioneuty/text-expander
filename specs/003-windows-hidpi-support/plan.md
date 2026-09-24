# Implementation Plan: Windows HiDPI 표시 지원

**Branch**: `003-windows-hidpi-support` | **Date**: 2026-09-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-windows-hidpi-support/spec.md`

## Summary

Windows **125/150/200%** 디스플레이 배율에서 tkinter GUI(메인 창·단축어 대화상자)가 **선명하고 적절한 크기**로 표시되도록 한다. **DPI awareness**를 프로세스·exe manifest에 선언하고, **100% 기준 geometry(720×540 등)를 scale factor로 확대**한다. 전역 키보드 확장·JSON 설정 동작은 변경하지 않는다.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: tkinter (stdlib), ctypes (Win DPI API), pynput (unchanged)  
**Storage**: N/A — 새 영속 필드 없음  
**Testing**: pytest (`test_dpi_scaling.py`), manual per [quickstart.md](./quickstart.md)  
**Target Platform**: Windows 10/11  
**Project Type**: Desktop utility (single package)  
**Performance Goals**: GUI startup 지연 체감 없음 (DPI 조회 1회)  
**Constraints**: `enable_dpi_awareness()` before `tk.Tk()`; GUI↔Hook 스레드 분리 유지  
**Scale/Scope**: 메인 창 + CRUD 대화상자 + PyInstaller exe manifest

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Windows 전역 확장 | ✅ PASS | KeyboardHook/injector 미변경 (FR-005) |
| II. 자유 트리거 | ✅ PASS | 영향 없음 |
| III. 레이어 분리 | ✅ PASS | `src/gui/dpi.py` — GUI 전용 |
| IV. 영속 저장 | ✅ PASS | shortcuts/settings 스키마 불변 |
| V. 단순함 | ✅ PASS | 단일 dpi 모듈, manifest 1파일 |
| tkinter GUI | ✅ PASS | 기존 프레임워크 유지 |
| 한국어 UI | ✅ PASS | copy 변경 없음 |

**Post-design re-check**: ✅ All gates pass. No constitution amendment required.

## Project Structure

### Documentation (this feature)

```text
specs/003-windows-hidpi-support/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/
│   ├── dpi-bootstrap.md
│   ├── gui-window-scaling.md
│   └── pyinstaller-manifest.md
└── tasks.md             # /speckit-tasks (next)
```

### Source Code (repository root)

```text
단축어 프로그램/
├── main.py                    # MODIFY — earliest enable_dpi_awareness()
├── assets/
│   └── app.manifest           # NEW — PerMonitorV2
├── build.spec                 # MODIFY — manifest=
├── src/
│   └── gui/
│       ├── dpi.py             # NEW — awareness, scale, geometry helpers
│       ├── app.py             # MODIFY — scaling apply, pass context
│       └── main_window.py     # MODIFY — scaled geometry, dialog size
└── tests/unit/
    └── test_dpi_scaling.py    # NEW
```

**Structure Decision**: HiDPI 로직을 `src/gui/dpi.py`에 집중. Hook/Service 레이어 비침투.

## Complexity Tracking

> Constitution violation 없음 — Complexity Tracking 비움.

---

## Implementation Phases

### Phase A — DPI module & bootstrap (FR-001 foundation)

| Task | File | Action |
|------|------|--------|
| A1 | `src/gui/dpi.py` | `enable_dpi_awareness`, `get_ui_scale_context`, `scale_geometry`, `scale_int`, `apply_tk_scaling` |
| A2 | `main.py` | Call `enable_dpi_awareness()` before `Application()` |
| A3 | `tests/unit/test_dpi_scaling.py` | Unit tests for scale math @ 1.0, 1.25, 1.5, 2.0 |

**Contract**: [dpi-bootstrap.md](./contracts/dpi-bootstrap.md)

### Phase B — Main window scaling (User Story 1, FR-002, FR-007)

| Task | File | Action |
|------|------|--------|
| B1 | `src/gui/app.py` | Load context, `apply_tk_scaling`, pass to `MainWindow` |
| B2 | `src/gui/main_window.py` | Scaled `geometry`, `minsize`, `wraplength`, frame padding |
| B3 | Manual | quickstart Scenario 1–2, 5 @ 100/150/200% |

**Contract**: [gui-window-scaling.md](./contracts/gui-window-scaling.md)

### Phase C — Dialog scaling (User Story 2, FR-003, FR-009)

| Task | File | Action |
|------|------|--------|
| C1 | `src/gui/main_window.py` | Dialog `geometry` 480×420 base, scaled minsize, widget widths |
| C2 | Manual | quickstart Scenario 3 |

### Phase D — exe manifest (User Story 3, FR-004)

| Task | File | Action |
|------|------|--------|
| D1 | `assets/app.manifest` | PerMonitorV2 manifest |
| D2 | `build.spec` | `manifest='assets/app.manifest'` |
| D3 | Manual | `build.bat` → Scenario 4 |

**Contract**: [pyinstaller-manifest.md](./contracts/pyinstaller-manifest.md)

### Phase E — Docs & Memory Bank

| Task | File | Action |
|------|------|--------|
| E1 | `README.md` | HiDPI 지원·권장 배율·재시작 안내 1단락 |
| E2 | `.cursor/rules/activeContext.md`, `progress.md` | Feature 완료 시 갱신 |

---

## Risk & Mitigation

| Risk | Mitigation |
|------|------------|
| tk scaling + geometry double-scale | @100% regression (SC-005); factor 1.0 identity tests |
| ctypes API unavailable | Fallback 1.0 + System DPI aware legacy |
| Dialog too small @200% | Explicit dialog baseline 480×420 + scaled minsize |
| Mixed DPI live wrong | Document restart (FR-008); no WM_DPICHANGED v1 |

---

## Verification Checklist (pre-merge)

- [ ] `pytest tests/unit` all pass
- [ ] quickstart Scenarios 1–5 (mandatory)
- [ ] Scenario 4 exe parity @150%
- [ ] Scenario 6 mixed DPI restart (if hardware available)
- [ ] 002 regression: expansion modes, CRUD, settings save

---

## Next Command

`/speckit-tasks` — 위 Phase A–E를 dependency-ordered tasks.md로 분해
