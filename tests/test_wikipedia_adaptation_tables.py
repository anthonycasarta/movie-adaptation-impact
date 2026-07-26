"""Acceptance tests for Wikipedia adaptation table recognition."""

from __future__ import annotations

import pytest

from src.collectors.wikipedia_adaptations import WikipediaAdaptationError, parse_adaptation_page


def _table_fragment(
    first_header: str,
    second_header: str,
    *,
    first_title: str = "Book",
    second_title: str = "Film",
    header_section: str = "thead",
) -> str:
    header_row = "<tr><th>" + first_header + "</th><th>" + second_header + "</th></tr>"
    data_row = "<tr><td><i>" + first_title + "</i></td><td><i>" + second_title + "</i></td></tr>"

    if header_section == "tbody":
        return "<table><tbody>" + header_row + data_row + "</tbody></table>"

    return "<table><thead>" + header_row + "</thead><tbody>" + data_row + "</tbody></table>"


@pytest.mark.parametrize("header_section", ["thead", "tbody"])
def test_exact_required_headers_are_recognized_in_thead_and_tbody(header_section: str) -> None:
    table_fragment = _table_fragment(
        "Fiction work(s)",
        "Film adaptation(s)",
        header_section=header_section,
    )
    html = "<html><body>" + table_fragment + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.tables_parsed == 1


def test_nested_markup_and_extra_whitespace_are_normalized() -> None:
    table_fragment = _table_fragment(
        "<span>  Fiction  </span>   work(s)",
        "<span>  Film  </span>   adaptation(s)",
    )
    html = "<html><body>" + table_fragment + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.tables_parsed == 1


@pytest.mark.parametrize(
    "book_header,movie_header,missing_header",
    [
        ("fiction work(s)", "Film adaptation(s)", "Fiction work(s)"),
        ("Fiction work(s)", "film adaptation(s)", "Film adaptation(s)"),
    ],
)
def test_case_sensitive_headers_raise_missing_exact_header(
    book_header: str, movie_header: str, missing_header: str
) -> None:
    table_fragment = _table_fragment(book_header, movie_header)
    html = "<html><body>" + table_fragment + "</body></html>"

    with pytest.raises(WikipediaAdaptationError) as exc_info:
        parse_adaptation_page(html)

    assert missing_header in str(exc_info.value)


def test_split_header_rows_raise_same_physical_row_error() -> None:
    book_header_row = "<tr><th>Fiction work(s)</th></tr>"
    movie_header_row = "<tr><th>Film adaptation(s)</th></tr>"
    table_html = "<table><thead>" + book_header_row + movie_header_row + "</thead></table>"
    html = "<html><body>" + table_html + "</body></html>"

    with pytest.raises(WikipediaAdaptationError) as exc_info:
        parse_adaptation_page(html)

    assert "same physical row" in str(exc_info.value)


def test_reversed_required_column_order_preserves_mapping() -> None:
    table_fragment = _table_fragment(
        "Film adaptation(s)",
        "Fiction work(s)",
        first_title="Film",
        second_title="Book",
    )
    html = "<html><body>" + table_fragment + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.tables_parsed == 1
    assert result.pairs == [{"book_title": "Book", "movie_title": "Film"}]


def test_unrelated_columns_do_not_change_mapping() -> None:
    header_row = "<tr><th>Notes</th><th>Fiction work(s)</th><th>Year</th><th>Film adaptation(s)</th><th>Source</th></tr>"
    data_row = "<tr><td>n</td><td><i>Book</i></td><td>2001</td><td><i>Film</i></td><td>s</td></tr>"
    table_html = "<table><thead>" + header_row + "</thead><tbody>" + data_row + "</tbody></table>"
    html = "<html><body>" + table_html + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.tables_parsed == 1
    assert result.pairs == [{"book_title": "Book", "movie_title": "Film"}]


def test_unrelated_table_is_ignored_when_valid_table_exists() -> None:
    unrelated_table = "<table><thead><tr><th>Nothing</th><th>Else</th></tr></thead></table>"
    valid_table = _table_fragment("Fiction work(s)", "Film adaptation(s)")
    html = "<html><body>" + unrelated_table + valid_table + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.tables_parsed == 1
    assert result.pairs == [{"book_title": "Book", "movie_title": "Film"}]
