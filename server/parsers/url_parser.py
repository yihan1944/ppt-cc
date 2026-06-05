"""URL/HTML input parser."""

from __future__ import annotations

import re

from server.parsers.base import BaseParser


class UrlParser(BaseParser):
    """Extract main text content from a web page."""

    def parse(self, source: str) -> str:
        """Fetch and extract text content from a URL.

        Args:
            source: URL to fetch.

        Returns:
            Extracted main text content.
        """
        import httpx
        from bs4 import BeautifulSoup

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            response = client.get(source, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove script, style, nav, footer, header elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        # Try to find main content area
        main = soup.find("main") or soup.find("article") or soup.find("body")
        if not main:
            main = soup

        # Extract text with some structure
        lines: list[str] = []
        for element in main.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
            text = element.get_text(strip=True)
            if not text:
                continue

            tag_name = element.name
            if tag_name == "h1":
                lines.append(f"# {text}")
            elif tag_name == "h2":
                lines.append(f"## {text}")
            elif tag_name in ("h3", "h4", "h5", "h6"):
                lines.append(f"### {text}")
            elif tag_name == "li":
                lines.append(f"- {text}")
            else:
                lines.append(text)

        return "\n".join(lines)

    def can_handle(self, source: str, source_type: str) -> bool:
        if source_type == "url":
            return True
        if source_type == "auto":
            return bool(re.match(r"https?://", source.strip()))
        return False
