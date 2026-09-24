# Progress

## 완료된 작업

- [x] 프로젝트 목적·범위 정의 (projectbrief)
- [x] 제품 컨텍스트·UX 목표 정리 (productContext)
- [x] 아키텍처·모듈 역할 설계 (systemPatterns)
- [x] 기술 스택·환경 정리 (techContext)
- [x] Memory Bank 초기화
- [x] Spec Kit 도입 (constitution, `.cursor/skills/`)
- [x] **요구사항 확정**: 전역 확장, 자유 트리거, tkinter GUI

## 진행 중

- (없음)

## 남은 작업

### MVP (P0)

- [x] 프로젝트 뼈대 (`main.py`, `requirements.txt`, `.gitignore`)
- [x] Shortcut 모델 + JSON Repository + Service
- [x] TextExpander (suffix, 최장 트리거 매칭)
- [x] KeyboardHook (pynput) + TextInjector
- [x] tkinter GUI: 목록, 추가, 수정, 삭제
- [x] GUI ↔ 후킹 연동 (저장 시 reload, ON/OFF)
- [x] README

### 1차 개선 (P1)

- [ ] 트레이 아이콘 / 최소화 시 백그라운드
- [ ] pyperclip fallback (다중 줄 expansion)
- [ ] GUI 상태 표시·오류 안내 강화
- [x] 영문 전용 트리거 + 확장 모드 선택 (002-english-expansion-mode)

### 2차 개선 (P2)

- [ ] pytest (Expander, Repository)
- [x] PyInstaller exe 패키징
- [x] 설정 파일 (확장 모드·확장 키 — `settings.json`)
- [ ] 설정 파일 (buffer 길이 등)

## 제외·취소된 항목

- ~~CLI 주 인터페이스~~ → tkinter GUI로 대체
- ~~트리거 접두사 강제 (`;`, `@@`)~~ → 자유 입력
- ~~1단계 터미널 REPL only~~ → 전역 확장이 MVP 핵심
- ~~한글 IME·한글 트리거 지원~~ → 영문 입력 전용 (002)

## 알려진 이슈

- (없음 — 구현 전)
- **예상 리스크**: 보안 SW 오탐, 자유 트리거 오치환(즉시 확장 모드)

## 기술 부채

- (없음 — 초기 상태)

## 현재 상태 요약

| 항목 | 상태 |
|------|------|
| Memory Bank | ✅ 요구사항 반영 완료 |
| 요구사항 | ✅ 전역 / 자유 트리거 / tkinter GUI |
| 소스 코드 | ✅ MVP 구현 완료 |
| 실행 가능 여부 | ✅ `python main.py` |
