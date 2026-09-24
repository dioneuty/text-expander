# Quickstart: Windows HiDPI 검증

**Feature**: 003-windows-hidpi-support  
**Prerequisites**: Windows 10/11, display scaling adjustable, venv active

## Setup

```powershell
cd "c:\portfolio-python\단축어 프로그램"
.\.venv\Scripts\Activate.ps1
python main.py
```

Optional exe build:

```powershell
.\build.bat
# dist\단축어프로그램.exe
```

---

## Scenario 1: 150% main window (SC-001, FR-001, FR-002)

1. Windows **Settings → Display → Scale 150%** → sign out/in if prompted.
2. Run `python main.py`.
3. Inspect: info labels, tree headers, Add/Edit/Delete, expansion mode, service toggle.

**Expected**:
- Text readable, **not blurry**
- No clipped controls at default window size
- Default window visibly larger than 100% baseline (~1080×810 logical)

---

## Scenario 2: 200% layout (SC-002, FR-007)

1. Set scale **200%**, restart app.
2. Main window at default size — no **horizontal scrollbar** on main content.

**Expected**: All P1 areas visible in one view.

---

## Scenario 3: Add dialog (SC-003, FR-003, FR-009)

1. At **150%+**, click **추가**.
2. Complete trigger `test1`, expansion `Hello HiDPI`, Save.

**Expected**:
- Dialog opens scaled
- All fields + buttons visible
- Save completes in < 3 min without workarounds

---

## Scenario 4: exe parity (SC-004, FR-004)

1. Same PC, same scale (150%).
2. Run `python main.py`, note layout/size/clarity.
3. Close; run `dist\단축어프로그램.exe`.

**Expected**: No obvious visual difference (size, sharpness, layout).

---

## Scenario 5: 100% regression (SC-005, FR-006)

1. Set scale **100%**.
2. List shortcuts, add one, toggle service OFF/ON.

**Expected**: Same or better layout vs pre-HiDPI; functional parity with 002 feature.

---

## Scenario 6: Mixed DPI best-effort (FR-008, User Story 4)

**Requires** two monitors with different scale (e.g. 150% + 100%).

1. Launch on primary — pass Scenarios 1–3.
2. Move window to secondary (may look wrong — OK).
3. **Restart app** on secondary.

**Expected**: After restart, FR-001~003 pass on that monitor.

---

## Scenario 7: Scale sweep (125%)

1. Set **125%**, restart app.

**Expected**: UI usable; between 100% and 150% behavior.

---

## Unit tests

```powershell
pytest tests/unit/test_dpi_scaling.py -v
```

**Expected**: geometry/token scaling math passes; no Windows API required if mocked.

---

## Mapping

| Scenario | Success Criteria |
|----------|------------------|
| 1 | SC-001 |
| 2 | SC-002 |
| 3 | SC-003 |
| 4 | SC-004 |
| 5 | SC-005 |
| 6 | FR-008 |
| 7 | Edge 125% |
