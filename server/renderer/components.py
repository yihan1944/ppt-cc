"""Reusable slide components — structured, clean, professional."""

from __future__ import annotations

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from server.renderer.themes.base import Theme


def add_title_bar(slide, theme: Theme) -> None:
    """Add the thin colored accent bar at the top of a slide."""
    layout = theme.layout
    if layout.title_bar_height <= 0:
        return
    r, g, b = theme.hex_to_rgb(theme.colors.primary)

    shape = slide.shapes.add_shape(
        1,  # RECTANGLE
        Inches(0),
        Inches(layout.title_bar_y),
        Inches(layout.slide_width),
        Inches(layout.title_bar_height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(r, g, b)
    shape.line.fill.background()


def add_page_number(slide, theme: Theme, page_num: int, total: int) -> None:
    """Add subtle page number at bottom-right."""
    layout = theme.layout
    r, g, b = theme.hex_to_rgb(theme.colors.text_muted)

    txBox = slide.shapes.add_textbox(
        Inches(layout.page_num_x),
        Inches(layout.page_num_y),
        Inches(1.0),
        Inches(0.4),
    )
    tf = txBox.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f"{page_num}"
    run.font.size = Pt(9)
    run.font.name = "Calibri"
    run.font.color.rgb = RGBColor(r, g, b)


def add_title_text(
    slide,
    theme: Theme,
    title: str,
    y: float | None = None,
    font_size: int | None = None,
    max_width: float | None = None,
) -> float:
    """Add a slide title — Calibri Light, left-aligned.

    Returns the bottom Y position of the title box.
    """
    layout = theme.layout
    r, g, b = theme.hex_to_rgb(theme.colors.primary)

    y_pos = y if y is not None else layout.margin_top
    size = Pt(font_size) if font_size else theme.fonts.title_size
    width = max_width if max_width is not None else layout.content_width

    # Dynamic height based on title length
    char_per_line = max(1, int(width * 5.5))
    num_lines = max(1, (len(title) + char_per_line - 1) // char_per_line)
    title_height = max(0.7, num_lines * 0.5)

    txBox = slide.shapes.add_textbox(
        Inches(layout.margin_left),
        Inches(y_pos),
        Inches(width),
        Inches(title_height),
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = title
    run.font.size = size
    run.font.bold = True
    run.font.name = theme.fonts.title
    run.font.color.rgb = RGBColor(r, g, b)

    return y_pos + title_height


def add_bullets(
    slide,
    theme: Theme,
    bullets: list,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
) -> None:
    """Add bullet points — clean with em-dash markers."""
    from server.models.schema import BulletItem

    layout = theme.layout
    r, g, b = theme.hex_to_rgb(theme.colors.text_dark)

    x_pos = x if x is not None else layout.margin_left
    y_pos = y if y is not None else layout.content_top
    w = width if width is not None else layout.content_width
    h = height if height is not None else 5.0

    txBox = slide.shapes.add_textbox(
        Inches(x_pos), Inches(y_pos), Inches(w), Inches(h)
    )
    tf = txBox.text_frame
    tf.word_wrap = True

    def _add_items(items: list[BulletItem], text_frame, first: bool = False):
        for i, item in enumerate(items):
            if first and i == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()

            p.level = item.level
            p.space_after = Pt(6)
            p.space_before = Pt(2)

            marker = "—  " if item.level == 0 else "–  "
            indent = "    " * item.level

            run = p.add_run()
            run.text = f"{indent}{marker}{item.text}"
            run.font.size = Pt(15)
            run.font.name = "Calibri"
            run.font.color.rgb = RGBColor(r, g, b)

            if item.sub_bullets:
                _add_items(item.sub_bullets, text_frame)

    _add_items(bullets, tf, first=True)


def set_slide_background(slide, theme: Theme, color: str | None = None) -> None:
    """Set slide background color."""
    bg_color = color or theme.colors.background
    r, g, b = theme.hex_to_rgb(bg_color)

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(r, g, b)


def add_thin_line(slide, theme: Theme, y: float, width: float | None = None) -> None:
    """Add a thin horizontal line."""
    layout = theme.layout
    r, g, b = theme.hex_to_rgb(theme.colors.divider)
    w = width if width is not None else layout.content_width

    shape = slide.shapes.add_shape(
        1,
        Inches(layout.margin_left),
        Inches(y),
        Inches(w),
        Inches(0.01),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(r, g, b)
    shape.line.fill.background()
