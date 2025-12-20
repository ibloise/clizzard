from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .option import Option


@dataclass(frozen=True, slots=True)
class Command:
    exe: str
    subcommands: Sequence[str] = field(default_factory=tuple)
    options: Sequence[Option] = field(default_factory=tuple)
    args: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.exe or not str(self.exe).strip():
            raise ValueError("Command exe mus be a non-empty string")

    def to_argv(self) -> list[str]:
        argv: list[str] = [self.exe]

        argv.extend([str(s) for s in self.subcommands])

        for opt in self.options:
            argv.extend(opt.to_argv())

        argv.extend([str(a) for a in self.args])
        return argv

    def to_string(self) -> str:
        return " ".join(self.to_argv())
