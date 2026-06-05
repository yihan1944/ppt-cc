"""Chart slide."""

from __future__ import annotations

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

from server.models.schema import SlideContent
from server.renderer.components import (
    add_title_bar,
    add_page_number,
    add_title_text,
)
from server.renderer.themes.base import Theme

_CHART_TYPE_MAP = {
    "bar": XL_CHART_TYPE.BAR_CLUSTERED,
    "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
    "line": XL_CHART_TYPE.LINE,
    "pie": XL_CHART_TYPE.PIE,
}


def render_chart(slide, content: SlideContent, theme: Theme, page_num: int, total: int) -> None:
    """Render a chart slide."""
    add_title_bar(slide, theme)
    title_bottom = add_title_text(slide, theme, content.title)
    add_page_number(slide, theme, page_num, total)

    if not content.chart:
        return

    layout = theme.layout
    chart_data = CategoryChartData()
    chart_data.categories = content.chart.categories

    for series in content.chart.series:
        chart_data.add_series(series.name, series.values)

    chart_type = _CHART_TYPE_MAP.get(content.chart.chart_type, XL_CHART_TYPE.COLUMN_CLUSTERED)

    chart_x = Inches(layout.margin_left)
    chart_y = Inches(title_bottom + 0.2)
    chart_cx = Inches(layout.content_width)
    chart_cy = Inches(4.8)

    chart_frame = slide.shapes.add_chart(
        chart_type, chart_x, chart_y, chart_cx, chart_cy, chart_data
    )

    chart = chart_frame.chart
    chart.has_legend = len(content.chart.series) > 1

    colors = theme.colors.chart_colors
    for i, series in enumerate(chart.series):
        color_hex = colors[i % len(colors)]
        r, g, b = theme.hex_to_rgb(color_hex)
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = RGBColor(r, g, b)
