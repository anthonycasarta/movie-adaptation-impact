"""Text utility module."""

from __future__ import annotations

import html
import re


_CITATION_RE = re.compile(r"(?:\s*\[(?:\d+(?:[–-]\d+)?(?:,\s*\d+(?:[–-]\d+)?)*)\])+")
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_title(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    text = html.unescape(value)
    text = _CITATION_RE.sub("", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def title_comparison_key(value: str) -> str:
    return normalize_title(value).casefold()
