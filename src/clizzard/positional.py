from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Positional:
    """A positional CLI argument rendered to argv tokens."""

    name: str
    value: Any
    variadic: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Positional name must be a non-empty string")

    def to_argv(self) -> list[str]:
        if self.value is None:
            return []

        if isinstance(self.value, (list, tuple)):
            if not self.variadic:
                raise TypeError(
                    "List/tuple values require variadic=True to render repeated positional arguments"
                )

            return [str(item) for item in self.value]

        return [str(self.value)]
