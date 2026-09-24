# Contract: KeyboardHook — Expansion Mode Behavior

**Module**: `src/keyboard_hook.py`  
**Feature**: 002-english-expansion-mode

## Configuration

```python
@dataclass(frozen=True)
class ExpansionSettings:
    mode: Literal["immediate", "on_key"]
    expansion_key: Literal["space", "enter", "tab"]
```

Hook MUST accept `settings: ExpansionSettings` at construct and expose:

```python
def set_settings(self, settings: ExpansionSettings) -> None: ...
```

Updates MUST be thread-safe (same lock as shortcuts reload).

---

## Buffer Rules

1. Only characters passing `is_buffer_char(char)` where `is_buffer_char` returns True **iff** ASCII printable non-whitespace.
2. Non-matching characters (including Hangul): **no buffer change**, no expansion, event returns normally.
3. Backspace: trim buffer by 1 when enabled and not paused (IME gate removed).

---

## Mode: `immediate`

| Event | Behavior |
|-------|----------|
| Printable buffer char | Append → `find_expansion(buffer)` → if match, `_apply_expansion` |
| Space / Enter / Tab | Append corresponding char to buffer only; **MUST NOT** run expansion |
| `. , ! ?` | Append only; **MUST NOT** run expansion |

---

## Mode: `on_key`

| Event | Behavior |
|-------|----------|
| Printable buffer char | Append only; **MUST NOT** run immediate expansion |
| Configured expansion key | If buffer matches trigger → `_apply_expansion`; expansion key char MUST NOT appear in output (trigger replaced only) |
| Other Space/Enter/Tab (not configured) | Append char to buffer only |
| `. , ! ?` | Append only; **MUST NOT** run expansion |

---

## Shared Rules (both modes)

- `find_expansion` / longest suffix match unchanged (`src/expander.py`)
- Service disabled or paused → no expansion, minimal buffer ops per existing behavior
- `_apply_expansion`: trim buffer by `len(trigger)`, call injector

---

## Regression

English triggers (`addr`, `myemail`) MUST match spec success criteria per mode.
