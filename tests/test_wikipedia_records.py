"""Tests for record finalization."""

from __future__ import annotations

from src.collectors.wikipedia_records import finalize_records


def test_finalize_records_deduplicates_by_combined_title_key() -> None:
    records = [
        {"book_title": "Dune", "movie_title": "Dune"},
        {"book_title": "dune [1]", "movie_title": "DUNE"},
        {"book_title": "Dune", "movie_title": "Children of Dune"},
        {"book_title": "Foundation", "movie_title": "Dune"},
    ]

    result = finalize_records(records)

    assert {"book_title": "Dune", "movie_title": "Dune"} in result
    assert {"book_title": "Dune", "movie_title": "Children of Dune"} in result
    assert {"book_title": "Foundation", "movie_title": "Dune"} in result
    assert len(result) == 3
