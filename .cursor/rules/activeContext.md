# Active Context

## 현재 작업 포커스

**003-windows-hidpi-support 구현 완료** — Windows HiDPI GUI 스케일링, exe manifest.

## 최근 변경사항

- 2026-09-24: 003-windows-hidpi-support 구현 (`src/gui/dpi.py`, manifest, scaled GUI)
- 2026-09-24: 002-english-expansion-mode 구현 (settings, Hook 모드, GUI, README)
- 2026-09-24: 001-korean-input 스펙 제거, ime_state/text_context 삭제
- 2026-09-24: Spec Kit 초기화, Python 3.12 + specify-cli 설치

## 활성 결정사항

| 결정 | 이유 |
|------|------|
| 영문 트리거만 매칭 | IME 복잡도 제거, 안내 일관성 |
| 기본 확장 모드 `on_key` + space | 오치환 위험 낮음 |
| `settings.json` 분리 | shortcuts 스키마 유지 |
| suffix + 최장 매칭 | 기존 규칙 유지 |
| HiDPI geometry × scale_factor | 100% 기준 720×540, 대화상자 480×420 |
| 혼합 DPI | 재시작 후 정상이면 통과 (best-effort) |

## 다음 단계

1. ~~003 HiDPI 수동 QA~~ ✅ M1~M7 사용자 검증 완료
2. P1: 트레이 아이콘, pyperclip fallback 강화
3. exe 재빌드 (`build.bat`) — 배포 시

## 주의사항

- GUI mainloop와 pynput listener 스레드 분리 유지
- CRUD 후 Hook reload, 설정 저장 후 `set_settings()` 호출
- 즉시 확장 모드는 오치환 위험 — GUI 경고 표시
