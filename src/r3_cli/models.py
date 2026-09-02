from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ColourMode(StrEnum):
    AUTO = "auto"
    ALWAYS = "always"
    NEVER = "never"


class Level(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


@dataclass(frozen=True)
class Diagnostic:
    level: Level | str
    code: str
    message: str
    details: str | None = None
    hint: str | None = None
    data: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "level": str(self.level),
            "code": self.code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        if self.hint:
            result["hint"] = self.hint
        if self.data:
            result["data"] = self.data
        return result


class CliError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        code: str,
        details: str | None = None,
        hint: str | None = None,
        exit_code: int = 2,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = details
        self.hint = hint
        self.exit_code = exit_code

    def as_diagnostic(self) -> Diagnostic:
        return Diagnostic(Level.ERROR, self.code, str(self), self.details, self.hint)
