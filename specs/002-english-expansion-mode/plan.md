# Implementation Plan: 영문 전용 안내 및 확장 모드 선택

**Branch**: `002-english-expansion-mode` | **Date**: 2026-09-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-english-expansion-mode/spec.md`

## Summary

한글 IME·한글 트리거 관련 **사용자 안내를 제거**하고 **영문 입력 전용**으로 정렬한다. KeyboardHook에 **확장 모드 2종**(즉시 확장 / 키 입력 후 확장)을 추가하고, `data/settings.json`으로 **영속 저장**한다. Hangul 버퍼·IME gate 코드를 제거해 동작을 단순화한다.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: pynput, tkinter (stdlib), pyperclip (expansion inject)  
**Storage**: `data/shortcuts.json` (기존) + `data/settings.json` (신규)  
**Testing**: pytest (unit), manual per quickstart.md  
**Target Platform**: Windows 10/11  
**Project Type**: Desktop utility (single package)  
**Performance Goals**: 키 입력 지연 체감 없음 (기존 Hook 수준)  
**Constraints**: GUI mainloop ↔ pynput 스레드 분리; thread-safe settings reload  
**Scale/Scope**: 단일 사용자 로컬 설정; 전역 설정 1세트

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Windows 전역 확장 | ✅ PASS | pynput Hook 유지 |
| II. 자유 트리거 | ✅ PASS | 접두사 강제 없음; 영문 **입력**만 매칭 |
| III. 레이어 분리 | ✅ PASS | SettingsRepository + Hook/GUI 분리 |
| IV. 영속 저장 | ✅ PASS | settings.json 추가 |
| V. 단순함 | ✅ PASS | ime_state 제거, 단일 settings 파일 |
| 한글 IME 규칙 (constitution) | ⚠️ SUPERSEDE | 본 feature로 **제거** — 구현 시 constitution·Memory Bank amendment 포함 |
| suffix + 최장 매칭 | ✅ PASS | Expander 변경 없음 |
| 한국어 UI 메시지 | ✅ PASS | 안내 문구는 한국어 유지 |

**Post-design re-check**: ✅ All gates pass. Constitution IME clause amendment tracked in Phase D.

## Project Structure

### Documentation (this feature)

```text
specs/002-english-expansion-mode/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/
│   ├── keyboard-hook-expansion-mode.md
│   ├── settings-repository.md
│   └── gui-settings-ui.md
└── tasks.md             # /speckit-tasks (next)
```

### Source Code (repository root)

```text
단축어 프로그램/
├── main.py
├── data/
│   ├── shortcuts.json
│   └── settings.json          # NEW
├── src/
│   ├── settings.py            # NEW — ExpansionSettings + SettingsRepository
│   ├── buffer_chars.py        # MODIFY — ASCII-only
│   ├── keyboard_hook.py       # MODIFY — mode gating, remove IME
│   ├── expander.py            # unchanged (matching logic)
│   ├── injector.py
│   ├── repository.py
│   ├── service.py
│   ├── ime_state.py           # DELETE
│   ├── text_context.py        # DELETE or trim if unused
│   └── gui/
│       ├── app.py             # MODIFY — load settings
│       ├── main_window.py     # MODIFY — settings UI
│       └── constants.py       # MODIFY — copy
├── tests/unit/
│   ├── test_buffer_char.py    # MODIFY
│   ├── test_expansion_settings.py  # NEW
│   └── (remove korean/ime tests)
└── README.md                  # MODIFY
```

**Structure Decision**: 기존 단일 패키지 유지. 설정은 `src/settings.py` 한 모듈로 YAGNI.

## Complexity Tracking

> Constitution IME 규칙 supersede — 별도 violation 없음. ime_state 제거는 **복잡도 감소**.

| Change | Why | Simpler Alternative Rejected |
|--------|-----|------------------------------|
| Delete `ime_state.py` | 한글 트리거 미지원 | IME gate 유지 → dead code |

---

## Implementation Phases

### Phase A — Settings & model (User Story 4 foundation)

| Task | File | Action |
|------|------|--------|
| A1 | `src/settings.py` | `ExpansionSettings` dataclass + `SettingsRepository` |
| A2 | `src/paths.py` | `get_settings_path()` if needed |
| A3 | `tests/unit/test_expansion_settings.py` | load/save/default merge |

### Phase B — English-only buffer & Hook modes (User Story 2, 3)

| Task | File | Action |
|------|------|--------|
| B1 | `src/buffer_chars.py` | ASCII printable only; remove Hangul ranges |
| B2 | `src/keyboard_hook.py` | Accept `ExpansionSettings`; `set_settings()`; mode gating per [contract](./contracts/keyboard-hook-expansion-mode.md) |
| B3 | `src/keyboard_hook.py` | Remove `ime_state` import and composing checks |
| B4 | `src/ime_state.py`, `text_context.py` | Delete if unused |
| B5 | `tests/unit/test_buffer_char.py` | Hangul → False |
| B6 | Tests | Remove/update `test_ime_state.py`, `test_expander_korean.py` |

### Phase C — GUI & copy (User Story 1, 4)

| Task | File | Action |
|------|------|--------|
| C1 | `src/gui/constants.py` | Remove `INFO_KOREAN_INPUT`; add English-only + mode warning strings |
| C2 | `src/gui/main_window.py` | Settings frame (mode radio, key combobox, save) |
| C3 | `src/gui/app.py` | Load settings → Hook; wire save callback |
| C4 | `README.md` | Remove Korean IME section; document modes + English-only |

### Phase D — Docs & constitution sync

| Task | File | Action |
|------|------|--------|
| D1 | `.specify/memory/constitution.md` | Remove 한글 IME rule; add English-only trigger note |
| D2 | `.cursor/rules/systemPatterns.md`, `techContext.md`, `progress.md` | Align with feature |
| D3 | Manual QA | Run [quickstart.md](./quickstart.md) SC-001~006 |

---

## Risk & Mitigation

| Risk | Mitigation |
|------|------------|
| Existing users on immediate behavior (README says immediate) | Default `on_key` + space per spec; README updated |
| `immediate` + short triggers → false expansion | GUI warning (FR-010) |
| Hangul triggers in shortcuts.json | No auto-delete; won't match (document in README) |
| Thread race on settings save | Same lock pattern as `reload()` |

---

## Next Command

Run **`/speckit-tasks`** to generate dependency-ordered `tasks.md`, then **`/speckit-implement`**.
