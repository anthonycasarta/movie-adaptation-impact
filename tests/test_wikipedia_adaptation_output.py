"""Acceptance tests for Wikipedia adaptation output."""

from __future__ import annotations

from pathlib import Path

from src.collectors.wikipedia_adaptations import parse_adaptation_page


def test_parses_adaptation_fixture() -> None:
    html = (Path(__file__).parent / "fixtures" / "wikipedia_adaptations.html").read_text(
        encoding="utf-8"
    )

    result = parse_adaptation_page(html)

    assert result.pairs == [
        {"book_title": "Example Book", "movie_title": "Example Film"},
        {"book_title": "Multiple Adaptations Book", "movie_title": "First Film"},
        {"book_title": "Multiple Adaptations Book", "movie_title": "Second Film"},
        {"book_title": "Unlinked Book", "movie_title": "Unlinked Film"},
        {"book_title": "Les Misérables", "movie_title": "Les Misérables"},
        {"book_title": "Primary Title", "movie_title": "Primary Film"},
        {"book_title": "Metadata Book", "movie_title": "Metadata Film"},
        {"book_title": "Source Book", "movie_title": "Source Film"},
        {"book_title": "Source Book", "movie_title": "Third Film"},
    ]
    assert result.tables_parsed == 2
    assert result.rows_inspected == 12
    assert result.invalid_rows == 3
