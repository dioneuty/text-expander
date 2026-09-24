# 단축어 프로그램

Windows 어디서든 동작하는 Python 기반 텍스트 확장(단축어) 프로그램입니다.  
짧은 트리거를 입력하면 마지막 글자와 함께 미리 등록한 문장으로 자동 치환됩니다.

## 요구 사항

- Windows 10/11
- **exe 사용 시**: Python 설치 불필요
- **소스 실행 시**: Python 3.10+

## exe로 실행 (권장)

1. `dist\단축어프로그램.exe`를 더블클릭합니다.
2. 단축어 데이터는 exe **와 같은 폴더**의 `data\shortcuts.json`에 저장됩니다.

> exe를 다른 PC로 옮길 때는 `단축어프로그램.exe`만 복사해도 됩니다.  
> 첫 실행 시 `data` 폴더가 자동 생성됩니다.

### exe 빌드 방법 (개발자용)

```bash
build.bat
```

빌드 결과: `dist\단축어프로그램.exe`

## 소스에서 실행 (개발용)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 사용법

1. GUI에서 **추가** 버튼으로 트리거와 확장 텍스트를 등록합니다.
2. 메모장, 브라우저, 메신저 등 다른 앱에서 트리거를 입력합니다.
3. 트리거의 **마지막 글자**를 입력하면 즉시 확장됩니다.
4. **전역 확장 서비스** 체크박스로 ON/OFF 할 수 있습니다.

### 예시

| 트리거 | 확장 텍스트 |
|--------|-------------|
| `addr` | `Seoul, Korea` |
| `myemail` | `user@example.com` |

메모장에서 `addr` 입력 완료 → `Seoul, Korea` 로 치환됩니다.

## 트리거 작성 팁

- 짧은 일반 단어(`the`, `is`)는 의도치 않은 치환이 발생할 수 있습니다.
- **긴·고유한 트리거**(예: `myaddr`, `company_sig`) 사용을 권장합니다.
- `addr`과 `myaddr`을 함께 등록하면, 더 긴 `myaddr`이 우선 매칭됩니다.

## MVP 제한 사항

- **영문·숫자 트리거**만 전역 자동 확장을 지원합니다.
- 한글 트리거·한글 IME 입력은 추후 업데이트(P1) 예정입니다.
- 다중 줄 확장은 등록·저장 가능하나, 일부 앱에서 입력 방식에 제한이 있을 수 있습니다.

## 데이터 저장

단축어는 `data/shortcuts.json`에 저장됩니다. 프로그램을 재시작해도 유지됩니다.

- **exe 실행**: `단축어프로그램.exe` 옆 `data\shortcuts.json`
- **소스 실행**: 프로젝트 폴더 `data\shortcuts.json`

## 문제 해결

| 증상 | 확인 사항 |
|------|-----------|
| 확장이 동작하지 않음 | GUI에서 **전역 확장 서비스**가 켜져 있는지 확인 |
| 후킹 시작 실패 | 백신·보안 프로그램 예외 등록, 관리자 권한으로 실행 시도 |
| GUI 입력 중 치환됨 | GUI 창에 포커스가 있을 때는 자동 확장이 일시 중지됩니다 |

## 프로젝트 구조

```
├── main.py              # 진입점
├── src/
│   ├── models.py        # Shortcut 모델
│   ├── repository.py    # JSON 저장/로드
│   ├── service.py       # CRUD + 검증
│   ├── expander.py      # suffix 트리거 매칭
│   ├── keyboard_hook.py # pynput 전역 후킹
│   ├── injector.py      # Backspace + 텍스트 입력
│   └── gui/             # tkinter GUI
└── data/
    └── shortcuts.json   # 사용자 단축어 (gitignore)
```

## 라이선스

개인 포트폴리오·학습용 프로젝트
