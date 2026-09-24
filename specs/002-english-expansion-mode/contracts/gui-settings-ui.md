# Contract: GUI Settings UI

**Module**: `src/gui/main_window.py`, `src/gui/constants.py`  
**Feature**: 002-english-expansion-mode

## Main Window — Info Labels

| Constant | Requirement |
|----------|-------------|
| `INFO_KOREAN_INPUT` | **REMOVED** — must not be displayed |
| `INFO_TRIGGER_TIP` | English-only trigger examples (e.g. `myaddr`); no Korean trigger examples |
| `INFO_ENGLISH_ONLY` | **NEW** — states triggers are English (Latin) letters, digits, symbols; Korean triggers not supported |
| `INFO_IMMEDIATE_MODE_WARNING` | **NEW** — warns immediate mode increases accidental expansion risk |

Main window MUST show `INFO_ENGLISH_ONLY` and updated `INFO_TRIGGER_TIP`.  
When `immediate` mode selected, show or emphasize `INFO_IMMEDIATE_MODE_WARNING`.

---

## Settings Frame (new)

**Location**: Main window, above or below service ON/OFF checkbox.

**Controls**:

| Control | ID / var | Values |
|---------|-----------|--------|
| Mode radio | `expansion_mode_var` | `immediate` / `on_key` (labels Korean: 즉시 확장 / 키 입력 후 확장) |
| Expansion key combobox | `expansion_key_var` | `space`, `enter`, `tab` (labels: 스페이스, Enter, Tab) |
| Save button | — | `BTN_SAVE_SETTINGS` or reuse save pattern |

**Behavior**:
- Combobox **disabled** when mode is `immediate`
- On Save: persist via `SettingsRepository`, call `hook.set_settings()`, show confirmation optional
- Initial load: reflect `SettingsRepository.load()` on window open

---

## Add/Edit Dialog (optional 1차)

- Trigger field: optional hint label `INFO_TRIGGER_ENGLISH` below trigger entry
- No validation block for non-ASCII triggers in 1차

---

## README Contract

- Section `## 한글 트리거 · IME` **REMOVED**
- Add section explaining English-only triggers and two expansion modes
- Remove Korean trigger examples from usage table
