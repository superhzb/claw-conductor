from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CodexStatus:
    raw: str
    model: str | None
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    cost_usd: float | None
    elapsed_s: float | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cost_usd": self.cost_usd,
            "elapsed_s": self.elapsed_s,
        }


_MODEL_RE = re.compile(r"^Model:\s*(?P<v>.+?)\s*$", re.M)
_IN_RE = re.compile(r"^Input tokens:\s*(?P<v>\d+)\s*$", re.M)
_OUT_RE = re.compile(r"^Output tokens:\s*(?P<v>\d+)\s*$", re.M)
_TOTAL_RE = re.compile(r"^Total tokens:\s*(?P<v>\d+)\s*$", re.M)
_COST_RE = re.compile(r"^Cost \(USD\):\s*\$?(?P<v>[0-9.]+)\s*$", re.M)
_ELAPSED_RE = re.compile(r"^Elapsed:\s*(?P<v>[0-9.]+)s\s*$", re.M)


def parse_codex_status(text: str) -> CodexStatus:
    def m(rex: re.Pattern[str]) -> str | None:
        mm = rex.search(text)
        return mm.group("v") if mm else None

    model = m(_MODEL_RE)
    input_tokens = int(m(_IN_RE)) if m(_IN_RE) else None
    output_tokens = int(m(_OUT_RE)) if m(_OUT_RE) else None
    total_tokens = int(m(_TOTAL_RE)) if m(_TOTAL_RE) else None
    cost_usd = float(m(_COST_RE)) if m(_COST_RE) else None
    elapsed_s = float(m(_ELAPSED_RE)) if m(_ELAPSED_RE) else None

    return CodexStatus(
        raw=text,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
        elapsed_s=elapsed_s,
    )
