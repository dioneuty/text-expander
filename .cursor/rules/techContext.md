# Tech Context

## 기술 스택

| 영역 | 선택 | 비고 |
|------|------|------|
| 언어 | Python 3.10+ | 타입 힌트 |
| GUI | **tkinter** | Python 표준 라이브러리, 별도 설치 불필요 |
| 전역 입력 | **pynput** | Windows 키보드 후킹 |
| 텍스트 주입 | pynput `Controller` + (필요 시) **pyperclip** | 긴/다중 줄 expansion |
| 저장 | JSON | stdlib `json`, `pathlib` |
| CLI | 없음 (또는 `main.py --debug` 수준만) | GUI가 주 인터페이스 |

## 개발 환경

- OS: **Windows 10/11** (주 개발·사용 환경)
- 에디터: Cursor / VS Code
- 가상환경: `venv` 권장

## 프로젝트 의존성

```
pynput>=1.7.6
pyperclip>=1.8.2      # 다중 줄·긴 expansion 붙여넣기 (필요 시)
```

### 표준 라이브러리

- `tkinter`, `json`, `pathlib`, `dataclasses`, `threading`, `logging`

## 파일·설정

| 경로 | 용도 |
|------|------|
| `data/shortcuts.json` | 사용자 단축어 저장 |
| `.gitignore` | `data/`, `__pycache__/`, `.venv/`, `dist/`, `build/` |
| `requirements.txt` | pynput, pyperclip |

## Windows 관련 제약 (중요)

| 이슈 | 대응 |
|------|------|
| **관리자 권한** | 일반 사용자 권한으로 동작 목표; 실패 시 GUI 안내 |
| **IME(한글 입력)** | 조합 중 문자는 버퍼 제외; commit 후에만 suffix 검사 |
| **백스페이스 치환** | 트리거 삭제 + expansion 입력; 타이밍 이슈 시 짧은 delay |
| **보안 SW** | 일부 백신이 키로거로 오탐 → 사용자 안내 |
| **클립보드** | pyperclip 사용 시 기존 클립보드 복원 권장 |

## tkinter GUI 구성 (예상)

| 화면 요소 | 위젯 |
|-----------|------|
| 단축어 목록 | `ttk.Treeview` (trigger / expansion 미리보기) |
| 추가·수정 | `Toplevel` + `Entry`(trigger) + `Text`(expansion) |
| 삭제 | 선택 항목 + 확인 `messagebox` |
| 서비스 ON/OFF | `ttk.Checkbutton` 또는 Toggle 버튼 |
| 상태 표시 | `ttk.Label` (실행 중 / 중지됨 / 오류) |

## 테스트

- **단위**: `expander.py`, `repository.py` — pytest (선택)
- **통합 수동**: 메모장, Notepad++, Chrome 입력창, 한글 IME ON/OFF
- **GUI 수동**: CRUD 후 JSON 반영·후킹 reload 확인

## 빌드·배포 (향후)

- PyInstaller `--windowed` 로 tkinter GUI exe
- `pynput`·`pyperclip` hidden import 확인

## 레퍼런스

- Espanso, AutoHotkey, TextExpander — 전역 확장 UX 참고 (코드 복사 X)
