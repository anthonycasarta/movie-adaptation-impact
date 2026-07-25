"""Tests for Wikipedia index helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.collectors.wikipedia_index import WikipediaIndexError, parse_index_page


FIXTURES = Path(__file__).parent / "fixtures"


def _load_index_fixture() -> str:
    return (FIXTURES / "wikipedia_index.html").read_text(encoding="utf-8")


def test_parse_index_page_returns_expected_urls_in_order() -> None:
    html = _load_index_fixture()

    assert parse_index_page(html) == [
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)",
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)",
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)",
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)",
    ]


def test_parse_index_page_excludes_non_allowlisted_links_inside_books() -> None:
    html = _load_index_fixture().replace(
        '</ul>\n      </section>\n\n      <section aria-labelledby="short-stories-and-novellas">',
        '<li><a href="/wiki/Should_Not_Be_Selected">List of short stories adapted into films</a></li></ul>\n      </section>\n\n      <section aria-labelledby="short-stories-and-novellas">',
        1,
    )

    urls = parse_index_page(html)

    assert "https://en.wikipedia.org/wiki/Should_Not_Be_Selected" not in urls


def test_parse_index_page_normalizes_nested_anchor_text() -> None:
    html = (
        '<html><body><main><h2>Books</h2>'
        '<div><a href="/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)">'
        '<span>List of fiction works made into feature films</span> '
        '<span>(0–9, A–C)</span></a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)"><span>List of fiction works</span> '
        '<span>made into feature films (D–J)</span></a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</div></main></body></html>'
    )

    assert parse_index_page(html)[0].endswith("(0%E2%80%939,_A%E2%80%93C)")


@pytest.mark.parametrize(
    "href_value, expected",
    [
        ('/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)', "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)"),
        ('//en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)', "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)"),
        ('https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)', "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)"),
    ],
)
def test_parse_index_page_normalizes_supported_href_forms(href_value: str, expected: str) -> None:
    html = (
        '<html><body><main><h2>Books</h2>'
        f'<a href="{href_value}">List of fiction works made into feature films (0–9, A–C)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</main></body></html>'
    )

    assert parse_index_page(html)[0] == expected


def test_parse_index_page_rejects_missing_allowlisted_title() -> None:
    html = _load_index_fixture().replace(
        "List of fiction works made into feature films (S–Z)",
        "List of fiction works made into feature films (S–Z) missing",
    )

    with pytest.raises(WikipediaIndexError, match=r"Missing allowlisted titles: List of fiction works made into feature films \(S–Z\)"):
        parse_index_page(html)


def test_parse_index_page_rejects_duplicate_allowlisted_title() -> None:
    html = _load_index_fixture().replace(
        '</ul>\n      </section>\n\n      <section aria-labelledby="short-stories-and-novellas">',
        '<li><a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a></li></ul>\n      </section>\n\n      <section aria-labelledby="short-stories-and-novellas">',
        1,
    )

    with pytest.raises(WikipediaIndexError, match=r"Duplicate allowlisted title: List of fiction works made into feature films \(D–J\)"):
        parse_index_page(html)


def test_parse_index_page_rejects_duplicate_without_href_before_href_validation() -> None:
    html = _load_index_fixture().replace(
        '</ul>\n      </section>\n\n      <section aria-labelledby="short-stories-and-novellas">',
        '<li><a>List of fiction works made into feature films (D–J)</a></li></ul>\n      </section>\n\n      <section aria-labelledby="short-stories-and-novellas">',
        1,
    )

    with pytest.raises(WikipediaIndexError, match=r"Duplicate allowlisted title: List of fiction works made into feature films \(D–J\)"):
        parse_index_page(html)


def test_parse_index_page_does_not_mistake_table_of_contents_link_for_books_heading() -> None:
    html = '<html><body><a href="#Books">Books</a><h2>Comics</h2></body></html>'

    with pytest.raises(WikipediaIndexError, match="Books section"):
        parse_index_page(html)


def test_parse_index_page_rejects_missing_books_heading() -> None:
    html = '<html><body><h2>Comics</h2></body></html>'

    with pytest.raises(WikipediaIndexError, match="Books section"):
        parse_index_page(html)


def test_parse_index_page_recognizes_books_heading_with_edit_text() -> None:
    html = (
        '<html><body><main><h2>Books <span class="mw-editsection">[edit]</span></h2>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)">List of fiction works made into feature films (0–9, A–C)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</main></body></html>'
    )

    assert len(parse_index_page(html)) == 4


def test_parse_index_page_keeps_lower_level_headings_in_scope() -> None:
    html = (
        '<html><body><main><h2>Books</h2><div><h3>Subsection</h3>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)">List of fiction works made into feature films (0–9, A–C)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</div></main></body></html>'
    )

    assert len(parse_index_page(html)) == 4


@pytest.mark.parametrize("boundary_tag", ["h2", "h1"])
def test_parse_index_page_stops_at_equal_or_higher_boundary(boundary_tag: str) -> None:
    html = (
        '<html><body><main><h2>Books</h2><section>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)">List of fiction works made into feature films (0–9, A–C)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        f'</section><section><{boundary_tag}>Comics</{boundary_tag}>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</section></main></body></html>'
    )

    assert parse_index_page(html) == [
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)",
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)",
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)",
        "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)",
    ]


@pytest.mark.parametrize(
    "href_value",
    ["ABSENT", "", "   "],
)
def test_parse_index_page_rejects_missing_or_blank_href(href_value: str | None) -> None:
    if href_value == "ABSENT":
        first_link = '<a>List of fiction works made into feature films (0–9, A–C)</a>'
    else:
        first_link = f'<a href="{href_value}">List of fiction works made into feature films (0–9, A–C)</a>'

    html = (
        '<html><body><main><h2>Books</h2>'
        f'{first_link}'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</main></body></html>'
    )

    with pytest.raises(WikipediaIndexError, match="missing href"):
        parse_index_page(html)


@pytest.mark.parametrize(
    "href_value",
    [
        'http://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)',
        'https://example.com/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)',
        'https://en.wikipedia.org/w/index.php?title=List_of_fiction_works_made_into_feature_films_(0%E2%80%939,_A%E2%80%93C)',
    ],
)
def test_parse_index_page_rejects_invalid_urls(href_value: str) -> None:
    html = (
        '<html><body><main><h2>Books</h2>'
        f'<a href="{href_value}">List of fiction works made into feature films (0–9, A–C)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)">List of fiction works made into feature films (D–J)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)">List of fiction works made into feature films (K–R)</a>'
        '<a href="/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)">List of fiction works made into feature films (S–Z)</a>'
        '</main></body></html>'
    )

    with pytest.raises(WikipediaIndexError, match="Invalid Wikipedia URL"):
        parse_index_page(html)


@pytest.mark.parametrize("value", [None, 1, [], b"title"])
def test_parse_index_page_rejects_non_strings(value: object) -> None:
    with pytest.raises(TypeError):
        parse_index_page(value)  # type: ignore[arg-type]


def test_parse_index_page_does_not_use_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_request(*args: object, **kwargs: object) -> None:
        raise AssertionError("Network request attempted")

    monkeypatch.setattr("requests.get", fail_request)

    assert parse_index_page(_load_index_fixture())
