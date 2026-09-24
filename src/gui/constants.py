"""GUI 문자열 상수 (한국어)."""

APP_TITLE = "단축어 프로그램"

# 버튼
BTN_ADD = "추가"
BTN_EDIT = "수정"
BTN_DELETE = "삭제"
BTN_SAVE = "저장"
BTN_CANCEL = "취소"
BTN_SAVE_SETTINGS = "설정 저장"

# 라벨
LBL_TRIGGER = "트리거"
LBL_EXPANSION = "확장 텍스트"
LBL_SERVICE = "전역 확장 서비스"
LBL_EXPANSION_MODE = "확장 모드"
LBL_EXPANSION_KEY = "확장 키"
LBL_STATUS_RUNNING = "실행 중"
LBL_STATUS_STOPPED = "중지됨"
LBL_STATUS_ERROR = "오류"

# 확장 모드
MODE_IMMEDIATE = "즉시 확장"
MODE_ON_KEY = "키 입력 후 확장"

# 확장 키 표시
KEY_SPACE = "스페이스"
KEY_ENTER = "Enter"
KEY_TAB = "Tab"

EXPANSION_KEY_LABELS = {
    "space": KEY_SPACE,
    "enter": KEY_ENTER,
    "tab": KEY_TAB,
}

EXPANSION_KEY_BY_LABEL = {label: key for key, label in EXPANSION_KEY_LABELS.items()}
EXPANSION_KEY_COMBO_VALUES = list(EXPANSION_KEY_LABELS.values())

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
    "긴·고유한 트리거(예: myaddr, myemail) 사용을 권장합니다."
)
INFO_ENGLISH_ONLY = (
    "트리거는 영문(라틴 알파벳)·숫자·기호 입력만 지원합니다. "
    "한글 트리거는 등록·매칭되지 않습니다. 확장 결과는 한글·여러 줄도 가능합니다."
)
INFO_IMMEDIATE_MODE_WARNING = (
    "「즉시 확장」 모드는 트리거 마지막 글자 입력 직후 치환됩니다. "
    "오치환 위험이 높을 수 있으니 고유한 트리거를 사용하세요."
)
INFO_TRIGGER_ENGLISH = "영문·숫자·기호로 입력하세요."

# 오류
ERR_EMPTY_TRIGGER = "트리거를 입력해 주세요."
ERR_TRIGGER_ASCII = (
    "트리거는 영문·숫자·기호만 입력할 수 있습니다. (한글·공백 불가)"
)
ERR_EMPTY_EXPANSION = "확장 텍스트를 입력해 주세요."
ERR_DUPLICATE_TRIGGER = "이미 등록된 트리거입니다."
ERR_NOT_FOUND = "선택한 단축어를 찾을 수 없습니다."
ERR_NO_SELECTION = "목록에서 단축어를 선택해 주세요."
ERR_HOOK_FAILED = (
    "키보드 후킹을 시작할 수 없습니다. "
    "관리자 권한 또는 백신 프로그램 설정을 확인해 주세요."
)
ERR_REPOSITORY = "단축어 파일을 읽거나 저장하는 중 오류가 발생했습니다."
ERR_SETTINGS = "설정 파일을 읽거나 저장하는 중 오류가 발생했습니다."

# 성공
MSG_SAVED = "저장되었습니다."
MSG_DELETED = "삭제되었습니다."
MSG_SETTINGS_SAVED = "설정이 저장되었습니다."
