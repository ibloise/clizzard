from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .option import Option
from .positional import Positional


@dataclass(frozen=True, slots=True)
class Command:
    exe: str
    subcommands: Sequence[str] = field(default_factory=tuple)
    options: Sequence[Option] = field(default_factory=tuple)
    args: Sequence[str | Positional] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.exe or not str(self.exe).strip():
            raise ValueError("Command exe mus be a non-empty string")

    def to_argv(self) -> list[str]:
        argv: list[str] = [self.exe]

        argv.extend([str(s) for s in self.subcommands])

        for opt in self.options:
            argv.extend(opt.to_argv())

        for arg in self.args:
            if isinstance(arg, Positional):
                argv.extend(arg.to_argv())
            else:
                argv.append(str(arg))
        return argv

    def to_string(self) -> str:
        return " ".join(self.to_argv())
