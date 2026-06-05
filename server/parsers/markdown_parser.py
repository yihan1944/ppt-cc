"""Markdown input parser."""

from __future__ import annotations

import re

from server.parsers.base import BaseParser


class MarkdownParser(BaseParser):
    """Parse Markdown text into plain text, preserving structure hints."""

    def parse(self, source: str) -> str:
        """Parse Markdown content into structured plain text.

        Converts headings to labeled sections, preserves bullet lists,
        and strips formatting while keeping logical structure.
        """
        lines = source.strip().split("\n")
        result: list[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                result.append("")
                continue

            # Headings → section markers
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                prefix = "#" * level
                result.append(f"{prefix} {text}")
                continue

            # Bullet lists (- or * or +)
            bullet_match = re.match(r"^(\s*)[-*+]\s+(.+)$", stripped)
            if bullet_match:
                indent = len(bullet_match.group(1))
                text = self._strip_inline_formatting(bullet_match.group(2))
                level = indent // 2
                prefix = "  " * level + "- "
                result.append(f"{prefix}{text}")
                continue

            # Numbered lists
            num_match = re.match(r"^(\s*)\d+[.)]\s+(.+)$", stripped)
            if num_match:
                text = self._strip_inline_formatting(num_match.group(2))
                result.append(f"- {text}")
                continue

            # Regular text
            result.append(self._strip_inline_formatting(stripped))

        return "\n".join(result)

    def can_handle(self, source: str, source_type: str) -> bool:
        if source_type == "markdown":
            return True
        # Check if source looks like markdown
        if source_type == "auto":
            heading_count = len(re.findall(r"^#{1,6}\s+", source, re.MULTILINE))
            bullet_count = len(re.findall(r"^[-*+]\s+", source, re.MULTILINE))
            return heading_count >= 2 or bullet_count >= 3
        return False

    @staticmethod
    def _strip_inline_formatting(text: str) -> str:
        """Remove markdown inline formatting (bold, italic, code, links)."""
        # Links [text](url) → text
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        # Images ![alt](url) → alt
        text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
        # Bold/italic ***text*** or **text** or *text*
        text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)
        # Inline code `text`
        text = re.sub(r"`([^`]+)`", r"\1", text)
        # Strikethrough ~~text~~
        text = re.sub(r"~~(.+?)~~", r"\1", text)
        return text.strip()
