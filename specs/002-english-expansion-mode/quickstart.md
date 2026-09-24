# Quickstart: 영문 전용 안내 및 확장 모드 검증

**Feature**: 002-english-expansion-mode  
**Prerequisites**: Windows 10/11, English keyboard input, `python main.py` or exe

## Setup

```powershell
cd "c:\portfolio-python\단축어 프로그램"
.\.venv\Scripts\Activate.ps1
python main.py
```

Register test shortcuts:

| Trigger | Expansion |
|---------|-----------|
| `addr` | `Seoul, Korea` |
| `myemail` | `user@example.com` |
| `myaddr` | `My Full Address Line` |
| `sig1` | `Best regards` |
| `sig2` | `Thank you` |

Ensure **전역 확장 서비스** is ON.

---

## Scenario 1: Copy audit (SC-001, SC-002)

1. Open main window → verify **no** Korean IME / Korean trigger support text.
2. Verify **English-only** guidance visible.
3. Open README → confirm Korean IME section removed; English-only documented.

**Expected**: SC-001 0 Korean-IME claims; SC-002 guidance on main + README.

---

## Scenario 2: Immediate mode (SC-003)

1. Settings → **즉시 확장** → Save.
2. Notepad: type `addr` (no space).

**Expected**: Expands to `Seoul, Korea` on last char `r`.

Repeat for 5 triggers → **5/5** without Space/Enter.

3. Type `add` only → **no** expansion.

4. With both `addr` and `myaddr` registered, type `myaddr` → expands to `My Full Address Line`.

---

## Scenario 3: On-key mode — Space (SC-004)

1. Settings → **키 입력 후 확장**, key **스페이스** → Save.
2. Notepad: type `addr` → **no** expansion.
3. Press Space → expands; space not duplicated in output.

Repeat 5 triggers: **0/5** before key, **5/5** after Space.

---

## Scenario 4: On-key mode — Enter / Tab

1. Set expansion key to **Enter** → Save.
2. Type `sig1` + Enter → expansion runs.

3. Set expansion key to **Tab** → Save.
4. Type `sig2` + Tab → expansion runs.

---

## Scenario 5: Settings persistence (SC-005)

1. Set **즉시 확장** → Save → exit app.
2. Restart → GUI shows immediate; Notepad test confirms immediate behavior.
3. Repeat 3 cycles with different modes/keys.

**Expected**: **3/3** match after restart.

---

## Scenario 6: Hangul input no false expansion (SC-006)

1. On-key mode, Space.
2. Switch to Korean IME, type arbitrary Hangul 10 times in Notepad (no registered Korean triggers).

**Expected**: **0** expansions; normal Hangul input in app.

---

## Scenario 7: Service OFF

1. Uncheck 전역 확장 서비스.
2. Type registered trigger in either mode.

**Expected**: No expansion.

---

## Pass Criteria Summary

| ID | Criterion |
|----|-----------|
| SC-001 | No Korean IME UI/README text |
| SC-002 | English-only guidance visible |
| SC-003 | Immediate 5/5 |
| SC-004 | On-key 0/5 then 5/5 |
| SC-005 | Settings persist 3/3 |
| SC-006 | Hangul 0 false expansions |

---

## Related Contracts

- [keyboard-hook-expansion-mode.md](./contracts/keyboard-hook-expansion-mode.md)
- [settings-repository.md](./contracts/settings-repository.md)
- [gui-settings-ui.md](./contracts/gui-settings-ui.md)
