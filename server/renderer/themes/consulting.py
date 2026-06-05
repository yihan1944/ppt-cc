"""Professional consulting theme — 结构清晰，配色克制."""

from __future__ import annotations

from pptx.util import Pt

from server.renderer.themes.base import (
    Theme,
    ThemeColors,
    ThemeFonts,
    ThemeLayout,
)


class ConsultingTheme(Theme):
    """Professional consulting theme.

    有结构感（顶部色条 + 分割线），配色克制（深墨蓝 + 墨绿），
    字体现代（Calibri），边距舒适（0.8"）。
    """

    name = "consulting"
    description = "商务简约 — 有结构感的专业风格，适合政务/AI产品经理"

    def __init__(self):
        super().__init__()
        self.colors = ThemeColors(
            primary="#1F2A44",       # 深墨蓝 — 顶部色条、标题
            secondary="#3F6B5C",     # 墨绿 — 强调色、高亮
            accent="#3F6B5C",        # 墨绿
            background="#FFFFFF",     # 白色背景
            text_dark="#2D2D2D",     # 近黑 — 正文
            text_light="#FFFFFF",    # 白色
            text_muted="#7F8C8B",    # 中灰 — 页码
            divider="#E8E8E4",       # 淡灰 — 分割线
            chart_colors=[
                "#1F2A44", "#3F6B5C", "#5B7DB1", "#8C6A4A",
                "#7F8C8B", "#1F2A44", "#3F6B5C", "#5B7DB1",
            ],
        )
        self.fonts = ThemeFonts(
            title="Calibri Light",
            body="Calibri",
            title_size=Pt(28),
            subtitle_size=Pt(18),
            body_size=Pt(16),
            bullet_size=Pt(15),
            note_size=Pt(10),
            caption_size=Pt(12),
        )
        self.layout = ThemeLayout(
            slide_width=13.333,
            slide_height=7.5,
            margin_left=0.8,
            margin_right=0.8,
            margin_top=0.75,
            margin_bottom=0.5,
            title_bar_height=0.06,   # 细色条 — 有结构但不抢眼
            title_bar_y=0.0,
            content_top=1.6,
            content_width=11.733,
            page_num_x=12.0,
            page_num_y=7.0,
        )
