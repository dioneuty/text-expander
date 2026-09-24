# Tasks: Windows HiDPI 표시 지원

**Input**: Design documents from `/specs/003-windows-hidpi-support/`  
**Prerequisites**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Plan includes unit tests for scale math (`test_dpi_scaling.py`); manual QA per quickstart.md.

**Organization**: Tasks grouped by user story for independent implementation and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1–US4)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare assets and feature checklist scaffolding

- [x] T001 Create `assets/` directory for Windows manifest per `specs/003-windows-hidpi-support/contracts/pyinstaller-manifest.md`
- [x] T002 Create `specs/003-windows-hidpi-support/checklists/manual-qa.md` template mapping SC-001~SC-005 to quickstart scenarios

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: DPI module, bootstrap order, unit tests — **MUST complete before user stories**

**⚠️ CRITICAL**: No user story work until this phase is complete

- [x] T003 Implement `enable_dpi_awareness()` in `src/gui/dpi.py` per `contracts/dpi-bootstrap.md` (SetProcessDpiAwareness(2) with fallback)
- [x] T004 Implement `UiScaleContext` and `get_ui_scale_context()` in `src/gui/dpi.py` per `data-model.md` (`scale_factor` clamp `[1.0, 3.0]`, `dpi/96` base)
- [x] T005 Implement `scale_geometry()` and `scale_int()` in `src/gui/dpi.py` per `data-model.md` WindowGeometry and LayoutTokens
- [x] T006 [P] Implement `configure_ui_fonts(root, context)` in `src/gui/dpi.py` per `contracts/dpi-bootstrap.md` (ttk Style, pixel fonts, `tk scaling`; keep `apply_tk_scaling` as deprecated)
- [x] T007 Call `enable_dpi_awareness()` before `Application()` in `main.py` per `contracts/dpi-bootstrap.md` call order
- [x] T008 Add `tests/unit/test_dpi_scaling.py` for `scale_geometry`/`scale_int` at factors 1.0, 1.25, 1.5, 2.0 per `research.md` R7

**Checkpoint**: `pytest tests/unit/test_dpi_scaling.py` passes; DPI bootstrap callable from `main.py`

---

## Phase 3: User Story 1 — 고배율 메인 화면 가독성 (Priority: P1) 🎯 MVP

**Goal**: Main window sharp and readable at 125/150/200% with scaled default geometry (FR-001, FR-002, FR-007)

**Independent Test**: quickstart Scenario 1–2, 5 @ 100/150/200% — info labels, tree, buttons, settings visible and not blurry

### Implementation for User Story 1

- [x] T009 [US1] Load `UiScaleContext`, call `configure_ui_fonts()`, pass context to `MainWindow` in `src/gui/app.py`
- [x] T010 [US1] Apply scaled `geometry` 720×540 and `minsize` 560×420 in `src/gui/main_window.py` per `contracts/gui-window-scaling.md`
- [x] T011 [US1] Scale info label `wraplength` 680 and frame `padding` 12 in `src/gui/main_window.py` per `data-model.md` LayoutTokens
- [x] T012 [US1] Assert `scale_factor == 1.0` yields identical geometry strings as pre-feature in `tests/unit/test_dpi_scaling.py` per FR-006

**Checkpoint**: US1 complete — main window usable at 150% and 200% without horizontal scroll (SC-002 at 200%)

---

## Phase 4: User Story 2 — 단축어 대화상자 사용성 (Priority: P1)

**Goal**: Add/Edit dialog scaled proportionally; all fields visible at 150%+ (FR-003, FR-009)

**Independent Test**: quickstart Scenario 3 — open Add dialog @150%, save shortcut in <3 min without layout workarounds

### Implementation for User Story 2

- [x] T013 [US2] Set scaled dialog `geometry` 480×420 and `minsize` 400×360 in `src/gui/main_window.py` `_show_edit_dialog` per `contracts/gui-window-scaling.md`
- [x] T014 [US2] Scale dialog frame `padding` 12, Entry `width` 40, Text `width` 40 `height` 8 in `src/gui/main_window.py` per `data-model.md` LayoutTokens

**Checkpoint**: US2 complete — Add/Edit dialog fully usable at 150% and 200%

---

## Phase 5: User Story 3 — exe HiDPI 동등 품질 (Priority: P2)

**Goal**: PyInstaller exe matches `python main.py` visual quality (FR-004, SC-004)

**Independent Test**: quickstart Scenario 4 @150% — no obvious size/sharpness difference between source and exe

### Implementation for User Story 3

- [x] T015 [P] [US3] Create `assets/app.manifest` with `dpiAware` and `PerMonitorV2` per `contracts/pyinstaller-manifest.md`
- [x] T016 [US3] Add `manifest='assets/app.manifest'` to `EXE(...)` in `build.spec` per `contracts/pyinstaller-manifest.md`
- [x] T017 [US3] Run `build.bat`, verify `dist/단축어프로그램.exe` at 150% per `quickstart.md` Scenario 4

**Checkpoint**: US3 complete — exe not blurry vs source run

---

## Phase 6: User Story 4 — 혼합 DPI best-effort (Priority: P3)

**Goal**: Document and validate restart-after-move behavior (FR-008)

**Independent Test**: quickstart Scenario 6 — move window cross-monitor, restart, FR-001~003 pass on target monitor

### Implementation for User Story 4

- [x] T018 [US4] Document mixed-DPI restart expectation in `README.md` per spec Clarifications and FR-008
- [x] T019 [US4] Execute `quickstart.md` Scenario 6 if dual-monitor available; record PASS/SKIP in `specs/003-windows-hidpi-support/checklists/manual-qa.md`

**Checkpoint**: US4 complete — restart path documented; manual result recorded

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Docs, Memory Bank, full regression

- [x] T020 [P] Add HiDPI section to `README.md` (supported scales 125/150/200%, restart after scale/monitor change)
- [x] T021 Update `.cursor/rules/activeContext.md` and `.cursor/rules/progress.md` for 003-windows-hidpi-support completion
- [x] T022 Run full `pytest tests/unit` and confirm no regressions in existing 002 tests per plan verification checklist
- [x] T023 Execute `quickstart.md` Scenarios 1–5 and 7; record results in `specs/003-windows-hidpi-support/checklists/manual-qa.md`
- [x] T024 Confirm KeyboardHook, `settings.json`, CRUD unchanged per FR-005 regression guard in `spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1 — **blocks all user stories**
- **US1 (Phase 3)**: Depends on Phase 2
- **US2 (Phase 4)**: Depends on Phase 2; shares `main_window.py` with US1 — **sequential after T010–T011 recommended**
- **US3 (Phase 5)**: Depends on Phase 2 only for manifest; can parallel with US1/US2 if different assignee (T015 [P] vs main_window work)
- **US4 (Phase 6)**: Depends on US1–US3 for meaningful validation
- **Polish (Phase 7)**: Depends on desired user stories complete

### User Story Dependencies

| Story | Depends on | Notes |
|-------|------------|-------|
| US1 | Foundational | MVP — main window only |
| US2 | Foundational, US1 layout pass | Same file `main_window.py` |
| US3 | Foundational | Independent files `assets/`, `build.spec` |
| US4 | US1–US3 | Documentation + optional manual |

### Parallel Opportunities

- **Phase 2**: T006 [P] parallel with T003–T005 after T005's module exists
- **Phase 5**: T015 [P] parallel while US1/US2 in progress (different files)
- **Phase 7**: T020 [P] parallel with T021

### Parallel Example: After Phase 2

```text
Developer A: T009 → T010 → T011 → T012 (US1)
Developer B: T015 → T016 (US3 manifest, no main_window conflict)
Then: T013 → T014 (US2 dialog, after US1 geometry landed)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 Setup
2. Phase 2 Foundational (**critical**)
3. Phase 3 US1
4. **STOP and VALIDATE**: quickstart Scenarios 1, 2, 5 @ 150%

### Incremental Delivery

1. Setup + Foundational → dpi module ready
2. US1 → main window HiDPI (**MVP**)
3. US2 → dialog HiDPI
4. US3 → exe manifest
5. US4 + Polish → docs, full QA

---

## Notes

- Do **not** modify `src/keyboard_hook.py`, `src/injector.py`, `src/settings.py` except import-neutral incidental changes (FR-005)
- `@ 100%` (`scale_factor == 1.0`) MUST match pre-feature layout (FR-006)
- Mixed DPI live move may look wrong until restart — expected per FR-008
- Commit after each phase checkpoint

---

## Phase 8: Convergence

- [x] T025 Execute `quickstart.md` Scenarios 1–5 and 7 on Windows; record PASS/FAIL for M1–M5 and M7 in `specs/003-windows-hidpi-support/checklists/manual-qa.md` per SC-001~SC-005
- [x] T026 Add `pyinstaller` to `requirements-dev.txt` so `build.bat` succeeds on a fresh venv per FR-004 and `contracts/pyinstaller-manifest.md`
