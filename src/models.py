from dataclasses import dataclass


@dataclass(frozen=True)
class Shortcut:
    trigger: str
    expansion: str
