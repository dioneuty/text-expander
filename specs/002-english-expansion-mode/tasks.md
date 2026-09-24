# Tasks: 영문 전용 안내 및 확장 모드 선택

**Feature**: 002-english-expansion-mode  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Phase 1: Settings & Model

- [x] T001 Create `ExpansionSettings` + `SettingsRepository` in `src/settings.py` per FR-008
- [x] T002 Wire settings path via `data/settings.json` in `src/gui/app.py`
- [x] T003 Add `tests/unit/test_expansion_settings.py` for load/save/defaults

## Phase 2: Hook & English-Only Buffer

- [x] T004 Restrict `is_buffer_char` to ASCII printable in `src/buffer_chars.py` per FR-009
- [x] T005 Add `is_valid_trigger` and service/GUI validation for trigger registration
- [x] T006 Implement expansion mode gating in `src/keyboard_hook.py` per FR-004, FR-005, FR-006
- [x] T007 Remove `ime_state.py`, `text_context.py` and related tests
- [x] T008 Fix on_key expansion key extra backspace in `src/injector.py` (US3/AC2)
- [x] T009 Update `tests/unit/test_buffer_char.py` and add `test_injector_backspace.py`

## Phase 3: GUI & Documentation

- [x] T010 Remove Korean IME copy; add English-only + mode warning in `src/gui/constants.py` per FR-001, FR-002, FR-010
- [x] T011 Add expansion mode settings UI in `src/gui/main_window.py` per FR-003, FR-011
- [x] T012 Load/save settings and hot-reload Hook in `src/gui/app.py`
- [x] T013 Update `README.md` per FR-001, FR-002

## Phase 4: Constitution & Memory Bank

- [x] T014 Update `.specify/memory/constitution.md` per plan Phase D1
- [x] T015 Update `.cursor/rules/systemPatterns.md`, `techContext.md`, `progress.md`, `activeContext.md` per plan D2

## Phase 5: Convergence

- [x] T016 Execute `quickstart.md` manual scenarios SC-001~SC-006 and record pass/fail in `checklists/manual-qa.md` per plan D3 (partial)
- [x] T017 Add unit tests for KeyboardHook immediate vs on_key gating per FR-004, FR-005, FR-006 (partial)
- [x] T018 Update `projectbrief.md` to state English-only trigger input/matching scope per plan D2 (partial)
- [x] T019 Show Korean display labels (스페이스, Enter, Tab) for expansion key combobox per `contracts/gui-settings-ui.md` (partial)
