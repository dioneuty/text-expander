# Manual QA: 영문 전용 안내 및 확장 모드 (002-english-expansion-mode)

**Date**: 2026-09-24  
**Environment**: Windows, Python 3.10+, `python main.py`

## Automated / Static Verification

| ID | Criterion | Method | Result |
|----|-----------|--------|--------|
| SC-001 | No Korean IME / Korean trigger support copy | grep `src/`, `README.md` | **PASS** |
| SC-002 | English-only guidance on main + dialog | `INFO_ENGLISH_ONLY`, `INFO_TRIGGER_ENGLISH` | **PASS** |
| SC-003 | Immediate mode last-key expansion | `test_keyboard_hook_modes.py` | **PASS** |
| SC-004 | On-key mode: no expand until key; space uses extra backspace | `test_keyboard_hook_modes.py`, `test_injector_backspace.py` | **PASS** |
| SC-005 | Settings persist load/save | `test_expansion_settings.py` | **PASS** |
| SC-006 | Hangul not matched in buffer | `test_buffer_char.py`, `test_trigger_validation.py` | **PASS** |

## Manual Scenarios (recommended before release)

| Scenario | Steps | Expected | Status |
|----------|-------|----------|--------|
| M1 Notepad immediate | `sd` trigger, immediate mode | Expands without Space | **PASS** (user verified) |
| M2 Notepad on-key | `sd` + Space, on_key mode | `안녕하세요` only (no `s` prefix) | **PASS** (user verified) |
| M3 Settings restart | Change mode → restart app | Same mode in GUI + behavior | **PASS** (user verified) |
| M4 Hangul typing | Korean IME in Notepad, on_key mode | No false expansion | **PASS** (user verified) |
| M5 Trigger dialog block | Type Hangul in trigger field | Input rejected | **PASS** (user verified) |

## Unit Test Summary

```
pytest tests/unit -q → 18 passed (2026-09-24)
```

## Sign-off

- [x] Static copy audit (SC-001, SC-002)
- [x] Automated behavioral tests (SC-003~SC-006)
- [x] Full manual Notepad/Chrome pass (M1~M5) — user verified 2026-09-24
