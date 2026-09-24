# Data Model: 영문 전용 안내 및 확장 모드 선택

**Feature**: 002-english-expansion-mode

## Persistent Entities

### SettingsFile (`data/settings.json`)

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| `version` | `int` | yes | `1` | Must be `1` for 1차 |
| `expansion_mode` | `string` | yes | `"on_key"` | `"immediate"` \| `"on_key"` |
| `expansion_key` | `string` | yes | `"space"` | `"space"` \| `"enter"` \| `"tab"` |

**Example**:
```json
{
  "version": 1,
  "expansion_mode": "on_key",
  "expansion_key": "space"
}
```

**Notes**:
- File missing → defaults applied, file created on first save
- Invalid enum → load defaults + log/warn (GUI message optional)
- `expansion_key` ignored at runtime when `expansion_mode` is `"immediate"` (still persisted for UX when user switches back)

---

### ExpansionSettings (runtime dataclass)

| Field | Type | Description |
|-------|------|-------------|
| `mode` | `Literal["immediate", "on_key"]` | Active expansion behavior |
| `expansion_key` | `Literal["space", "enter", "tab"]` | Key that triggers expansion in `on_key` mode |

**Mapping to pynput `Key`**:
| `expansion_key` | pynput Key |
|-----------------|------------|
| `space` | `Key.space` |
| `enter` | `Key.enter` |
| `tab` | `Key.tab` |

**Defaults**: `ExpansionSettings(mode="on_key", expansion_key="space")`

---

### Shortcut (unchanged)

| Field | Type | Notes |
|-------|------|-------|
| `trigger` | `str` | 1차: 영문·숫자·ASCII 기호 권장; 한글 트리거는 매칭되지 않음 |
| `expansion` | `str` | 한글·여러 줄 허용 |

Stored in `data/shortcuts.json` — schema unchanged.

---

## Runtime State (KeyboardHook)

| State | Type | Notes |
|-------|------|-------|
| `_buffer` | `str` | suffix matching; ASCII printable chars only |
| `_shortcuts` | `dict[str, str]` | reload from Service |
| `_settings` | `ExpansionSettings` | reload via `set_settings()` |
| `_enabled`, `_paused` | `bool` | unchanged |

---

## State Transitions

### Settings save (GUI → disk → Hook)

```
User changes mode/key in GUI
  → validate enums
  → SettingsRepository.save()
  → KeyboardHook.set_settings(new_settings)
  → (optional) status message
```

### Character input (Hook)

```
on_key press (printable, is_buffer_char)
  → append buffer
  → if mode == immediate: try find_expansion → apply or noop

expansion key press (space/enter/tab)
  → if mode == on_key AND key == configured expansion_key:
       find_expansion → apply if match
  → if mode == immediate: append char only (no expansion on this key)
  → if mode == on_key AND key != configured: append char only
```

---

## Files Touched (implementation reference)

| File | Change |
|------|--------|
| `data/settings.json` | NEW (gitignore if `data/` ignored) |
| `src/settings.py` | NEW — model + repository |
| `src/buffer_chars.py` | ASCII-only |
| `src/keyboard_hook.py` | mode gating, remove IME |
| `src/ime_state.py` | DELETE (or deprecate) |
| `src/gui/constants.py` | copy update |
| `src/gui/main_window.py` | settings UI |
| `src/gui/app.py` | load settings, wire hook |
| `README.md` | remove Korean IME section |

---

## Validation Rules (GUI)

| Rule | Message (KO) |
|------|----------------|
| expansion_mode required | (radiobutton — always one selected) |
| expansion_key required when on_key | (combobox — always one selected) |

Optional future: trigger ASCII-only warning on save — **Out of scope** for 1차.
