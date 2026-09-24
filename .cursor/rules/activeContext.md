# Active Context

## 현재 작업 포커스

**요구사항 확정 완료** — 전역 확장 + 자유 트리거 + tkinter GUI. 다음은 **MVP 구현** (Repository/Service/Expander → KeyboardHook → tkinter GUI).

## 최근 변경사항

- 2026-09-24: Memory Bank 6개 파일 초기화
- 2026-09-24: **사용자 결정 반영**
  - **어디서든 동작** — 전역 키보드 후킹을 핵심 기능(P0)으로 승격
  - **자유 트리거** — 접두사(`;`, `@@`) 규칙 제거
  - **tkinter GUI** — CLI 대신 GUI를 주 인터페이스로 확정

## 활성 결정사항

| 결정 | 이유 |
|------|------|
| 전역 확장 (pynput) | 메모장·브라우저·메신저 등 모든 앱에서 사용 |
| 자유 트리거 입력 | 사용자 유연성; 긴·고유 트리거 사용 권장으로 오치환 완화 |
| tkinter GUI | 표준 라이브러리, 설치 부담 없음, Windows 데스크톱에 적합 |
| JSON 파일 저장 | 의존성 없음, GUI·후킹이 동일 데이터 공유 |
| suffix + 최장 매칭 | 자유 트리거 환경에서 `addr` vs `myaddr` 충돌 처리 |
| 확장 트리거 키 | Space/Enter/Tab 등 입력 시점에 치환 (자유 트리거 오입력 방지) |

## 다음 단계

1. 프로젝트 뼈대: `main.py`, `requirements.txt`, `.gitignore`
2. `models.py`, `repository.py`, `service.py`, `expander.py`
3. `keyboard_hook.py`, `injector.py` — pynput 전역 후킹
4. `gui/main_window.py`, `gui/app.py` — tkinter CRUD + 서비스 ON/OFF
5. Windows·한글 IME 수동 테스트 (메모장, Chrome)
6. README: 설치, 실행, 트리거 작성 팁

## 미결정 (구현 중 결정)

- **트레이 아이кон**: 1차 MVP 포함 vs 2차
- **expansion 주입 방식**: `Controller.type` only vs pyperclip fallback
- **확장 트리거 키 목록**: Space/Enter/Tab 외 추가 여부

## 주의사항

- GUI mainloop와 pynput 리스ner **스레드 분리** 필수
- CRUD 후 KeyboardHook에 shortcuts **reload** 필요
- 한글 IME 조합 중 버퍼 처리 — 초기부터 설계에 포함
- 자유 트리거는 짧은 일반 단어 등록 시 오치환 위험 → GUI 등록 화면에 안내 문구
