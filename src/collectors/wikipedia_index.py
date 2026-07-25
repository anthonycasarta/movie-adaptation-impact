"""Wikipedia index parsing helpers."""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

WIKIPEDIA_BASE_URL = "https://en.wikipedia.org"

WIKIPEDIA_INDEX_URL = (
    "https://en.wikipedia.org/wiki/"
    "Lists_of_works_of_fiction_made_into_feature_films"
)

ALLOWED_BOOK_LIST_TITLES = frozenset(
    {
        "List of fiction works made into feature films (0–9, A–C)",
        "List of fiction works made into feature films (D–J)",
        "List of fiction works made into feature films (K–R)",
        "List of fiction works made into feature films (S–Z)",
    }
)


class WikipediaIndexError(Exception):
    """Raised when the Wikipedia index page structure is invalid."""


def parse_index_page(html: str) -> list[str]:
    if not isinstance(html, str):
        raise TypeError("html must be a string")

    soup = BeautifulSoup(html, "html.parser")
    books_heading = _find_books_heading(soup)
    if books_heading is None:
        raise WikipediaIndexError("Could not find a Books section")

    allowed_titles_in_order = []
    url_by_title = {}
    counts_by_title = {title: 0 for title in ALLOWED_BOOK_LIST_TITLES}

    for anchor in _iter_section_anchors(books_heading):
        displayed_text = " ".join(anchor.stripped_strings)
        if displayed_text not in ALLOWED_BOOK_LIST_TITLES:
            continue

        counts_by_title[displayed_text] += 1
        if counts_by_title[displayed_text] > 1:
            raise WikipediaIndexError(f"Duplicate allowlisted title: {displayed_text}")

        href = anchor.get("href")
        if not isinstance(href, str) or not href.strip():
            raise WikipediaIndexError(f"Allowlisted title missing href: {displayed_text}")

        absolute_url = urljoin(WIKIPEDIA_BASE_URL, href)
        parsed_url = urlparse(absolute_url)
        if parsed_url.scheme != "https" or parsed_url.netloc != "en.wikipedia.org" or not parsed_url.path.startswith("/wiki/"):
            raise WikipediaIndexError(f"Invalid Wikipedia URL for allowlisted title: {displayed_text}")

        allowed_titles_in_order.append(displayed_text)
        url_by_title[displayed_text] = absolute_url

    missing_titles = sorted(title for title, count in counts_by_title.items() if count == 0)
    if missing_titles:
        raise WikipediaIndexError(f"Missing allowlisted titles: {', '.join(missing_titles)}")

    return [url_by_title[title] for title in allowed_titles_in_order]


def _find_books_heading(soup: BeautifulSoup):
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        heading_text = " ".join(heading.stripped_strings).replace("[edit]", "").strip()
        heading_id = heading.get("id")
        if heading_id == "Books" or heading_id == "books" or heading_text == "Books":
            return heading
    return None


def _iter_section_anchors(heading):
    heading_level = int(heading.name[1])
    for element in heading.next_elements:
        if element is heading:
            continue
        element_name = getattr(element, "name", None)
        if element_name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            if int(element_name[1]) <= heading_level:
                break
            continue
        if element_name == "a":
            yield element
