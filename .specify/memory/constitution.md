# 단축어 프로그램 Constitution

## Core Principles

### I. Windows 전역 텍스트 확장
메모장, 브라우저, 채팅 앱 등 **Windows 어디서든** 동작해야 한다. 전역 키보드 후킹(pynput)은 핵심 기능이며 제거·약화하지 않는다.

### II. 자유 트리거
트리거에 접두사(`;`, `@@` 등)를 **강제하지 않는다**. 사용자가 원하는 문자열을 등록할 수 있어야 하며, 오치환 위험은 GUI 안내로 완화한다.

### III. 레이어 분리
Repository → Service → Expander / KeyboardHook / GUI 구조를 유지한다. GUI와 전역 Hook은 **동일 Service·Repository**를 공유한다.

### IV. 영속 저장
단축어 매핑은 JSON(`shortcuts.json`)에 저장하고, 재시작 후에도 유지되어야 한다. CRUD 후 Hook에 **reload**가 필요하다.

### V. 단순함 (YAGNI)
클라우드 동기화, 다중 사용자, 고급 매크로(조건문·변수)는 범위 밖이다. MVP 이후에도 불필요한 추상화를 추가하지 않는다.

## 기술 제약

| 영역 | 선택 |
|------|------|
| 언어 | Python 3.10+ (타입 힌트) |
| GUI | tkinter (표준 라이브러리) |
| 전역 입력 | pynput |
| 저장 | JSON (stdlib) |
| OS | Windows 10/11 우선 |

## 구현 규칙

- GUI mainloop와 pynput listener는 **스레드 분리**한다.
- 트리거 매칭: InputBuffer **suffix** + **최장 트리거 우선**.
- 트리거 매칭: **영문(ASCII printable)** 입력만 버퍼에 반영.
- 확장 모드: **즉시 확장** 또는 **키 입력 후 확장**(Space/Enter/Tab) — `settings.json`에 영속.
- 사용자-facing 메시지는 **한국어**로 작성한다.

## Memory Bank 연동

Spec Kit 작업 시 다음 파일을 상시 컨텍스트로 참고한다:

- `.cursor/rules/projectbrief.md` — 프로젝트 목적·범위
- `.cursor/rules/systemPatterns.md` — 아키텍처·모듈 역할
- `.cursor/rules/activeContext.md` — 현재 작업 포커스
- `.cursor/rules/progress.md` — 완료·남은 작업

기능별 명세(`specs/`)는 Spec Kit으로 관리하고, 프로젝트 전체 상태는 Memory Bank로 유지한다.

## Governance

- Constitution은 plan·analyze 단계의 판단 기준이다.
- 기존 아키텍처·공개 동작과 충돌하는 변경은 spec에서 **호환성 경계**를 명시해야 한다.
- 기능 완료 후 `activeContext.md`, `progress.md`를 갱신한다.

**Version**: 1.0.0 | **Ratified**: 2026-09-24 | **Last Amended**: 2026-09-24
