"""Wikipedia adaptation table parser."""

from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

from src.utils.text import normalize_title


class WikipediaAdaptationError(RuntimeError):
    pass


@dataclass
class AdaptationParseResult:
    pairs: list[dict[str, str]]
    tables_parsed: int
    rows_inspected: int
    invalid_rows: int


def parse_adaptation_page(html: str) -> AdaptationParseResult:
    if not isinstance(html, str):
        raise TypeError("html must be a string")

    soup = BeautifulSoup(html, "html.parser")
    pairs: list[dict[str, str]] = []
    tables_parsed = 0
    rows_inspected = 0
    invalid_rows = 0
    deferred_error: WikipediaAdaptationError | None = None

    for table in soup.find_all("table"):
        if table.find_parent("table") is not None:
            continue

        classification = _classify_table(table)
        if classification is None:
            continue

        if classification[0] == "error":
            deferred_error = classification[1]
            continue

        header_row, book_index, movie_index = classification[1]
        tables_parsed += 1
        explicit_book: str | None = None
        carried_book: str | None = None
        carried_rows = 0

        for row in _table_rows(table):
            if row is header_row:
                continue

            cells = row.find_all(["th", "td"], recursive=False)
            if not cells:
                rows_inspected += 1
                invalid_rows += 1
                if carried_rows > 0:
                    carried_rows -= 1
                    if carried_rows == 0:
                        carried_book = None
                continue

            if _header_only_row(cells):
                continue

            rows_inspected += 1

            if carried_rows > 0:
                carried_rows -= 1
                if len(cells) == 1:
                    movie_title = _extract_title(cells[0])
                    if carried_book and movie_title:
                        pairs.append({"book_title": carried_book, "movie_title": movie_title})
                    else:
                        invalid_rows += 1
                    if carried_rows == 0:
                        carried_book = None
                    continue
                invalid_rows += 1
                if carried_rows == 0:
                    carried_book = None
                continue

            if len(cells) <= max(book_index, movie_index):
                invalid_rows += 1
                continue

            book_cell = cells[book_index]
            movie_cell = cells[movie_index]
            book_title = _extract_title(book_cell)
            movie_title = _extract_title(movie_cell)

            if _is_same_as_above(book_cell):
                if explicit_book is None:
                    invalid_rows += 1
                    continue
                book_title = explicit_book

            if not book_title or not movie_title:
                invalid_rows += 1
                continue

            pairs.append({"book_title": book_title, "movie_title": movie_title})
            explicit_book = book_title if not _is_same_as_above(book_cell) else explicit_book

            rowspan = _parse_rowspan(book_cell.get("rowspan"))
            if rowspan > 1:
                carried_book = book_title
                carried_rows = rowspan - 1

    if tables_parsed == 0:
        if deferred_error is not None:
            raise deferred_error
        raise WikipediaAdaptationError("no recognizable adaptation table was found")

    if not pairs and deferred_error is not None:
        raise deferred_error

    return AdaptationParseResult(
        pairs=pairs,
        tables_parsed=tables_parsed,
        rows_inspected=rows_inspected,
        invalid_rows=invalid_rows,
    )


def _classify_table(table: Tag) -> tuple[str, WikipediaAdaptationError] | tuple[str, tuple[Tag, int, int]] | None:
    seen_book_row: Tag | None = None
    seen_movie_row: Tag | None = None

    for row in _table_rows(table):
        headers = row.find_all("th", recursive=False)
        if not headers:
            continue
        texts = [" ".join(header.stripped_strings) for header in headers]
        has_book = "Fiction work(s)" in texts
        has_movie = "Film adaptation(s)" in texts
        if has_book and has_movie:
            return "ok", (row, texts.index("Fiction work(s)"), texts.index("Film adaptation(s)"))
        if has_book:
            seen_book_row = row
        if has_movie:
            seen_movie_row = row

    if seen_book_row is not None and seen_movie_row is not None:
        return "error", WikipediaAdaptationError("required headers must appear in the same physical row")
    if seen_book_row is not None:
        return "error", WikipediaAdaptationError("missing required header: Film adaptation(s)")
    if seen_movie_row is not None:
        return "error", WikipediaAdaptationError("missing required header: Fiction work(s)")
    return None


def _table_rows(table: Tag) -> list[Tag]:
    rows: list[Tag] = []
    for section in table.find_all(["thead", "tbody", "tfoot"], recursive=False):
        rows.extend(section.find_all("tr", recursive=False))
    if not rows:
        rows.extend(table.find_all("tr", recursive=False))
    return rows


def _header_only_row(cells: list[Tag]) -> bool:
    return all(cell.name == "th" for cell in cells)


def _extract_title(cell: Tag) -> str:
    italic = cell.find("i")
    if italic is None:
        return ""

    link = italic.find("a")
    if link is not None:
        title = normalize_title(" ".join(link.stripped_strings))
        if title:
            return title

    return normalize_title(" ".join(italic.stripped_strings))


def _is_same_as_above(cell: Tag) -> bool:
    return normalize_title(" ".join(cell.stripped_strings)).casefold() == "same as above"


def _parse_rowspan(value: object) -> int:
    if value is None:
        return 1
    if not isinstance(value, str) or not value.isascii() or not value.isdigit():
        return 1
    parsed = int(value)
    return parsed if parsed > 0 else 1
