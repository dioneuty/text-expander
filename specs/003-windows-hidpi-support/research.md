# Research: Windows HiDPI 표시 지원 (003-windows-hidpi-support)

## R1: Windows DPI Awareness 선언

**Decision**: 프로세스 시작 시 **Per-Monitor DPI Aware (v1, awareness=2)** 를 `tk.Tk()` **이전**에 ctypes로 설정하고, PyInstaller exe에는 **애플리케이션 manifest**에 `dpiAwareness` PerMonitorV2를 포함한다.

**Rationale**:
- DPI unaware 상태에서는 Windows가 전체 창을 비트맵 스케일링해 **흐림(blur)** 이 발생한다(FR-001).
- Per-Monitor aware는 단일/혼합 모니터에서 논리 픽셀 기준 렌더링을 허용한다.
- tkinter는 Tk 생성 **전** DPI awareness가 설정되어야 일관된 동작을 한다.

**Implementation sketch** (`main.py` 또는 `src/gui/dpi.py`):
```python
def enable_dpi_awareness() -> None:
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass
```

**Alternatives considered**:
- System DPI aware only (awareness=1) → 혼합 DPI에서 보조 모니터 스케일 오차, Per-Monitor v1이 더 낫다
- manifest만, 런타임 호출 없음 → `python main.py`와 exe 일관성 위해 **둘 다** 적용
- Per-Monitor V2 (awareness=2 + manifest PerMonitorV2) → Win10 1703+; 실시간 WM_DPICHANGED 핸들러는 1차 범위 밖(FR-008)

---

## R2: DPI 스케일 팩터 측정

**Decision**: `src/gui/dpi.py`에 `get_ui_scale_factor() -> float` 제공. **96 DPI = 1.0** 기준, `round(dpi/96, 2)` 클램프(최소 1.0, 최대 3.0).

**Rationale**: FR-007/FR-009의 “100% 기준 크기 × 배율”을 코드로 일관 적용.

**Preferred query order** (Windows):
1. `GetDpiForSystem()` (Win10 1607+)
2. `GetDeviceCaps(hdc, LOGPIXELSX)` fallback
3. 실패 시 `1.0`

**Tk 생성 후 교차 검증**(선택): `root.winfo_fpixels('1i') / 96.0` — bootstrap과 ±0.05 이내면 Tk 값 사용.

**Alternatives considered**:
- tk `scaling`만 사용 → Tk 생성 전 창 geometry 계산 불가, bootstrap 분리 필요
- Windows 설정 UI % 직접 읽기 → API 없음, DPI가 정확

---

## R3: 창·대화상자 geometry 스케일링

**Decision**: 100% 기준 상수를 `src/gui/dpi.py`(또는 `constants.py` 일부)에 두고 `scale_geometry(base_w, base_h, factor)`로 산출.

| Surface | 100% base | Scaled example @150% |
|---------|-----------|----------------------|
| Main window | 720×540 | 1080×810 |
| Main minsize | 560×420 | 840×630 |
| Add/Edit dialog | 480×420 (신규 명시) | 720×630 |

**Rationale**: Clarify Q1/Q3 — 메인·대화상자 동일 규칙. 현재 대화상자는 geometry 미설정 → 명시적 크기 + `minsize` 추가.

**Also scale**:
- `wraplength` (현재 680 → `int(680 * factor)`)
- Frame `padding` (12 → `int(12 * factor)`)
- Entry `width` / Text `width,height` (grid 기반 dialog)

**Alternatives considered**:
- geometry만 키우고 wraplength 고정 → 200%에서 줄바꿈 과다·레이아웃 깨짐
- ttk themes only → tkinter 기본 ttk는 고배율 폰트 자동 확대가 약함; scaling + geometry 병행

---

## R4: tk scaling / 폰트

**Decision**: `Application.__init__`에서 `Tk()` 직후 `root.tk.call('tk', 'scaling', factor)` 호출. ttk 기본 폰트는 scaling에 따름.

**Rationale**: Clarify에서 “폰트/패딩 세부”는 plan 단계로 deferred — `tk scaling`이 최소 변경으로 가독성 개선.

**Alternatives considered**:
- ttk.Style per-widget font override → 유지보수 부담, 1차 불필요
- custom tk Font everywhere → 과도

---

## R5: PyInstaller exe HiDPI (FR-004)

**Decision**: `build.spec` EXE에 Windows manifest 리소스 추가.

**Manifest essentials**:
```xml
<dpiAware>true</dpiAware>
<dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
```

**Files**: `assets/app.manifest` (신규) + `build.spec` `exe` 섹션에 `manifest='assets/app.manifest'`.

**Rationale**: SC-004 — exe만 DPI unaware로 빌드되면 blur 재발.

**Alternatives considered**:
- `--win-private-assemblies` only → DPI manifest 없으면 blur 지속
- console=True debug exe → 배포 exe와 동일 manifest 적용

---

## R6: 혼합 DPI / 재시작 (FR-008)

**Decision**: 1차는 **WM_DPICHANGED 핸들러 미구현**. Per-Monitor aware + 재시작 후 정상이면 통과.

**Rationale**: Clarify Q2 best-effort. 실시간 Per-Monitor V2 이벤트 처리는 tkinter에서 복잡도 대비 효익 낮음.

**Alternatives considered**:
- Tk `tk scaling` bind on move → 불안정, 기각
- System DPI only → 혼합 모니터 품질 저하

---

## R7: 테스트 전략

**Decision**:
- **Unit**: `scale_geometry`, `get_ui_scale_factor` mock/fallback (Windows API mock or fixed factor injection)
- **Manual**: quickstart.md — 125/150/200% 단일 모니터 + exe 비교 + 혼합 DPI 재시작

**Rationale**: GUI 픽셀 perfect assertion은 CI Windows runner 없으면 brittle; 수학·bootstrap 단위 + 수동 SC 매핑.

**Alternatives considered**:
- Pillow screenshot diff → 과도, 1차 불필요
