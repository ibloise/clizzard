from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_VALID_PREFIXES = {"-", "--"}


@dataclass(frozen=True, slots=True)
class Option:
    """
    A CLI option rendered to argv tokens.

    Semantics:
    - value is True  -> emits flag only         ["--verbose"]
    - value is False -> emits nothing           []
    - value is None  -> emits nothing           []
    - value is scalar -> emits flag + value     ["--threads", "4"]
    - value is list/tuple -> requires repeatable=True, emits repeated pairs
      ["--include", "a", "--include", "b"]

    Name normalization (optional):
    - replace '_' with '-' when normalize_name=True
    """

    name: str
    value: Any = True
    prefix: str = "--"
    repeatable: bool = False
    normalize_name: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Option name must be a non-empty string")

        if self.prefix not in _VALID_PREFIXES:
            raise ValueError(
                f"Invalid prefix {self.prefix!r}. Use one of: {_VALID_PREFIXES}"
            )

        if self.normalize_name and "_" in self.name:
            object.__setattr__(self, "name", self.name.replace("_", "-"))

    def flag(self) -> str:
        return f"{self.prefix}{self.name}"

    def to_argv(self) -> list[str]:
        if self.value is False or self.value is None:
            return []

        flag = self.flag()

        if self.value is True:
            return [flag]

        if isinstance(self.value, (list, tuple)):
            if not self.repeatable:
                raise TypeError(
                    "List/tuple values require repetable=True to render repeated options"
                )

            argv: list[str] = []

            for item in self.value:  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                argv.extend([flag, str(item)])  # pyright: ignore[reportUnknownArgumentType]

            return argv

        return [flag, str(self.value)]
