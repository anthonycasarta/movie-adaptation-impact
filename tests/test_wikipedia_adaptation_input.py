"""Acceptance tests for Wikipedia adaptation parsing."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.collectors.wikipedia_adaptations import AdaptationParseResult, parse_adaptation_page


FIXTURES = Path(__file__).parent / "fixtures"


def _load_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_loads_fixture_locally_with_pathlib() -> None:
    html = _load_fixture("wikipedia_adaptations.html")

    assert "adaptation-table-standard" in html


@pytest.mark.parametrize("value", [None, 1, [], b"title"])
def test_rejects_non_string_input_before_html_parsing(value: object) -> None:
    with pytest.raises(TypeError):
        parse_adaptation_page(value)  # type: ignore[arg-type]


def test_supplied_html_is_parsed_without_network_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = _load_fixture("wikipedia_adaptations.html")

    def fail_request(*args: object, **kwargs: object) -> None:
        raise AssertionError("Network request attempted")

    monkeypatch.setattr("requests.get", fail_request)

    result = parse_adaptation_page(html)

    assert isinstance(result, AdaptationParseResult)
