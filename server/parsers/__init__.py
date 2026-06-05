"""Input parsers for various file formats."""

from __future__ import annotations

from server.parsers.base import BaseParser
from server.parsers.docx_parser import DocxParser
from server.parsers.markdown_parser import MarkdownParser
from server.parsers.pdf_parser import PdfParser
from server.parsers.url_parser import UrlParser

_PARSERS: list[BaseParser] = [
    UrlParser(),
    PdfParser(),
    DocxParser(),
    MarkdownParser(),
]


def parse_input(source: str, source_type: str = "auto") -> str:
    """Parse input from any supported format.

    Args:
        source: Text content, file path, or URL.
        source_type: Explicit type hint, or 'auto' to detect.

    Returns:
        Extracted plain text content.
    """
    # If source_type is 'text', return as-is
    if source_type == "text":
        return source

    # Try each parser
    for parser in _PARSERS:
        if parser.can_handle(source, source_type):
            return parser.parse(source)

    # Fallback: treat as plain text
    return source


__all__ = ["parse_input", "MarkdownParser", "PdfParser", "DocxParser", "UrlParser"]
