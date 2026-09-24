"""GUI 문자열 상수 (한국어)."""

APP_TITLE = "단축어 프로그램"

# 버튼
BTN_ADD = "추가"
BTN_EDIT = "수정"
BTN_DELETE = "삭제"
BTN_SAVE = "저장"
BTN_CANCEL = "취소"

# 라벨
LBL_TRIGGER = "트리거"
LBL_EXPANSION = "확장 텍스트"
LBL_SERVICE = "전역 확장 서비스"
LBL_STATUS_RUNNING = "실행 중"
LBL_STATUS_STOPPED = "중지됨"
LBL_STATUS_ERROR = "오류"

# 컬럼
COL_TRIGGER = "트리거"
COL_EXPANSION = "확장 텍스트"

# 다이얼로그
DLG_ADD_TITLE = "단축어 추가"
DLG_EDIT_TITLE = "단축어 수정"
DLG_DELETE_TITLE = "단축어 삭제"
DLG_DELETE_CONFIRM = "선택한 단축어를 삭제하시겠습니까?"

# 안내
INFO_TRIGGER_TIP = (
    "짧은 일반 단어는 의도치 않은 치환이 발생할 수 있습니다. "
    "긴·고유한 트리거(예: myaddr, 회사서명) 사용을 권장합니다."
)
INFO_MVP_ENGLISH = (
    "현재 MVP는 영문·숫자 트리거만 자동 확장됩니다. "
    "한글 트리거 지원은 추후 업데이트 예정입니다."
)

# 오류
ERR_EMPTY_TRIGGER = "트리거를 입력해 주세요."
ERR_EMPTY_EXPANSION = "확장 텍스트를 입력해 주세요."
ERR_DUPLICATE_TRIGGER = "이미 등록된 트리거입니다."
ERR_NOT_FOUND = "선택한 단축어를 찾을 수 없습니다."
ERR_NO_SELECTION = "목록에서 단축어를 선택해 주세요."
ERR_HOOK_FAILED = (
    "키보드 후킹을 시작할 수 없습니다. "
    "관리자 권한 또는 백신 프로그램 설정을 확인해 주세요."
)
ERR_REPOSITORY = "단축어 파일을 읽거나 저장하는 중 오류가 발생했습니다."

# 성공
MSG_SAVED = "저장되었습니다."
MSG_DELETED = "삭제되었습니다."
