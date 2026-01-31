from __future__ import annotations

from enum import Enum


class Step(str, Enum):
    INTAKE = "INTAKE"
    PLAN = "PLAN"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    REVIEW = "REVIEW"
    FIXLOOP = "FIXLOOP"
    GATE = "GATE"
    PUBLISH = "PUBLISH"
