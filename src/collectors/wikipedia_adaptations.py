"""Wikipedia adaptation table parser contract."""

from __future__ import annotations

from dataclasses import dataclass


class WikipediaAdaptationError(RuntimeError):
    pass


@dataclass
class AdaptationParseResult:
    pairs: list[dict[str, str]]
    tables_parsed: int
    rows_inspected: int
    invalid_rows: int


def parse_adaptation_page(html: str) -> AdaptationParseResult:
    raise NotImplementedError("Step 11 will implement adaptation parsing")
