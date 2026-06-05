"""Base parser interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base for all input parsers."""

    @abstractmethod
    def parse(self, source: str) -> str:
        """Parse input source and return plain text content.

        Args:
            source: File path, URL, or raw text content.

        Returns:
            Extracted plain text.
        """
        ...

    @abstractmethod
    def can_handle(self, source: str, source_type: str) -> bool:
        """Check if this parser can handle the given source.

        Args:
            source: The input source.
            source_type: Explicit type hint (e.g. 'pdf', 'markdown').

        Returns:
            True if this parser can handle the source.
        """
        ...
