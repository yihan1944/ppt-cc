"""Base theme definition."""

from __future__ import annotations

from dataclasses import dataclass, field

from pptx.util import Inches, Pt


@dataclass
class ThemeColors:
    """Color scheme for a theme."""

    primary: str = "#1F2A44"  # 深墨蓝 — 标题、主色
    secondary: str = "#5B7DB1"  # 雾霾蓝 — 强调、装饰
    accent: str = "#5B7DB1"  # 雾霾蓝 — 高亮、重点
    background: str = "#FAFAF8"  # 暖白 — 背景
    text_dark: str = "#2E2E2E"  # 深灰 — 正文（不用纯黑）
    text_light: str = "#FFFFFF"  # 白色 — 深色背景上的文字
    text_muted: str = "#6B7280"  # 次级灰 — 注释、页码
    divider: str = "#E8EAF0"  # 辅助线 — 分隔线
    chart_colors: list[str] = field(
        default_factory=lambda: [
            "#1F2A44", "#5B7DB1", "#3F6B5C", "#8C6A4A",
            "#6B7280", "#1F2A44", "#5B7DB1", "#3F6B5C",
        ]
    )


@dataclass
class ThemeFonts:
    """Font settings for a theme."""

    title: str = "Arial"
    body: str = "Arial"
    title_size: Pt = field(default_factory=lambda: Pt(28))
    subtitle_size: Pt = field(default_factory=lambda: Pt(18))
    body_size: Pt = field(default_factory=lambda: Pt(16))
    bullet_size: Pt = field(default_factory=lambda: Pt(14))
    note_size: Pt = field(default_factory=lambda: Pt(10))
    caption_size: Pt = field(default_factory=lambda: Pt(12))


@dataclass
class ThemeLayout:
    """Layout measurements for a theme (in inches)."""

    slide_width: float = 13.333  # 16:9 widescreen
    slide_height: float = 7.5

    # Margins
    margin_left: float = 0.8
    margin_right: float = 0.8
    margin_top: float = 1.2
    margin_bottom: float = 0.6

    # Title bar
    title_bar_height: float = 0.08
    title_bar_y: float = 0.0

    # Content area
    content_top: float = 1.5
    content_width: float = 11.733

    # Page number
    page_num_x: float = 12.0
    page_num_y: float = 7.0


class Theme:
    """Base theme class."""

    name: str = "base"
    description: str = "Base theme"

    def __init__(self):
        self.colors = ThemeColors()
        self.fonts = ThemeFonts()
        self.layout = ThemeLayout()

    def hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
