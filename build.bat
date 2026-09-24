@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [1/4] 가상환경 생성...
    python -m venv .venv
)

echo [2/4] 의존성 설치...
.venv\Scripts\pip install -r requirements-dev.txt -q

echo [3/4] exe 빌드 중...
.venv\Scripts\pyinstaller build.spec --noconfirm

if errorlevel 1 (
    echo 빌드 실패
    exit /b 1
)

echo [4/4] 완료
echo.
echo 실행 파일: dist\단축어프로그램.exe
echo 단축어 데이터: exe와 같은 폴더의 data\shortcuts.json
echo.
endlocal
