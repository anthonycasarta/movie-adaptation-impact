"""Acceptance tests for Wikipedia adaptation parsing."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.collectors.wikipedia_adaptations import AdaptationParseResult, WikipediaAdaptationError, parse_adaptation_page


def _load_fixture(name: str) -> str:
    return (Path(__file__).parent / "fixtures" / name).read_text(encoding="utf-8")


def test_rejects_non_string_input_before_html_parsing() -> None:
    with pytest.raises(TypeError):
        parse_adaptation_page(None)  # type: ignore[arg-type]


def test_fixture_parsing_returns_expected_pairs_and_counts() -> None:
    html = _load_fixture("wikipedia_adaptations.html")

    result = parse_adaptation_page(html)

    assert isinstance(result, AdaptationParseResult)
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


def test_unrecognized_table_raises_error() -> None:
    html = "<html><body><table><thead><tr><th>Nothing</th><th>Else</th></tr></thead></table></body></html>"

    with pytest.raises(WikipediaAdaptationError):
        parse_adaptation_page(html)
