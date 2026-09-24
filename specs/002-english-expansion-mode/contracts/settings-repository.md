# Contract: Settings Repository

**Module**: `src/settings.py` (신규)  
**Feature**: 002-english-expansion-mode

## Path

- Same directory as shortcuts: `get_data_path().parent / "settings.json"` or sibling `settings.json` next to `shortcuts.json` under `data/`.

## API

```python
DEFAULT_SETTINGS = ExpansionSettings(mode="on_key", expansion_key="space")

class SettingsRepository:
    def __init__(self, path: Path) -> None: ...
    def load(self) -> ExpansionSettings: ...
    def save(self, settings: ExpansionSettings) -> None: ...
```

## Load Semantics

| Condition | Result |
|-----------|--------|
| File missing | Return `DEFAULT_SETTINGS`; do not auto-create until save |
| Invalid JSON | Raise `RepositoryError` (same pattern as shortcuts) |
| Unknown `expansion_mode` / `expansion_key` | Fall back field to default; if all invalid, return `DEFAULT_SETTINGS` |
| Missing fields | Merge with defaults per field |

## Save Semantics

- Write JSON UTF-8, `ensure_ascii=False`, indent 2
- Payload shape:
  ```json
  { "version": 1, "expansion_mode": "...", "expansion_key": "..." }
  ```
- Atomic write not required for 1차 (match shortcuts repository)

## Serialization Mapping

| JSON field | Dataclass field |
|------------|-----------------|
| `expansion_mode` | `mode` |
| `expansion_key` | `expansion_key` |
