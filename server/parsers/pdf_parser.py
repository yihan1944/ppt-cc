"""PDF input parser using PyMuPDF."""

from __future__ import annotations

import os

from server.parsers.base import BaseParser


class PdfParser(BaseParser):
    """Extract text from PDF files."""

    def parse(self, source: str) -> str:
        """Extract text from a PDF file.

        Args:
            source: Path to the PDF file.

        Returns:
            Extracted text content.
        """
        import pymupdf

        if not os.path.exists(source):
            raise FileNotFoundError(f"PDF file not found: {source}")

        doc = pymupdf.open(source)
        pages: list[str] = []

        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            if text.strip():
                pages.append(f"--- Page {page_num + 1} ---\n{text.strip()}")

        doc.close()
        return "\n\n".join(pages)

    def can_handle(self, source: str, source_type: str) -> bool:
        if source_type == "pdf":
            return True
        if source_type == "auto" and os.path.isfile(source):
            return source.lower().endswith(".pdf")
        return False
