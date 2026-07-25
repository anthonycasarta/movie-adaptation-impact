"""Tests for text utilities."""

from __future__ import annotations

import pytest

from src.utils.text import normalize_title, title_comparison_key


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Pride &amp; Prejudice", "Pride & Prejudice"),
        ("  The\tGreat\n Gatsby  ", "The Great Gatsby"),
        ("Dune [1]", "Dune"),
        ("Dune [1][2]", "Dune"),
        ("Dune [1, 2]", "Dune"),
        ("Dune [1-3]", "Dune"),
        ("Dune [1–3]", "Dune"),
        ("It [novel]", "It [novel]"),
        (" [1] ", ""),
    ],
)
def test_normalize_title(raw: str, expected: str) -> None:
    assert normalize_title(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [None, 42, [], b"title"],
)
def test_normalize_title_rejects_non_strings(raw: object) -> None:
    with pytest.raises(TypeError):
        normalize_title(raw)  # type: ignore[arg-type]


def test_normalize_title_preserves_unicode_and_punctuation() -> None:
    assert normalize_title("  Les Misérables: L'Œuvre [1]  ") == "Les Misérables: L'Œuvre"


def test_title_comparison_key_uses_casefolded_normalized_title() -> None:
    assert title_comparison_key("DUNE [1]") == "dune"
    assert title_comparison_key("Straße") == "strasse"


def test_title_comparison_key_is_case_insensitive() -> None:
    assert title_comparison_key("Dune") == title_comparison_key("DUNE")


def test_title_comparison_key_does_not_modify_display_title() -> None:
    raw = "  Pride &amp; Prejudice [1]  "
    display_title = normalize_title(raw)

    assert display_title == "Pride & Prejudice"
    assert title_comparison_key(raw) == "pride & prejudice"
    assert display_title == "Pride & Prejudice"
