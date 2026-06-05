"""Theme registry."""

from __future__ import annotations

from server.renderer.themes.base import Theme
from server.renderer.themes.consulting import ConsultingTheme

_THEMES: dict[str, type[Theme]] = {
    "consulting": ConsultingTheme,
}


def get_theme(name: str) -> Theme:
    """Get a theme instance by name.

    Args:
        name: Theme name.

    Returns:
        Theme instance.

    Raises:
        ValueError: If theme not found.
    """
    cls = _THEMES.get(name)
    if cls is None:
        available = ", ".join(_THEMES.keys())
        raise ValueError(f"Unknown theme '{name}'. Available: {available}")
    return cls()


def list_themes() -> list[dict[str, str]]:
    """List all available themes.

    Returns:
        List of theme info dicts.
    """
    return [
        {"name": name, "description": cls().description}
        for name, cls in _THEMES.items()
    ]


__all__ = ["get_theme", "list_themes", "Theme"]
