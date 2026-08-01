"""Wikipedia record finalization helpers."""

from __future__ import annotations

from src.utils.text import title_comparison_key


def finalize_records(records: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    finalized: list[dict[str, str]] = []

    for record in records:
        key = (
            title_comparison_key(record["book_title"]),
            title_comparison_key(record["movie_title"]),
        )
        if key in seen:
            continue
        seen.add(key)
        finalized.append(record)

    return sorted(finalized, key=lambda record: (record["book_title"], record["movie_title"]))
