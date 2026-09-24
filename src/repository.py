import json
from pathlib import Path


class RepositoryError(Exception):
    """JSON 파일 읽기/쓰기 오류."""


class ShortcutRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> dict[str, str]:
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self.save({})
            return {}

        try:
            raw = self._path.read_text(encoding="utf-8")
            if not raw.strip():
                return {}
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RepositoryError(f"JSON 파싱 오류: {self._path}") from exc
        except OSError as exc:
            raise RepositoryError(f"파일 읽기 오류: {self._path}") from exc

        shortcuts = data.get("shortcuts", {})
        if not isinstance(shortcuts, dict):
            raise RepositoryError("shortcuts 필드 형식이 올바르지 않습니다.")

        return {str(k): str(v) for k, v in shortcuts.items()}

    def save(self, shortcuts: dict[str, str]) -> None:
        payload = {"version": 1, "shortcuts": shortcuts}
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            raise RepositoryError(f"파일 저장 오류: {self._path}") from exc
