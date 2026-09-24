# Research: 영문 전용 안내 및 확장 모드 선택 (002-english-expansion-mode)

## R1: 설정 영속화 위치

**Decision**: `data/settings.json` 별도 파일 + `SettingsRepository` (또는 `src/settings.py` 단일 모듈).

**Rationale**: `shortcuts.json`은 단축어 CRUD 전용 스키마(`version`, `shortcuts`)를 유지한다. 확장 모드는 단축어와 독립적으로 변경·로드되며, 기존 사용자 `shortcuts.json` 마이그레이션 없이 기본값으로 동작 가능.

**Alternatives considered**:
- `shortcuts.json`에 `settings` 키 추가 → 단일 파일이지만 Repository 책임 혼합, version bump 필요
- 레지스트리/ini → Constitution JSON 정책과 불일치

**Default values** (spec Assumptions):
```json
{
  "version": 1,
  "expansion_mode": "on_key",
  "expansion_key": "space"
}
```

---

## R2: 즉시 확장 vs 키 입력 후 확장 — KeyboardHook 분기

**Decision**: `KeyboardHook` 생성 시 `ExpansionSettings` snapshot을 받고, `set_settings()`로 GUI 저장 시 갱신(thread-safe lock).

| Mode | `_try_immediate_expansion()` | Expansion key handler |
|------|------------------------------|------------------------|
| `immediate` | **ON** — printable char append 후 | **OFF** — Space/Enter/Tab은 버퍼에만 append(확장 판정 없음) |
| `on_key` | **OFF** | **ON** — 설정된 키(space/enter/tab) 입력 시에만 `find_expansion` |

**Rationale**: 현재 코드는 두 경로가 **동시에** 활성(`keyboard_hook.py` L123–139). Spec FR-004/FR-006은 **상호 배타** 모드를 요구. `on_key`에서 즉시 확장을 끄면 트리거만 입력 시 미치환 충족.

**Punctuation triggers** (`.`, `,`, `!`, `?`): Spec 1차 범위는 space/enter/tab만. `on_key` 모드에서는 **구두점 확장 트리거 비활성화**. `immediate` 모드에서도 구두점으로 확장하지 않음(즉시 확장만).

**Alternatives considered**:
- immediate 모드에서 expansion key도 허용 → 이중 확장·혼란, 기각
- 모드별 Hook 클래스 분리 → YAGNI, 단일 Hook + flag로 충분

---

## R3: 영문 전용 버퍼 문자

**Decision**: `is_buffer_char()`를 **ASCII printable** (`char.isascii() and char.isprintable() and not char.isspace()`) 로 제한. Hangul Unicode range 제거.

**Rationale**: FR-009. `buffer_chars.py` 현재 Hangul 허용 — 제거. 한글 입력은 버퍼 무시, 앱으로 그대로 전달(pynput 기본 동작).

**IME 처리**: `ime_state.py` import 및 `is_ime_composing()` gate **제거**. 한글 트리거 미지원이므로 IMM API 불필요. `ime_state.py`, `text_context.py`(IME 전용), 관련 테스트는 정리 대상.

**Alternatives considered**:
- IME gate 유지 + Hangul 버퍼만 차단 → dead code, 기각
- 등록 시 트리거 ASCII 검증 추가 → UX 보조(선택); 1차는 안내 + 버퍼 필터만

---

## R4: GUI 설정 UX

**Decision**: 메인 창 하단(서비스 ON/OFF 근처)에 **설정 프레임** 추가:
- `ttk.Radiobutton` ×2: 즉시 확장 / 키 입력 후 확장
- `ttk.Combobox`(readonly): space | enter | tab — `on_key` 선택 시에만 enabled
- **저장** 버튼 또는 옵션 변경 즉시 저장 + Hook `set_settings()` 호출

**Rationale**: FR-011. tkinter 기존 패턴 유지. 모드 전환 시 expansion key combobox enable/disable.

**Copy changes** (`constants.py`):
- `INFO_KOREAN_INPUT` **삭제**
- `INFO_TRIGGER_TIP` — `회사서명` 예시 제거, 영문 예시만
- `INFO_ENGLISH_ONLY` 추가
- `INFO_IMMEDIATE_MODE_WARNING` 추가 (FR-010)
- 다이얼로그에 `INFO_TRIGGER_ENGLISH` 한 줄 (선택)

---

## R5: Hook ↔ GUI 설정 동기화

**Decision**: `Application`이 `SettingsRepository.load()` → `KeyboardHook(..., settings=...)` → `MainWindow`에 settings + callback `on_settings_saved`.

**Rationale**: Constitution III — GUI와 Hook이 Service/Repository 공유. 설정은 Repository 경유, 저장 후 Hook hot-reload( shortcuts와 동일 패턴).

**Thread safety**: `_settings_lock` + immutable `ExpansionSettings` dataclass 교체.

---

## R6: 테스트 전략

**Decision**:
- **Unit**: `test_buffer_char.py` — Hangul False, ASCII True; `test_expansion_settings.py` — mode gating logic (Hook behavior via extracted helper or mock)
- **Manual**: `quickstart.md` SC-001~006 시나리오

**Rationale**: pynput 통합 테스트는 brittle. 핵심 분기는 순수 함수/설정 객체로 테스트 가능하면 추출.

---

## R7: Constitution 정합성

**Decision**: 구현 완료 시 `.specify/memory/constitution.md` 및 Memory Bank에서 **한글 IME 규칙** 문구 제거·영문 전용으로 수정 (별도 amendment, 본 feature tasks에 포함).

**Gate note**: Plan 단계 Constitution Check에서 "한글 IME" 규칙은 **본 feature로 supersede** — justified in Complexity Tracking 없음(정합성 업데이트).
