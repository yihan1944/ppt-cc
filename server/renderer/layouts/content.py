"""Content slide — structured with title bar, natural spacing."""

from __future__ import annotations

from server.models.schema import SlideContent
from server.renderer.components import (
    add_title_bar,
    add_page_number,
    add_title_text,
    add_bullets,
)
from server.renderer.themes.base import Theme


def render_content(slide, content: SlideContent, theme: Theme, page_num: int, total: int) -> None:
    """Render a content slide with bullet points."""
    add_title_bar(slide, theme)
    title_bottom = add_title_text(slide, theme, content.title)
    add_page_number(slide, theme, page_num, total)

    if content.bullets:
        add_bullets(slide, theme, content.bullets, y=title_bottom + 0.25)
