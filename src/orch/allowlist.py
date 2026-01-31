from __future__ import annotations

import re
import shlex
from dataclasses import dataclass


class DisallowedCommand(RuntimeError):
    pass


@dataclass(frozen=True)
class CommandAllowlist:
    patterns: tuple[re.Pattern[str], ...]

    @classmethod
    def from_regexes(cls, regexes: tuple[str, ...]) -> "CommandAllowlist":
        return cls(patterns=tuple(re.compile(r) for r in regexes))

    def check(self, command: str) -> None:
        # Normalize leading command token for simple matching.
        command = command.strip()
        if not command:
            raise DisallowedCommand("Empty command")

        # Avoid weird edge cases by ensuring it tokenizes.
        _ = shlex.split(command)

        if any(p.search(command) for p in self.patterns):
            return

        raise DisallowedCommand(
            "Command is not in allowlist. Refusing to run: " + command
        )
