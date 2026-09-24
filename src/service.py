from collections.abc import Callable

from src.buffer_chars import is_valid_trigger
from src.models import Shortcut
from src.repository import RepositoryError, ShortcutRepository

ERR_TRIGGER_ASCII = (
    "트리거는 영문·숫자·기호만 입력할 수 있습니다. (한글·공백 불가)"
)


class ValidationError(Exception):
    """단축어 검증 오류."""


class ShortcutService:
    def __init__(
        self,
        repository: ShortcutRepository,
        on_change: Callable[[dict[str, str]], None] | None = None,
    ) -> None:
        self._repository = repository
        self._on_change = on_change
        self._shortcuts: dict[str, str] = {}

    def load(self) -> None:
        self._shortcuts = self._repository.load()

    def list_all(self) -> list[Shortcut]:
        return [
            Shortcut(trigger=trigger, expansion=expansion)
            for trigger, expansion in sorted(self._shortcuts.items())
        ]

    def get_all(self) -> dict[str, str]:
        return dict(self._shortcuts)

    def add(self, trigger: str, expansion: str) -> None:
        trigger = trigger.strip()
        expansion = expansion.strip()
        self._validate(trigger, expansion, trigger_legacy=None)

        if trigger in self._shortcuts:
            raise ValidationError("이미 등록된 트리거입니다.")

        self._shortcuts[trigger] = expansion
        self._persist()

    def update(self, old_trigger: str, new_trigger: str, expansion: str) -> None:
        old_trigger = old_trigger.strip()
        new_trigger = new_trigger.strip()
        expansion = expansion.strip()
        self._validate(new_trigger, expansion, trigger_legacy=old_trigger)

        if old_trigger not in self._shortcuts:
            raise ValidationError("선택한 단축어를 찾을 수 없습니다.")

        if new_trigger != old_trigger and new_trigger in self._shortcuts:
            raise ValidationError("이미 등록된 트리거입니다.")

        if old_trigger != new_trigger:
            del self._shortcuts[old_trigger]

        self._shortcuts[new_trigger] = expansion
        self._persist()

    def remove(self, trigger: str) -> None:
        trigger = trigger.strip()
        if trigger not in self._shortcuts:
            raise ValidationError("선택한 단축어를 찾을 수 없습니다.")

        del self._shortcuts[trigger]
        self._persist()

    def _validate(
        self,
        trigger: str,
        expansion: str,
        *,
        trigger_legacy: str | None,
    ) -> None:
        if not trigger:
            raise ValidationError("트리거를 입력해 주세요.")
        if not expansion:
            raise ValidationError("확장 텍스트를 입력해 주세요.")
        if trigger_legacy is None or trigger != trigger_legacy:
            if not is_valid_trigger(trigger):
                raise ValidationError(ERR_TRIGGER_ASCII)

    def _persist(self) -> None:
        try:
            self._repository.save(self._shortcuts)
        except RepositoryError:
            raise
        if self._on_change:
            self._on_change(self.get_all())
