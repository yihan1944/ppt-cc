"""Data models for PPT-CC slide deck structure."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SlideType(str, Enum):
    """Supported slide types for consulting-style presentations."""

    TITLE = "title"  # 封面页
    AGENDA = "agenda"  # 议程/目录页
    SECTION = "section"  # 章节分隔页
    CONTENT = "content"  # 内容页（要点列表）
    TWO_COLUMN = "two_column"  # 双栏对比页
    CHART = "chart"  # 图表页
    TABLE = "table"  # 表格页
    QUOTE = "quote"  # 引用/金句页
    KEY_TAKEAWAY = "key_takeaway"  # 关键要点页
    CLOSING = "closing"  # 结尾页


class BulletItem(BaseModel):
    """A single bullet point with optional sub-bullets."""

    text: str = Field(description="Bullet point text")
    level: int = Field(default=0, description="Indentation level (0=top, 1=sub, 2=sub-sub)")
    sub_bullets: list[BulletItem] = Field(default_factory=list, description="Nested sub-bullets")


class ChartData(BaseModel):
    """Data for chart slides."""

    chart_type: str = Field(description="Chart type: bar, pie, line, column")
    title: str = Field(default="", description="Chart title")
    categories: list[str] = Field(description="Category labels")
    series: list[ChartSeries] = Field(description="Data series")


class ChartSeries(BaseModel):
    """A single data series in a chart."""

    name: str = Field(description="Series name")
    values: list[float] = Field(description="Data values")


class TableCell(BaseModel):
    """A cell in a table."""

    text: str = Field(description="Cell text")
    is_header: bool = Field(default=False, description="Whether this is a header cell")


class SlideContent(BaseModel):
    """Content for a single slide."""

    slide_type: SlideType = Field(description="Type of this slide")
    title: str = Field(default="", description="Slide title")
    subtitle: str = Field(default="", description="Slide subtitle (for title/section slides)")
    bullets: list[BulletItem] = Field(default_factory=list, description="Bullet points")
    left_bullets: list[BulletItem] = Field(default_factory=list, description="Left column bullets (two_column)")
    right_bullets: list[BulletItem] = Field(default_factory=list, description="Right column bullets (two_column)")
    left_title: str = Field(default="", description="Left column title (two_column)")
    right_title: str = Field(default="", description="Right column title (two_column)")
    body_text: str = Field(default="", description="Free-form body text")
    quote_text: str = Field(default="", description="Quote text (for quote slides)")
    quote_author: str = Field(default="", description="Quote attribution")
    key_point: str = Field(default="", description="Key takeaway text")
    agenda_items: list[str] = Field(default_factory=list, description="Agenda item titles")
    chart: Optional[ChartData] = Field(default=None, description="Chart data")
    table_rows: list[list[str]] = Field(default_factory=list, description="Table data as rows of strings")
    table_headers: list[str] = Field(default_factory=list, description="Table column headers")
    speaker_notes: str = Field(default="", description="Speaker notes for this slide")


class DeckPlan(BaseModel):
    """Complete deck plan — the contract between planner and renderer."""

    title: str = Field(description="Presentation title")
    subtitle: str = Field(default="", description="Presentation subtitle")
    author: str = Field(default="", description="Author name")
    theme: str = Field(default="consulting", description="Theme name")
    slides: list[SlideContent] = Field(description="Ordered list of slides")


# Rebuild forward references
ChartData.model_rebuild()
