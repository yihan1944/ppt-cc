"""Layout renderers for different slide types."""

from server.renderer.layouts.agenda import render_agenda
from server.renderer.layouts.chart import render_chart
from server.renderer.layouts.closing import render_closing
from server.renderer.layouts.content import render_content
from server.renderer.layouts.key_takeaway import render_key_takeaway
from server.renderer.layouts.quote import render_quote
from server.renderer.layouts.section import render_section
from server.renderer.layouts.table import render_table
from server.renderer.layouts.title import render_title
from server.renderer.layouts.two_column import render_two_column

__all__ = [
    "render_title",
    "render_agenda",
    "render_section",
    "render_content",
    "render_two_column",
    "render_chart",
    "render_table",
    "render_quote",
    "render_key_takeaway",
    "render_closing",
]
