"""Acceptance tests for Wikipedia adaptation row handling."""

from __future__ import annotations

import pytest

from src.collectors.wikipedia_adaptations import parse_adaptation_page


def test_recognized_header_row_is_not_counted_as_data_row() -> None:
    header_row = "<tr><th>Fiction work(s)</th><th>Film adaptation(s)</th></tr>"
    data_row = "<tr><td><i>Book</i></td><td><i>Film</i></td></tr>"
    table_html = "<table><tbody>" + header_row + data_row + "</tbody></table>"
    html = "<html><body>" + table_html + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.rows_inspected == 1


def test_additional_header_only_row_is_not_inspected() -> None:
    recognized_header_row = "<tr><th>Fiction work(s)</th><th>Film adaptation(s)</th></tr>"
    additional_header_row = "<tr><th>Books</th><th>Films</th></tr>"
    data_row = "<tr><td><i>Book</i></td><td><i>Film</i></td></tr>"
    table_html = (
        "<table><thead>"
        + recognized_header_row
        + "</thead><tbody>"
        + additional_header_row
        + data_row
        + "</tbody></table>"
    )
    html = "<html><body>" + table_html + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.rows_inspected == 1


def test_mixed_th_and_td_data_row_is_inspected() -> None:
    header_row = "<tr><th>Fiction work(s)</th><th>Film adaptation(s)</th></tr>"
    mixed_row = "<tr><th><i>Book</i></th><td><i>Film</i></td></tr>"
    table_html = "<table><thead>" + header_row + "</thead><tbody>" + mixed_row + "</tbody></table>"
    html = "<html><body>" + table_html + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.rows_inspected == 1


def test_rows_across_multiple_tbody_sections_preserve_document_order() -> None:
    header_row = "<tr><th>Fiction work(s)</th><th>Film adaptation(s)</th></tr>"
    first_row = "<tr><td><i>Book One</i></td><td><i>Film One</i></td></tr>"
    second_row = "<tr><td><i>Book Two</i></td><td><i>Film Two</i></td></tr>"
    table_html = (
        "<table><thead>"
        + header_row
        + "</thead><tbody>"
        + first_row
        + "</tbody><tbody>"
        + second_row
        + "</tbody></table>"
    )
    html = "<html><body>" + table_html + "</body></html>"
    result = parse_adaptation_page(html)

    assert result.pairs == [
        {"book_title": "Book One", "movie_title": "Film One"},
        {"book_title": "Book Two", "movie_title": "Film Two"},
    ]
