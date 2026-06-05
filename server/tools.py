"""MCP Tool definitions for PPT-CC."""

from __future__ import annotations

import json
import logging
import sys

from mcp.server.fastmcp import FastMCP

from server.models.schema import DeckPlan, SlideType
from server.parsers import parse_input
from server.planner.slide_planner import get_planning_prompt, parse_deck_plan_json, validate_deck_plan
from server.renderer.engine import render_deck
from server.renderer.themes import list_themes as _list_themes

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "ppt-cc",
    instructions=(
        "PPT-CC: AI-powered PowerPoint generation. "
        "Use `create_ppt` to generate a presentation from a structured deck plan JSON. "
        "Use `parse_input` first to extract text from PDF/DOCX/URL/Markdown files. "
        "Use `get_planning_prompt` to get the LLM prompt for planning a deck. "
        "Use `list_themes` to see available visual themes. "
        "Use `get_slide_types` to see supported slide types."
    ),
)


@mcp.tool()
async def parse_input_tool(source: str, source_type: str = "auto") -> str:
    """Extract text content from various input formats.

    Supports: plain text, Markdown, PDF, DOCX, and URLs.
    Use this first to extract content before planning the deck.

    Args:
        source: Text content, file path, or URL to parse.
        source_type: Input type - 'auto' (detect), 'text', 'markdown', 'pdf', 'docx', 'url'.
    """
    try:
        result = parse_input(source, source_type)
        return result
    except Exception as e:
        return f"Error parsing input: {e}"


@mcp.tool()
async def get_planning_prompt_tool(content: str, max_slides: int = 15, theme: str = "consulting") -> str:
    """Get the LLM prompt for planning a presentation deck structure.

    Returns a prompt that should be sent to an LLM to generate a structured
    deck plan JSON. The LLM's JSON response should then be passed to create_ppt.

    Args:
        content: The text content to plan a presentation around.
        max_slides: Maximum number of slides (default 15).
        theme: Theme name (default 'consulting').
    """
    return get_planning_prompt(content, max_slides, theme)


@mcp.tool()
async def create_ppt(deck_plan_json: str, output_path: str = "") -> str:
    """Generate a PowerPoint presentation from a structured deck plan.

    Takes a JSON string matching the DeckPlan schema and renders it into
    a professional .pptx file. Use get_planning_prompt first to get the
    prompt for generating the deck plan JSON.

    Args:
        deck_plan_json: JSON string of the deck plan (DeckPlan schema).
        output_path: Output file path. If empty, auto-generates in ~/ppt-cc-output/.
    """
    try:
        deck = parse_deck_plan_json(deck_plan_json)
        result_path = render_deck(deck, output_path)
        return f"Presentation saved to: {result_path}"
    except ValueError as e:
        return f"Invalid deck plan: {e}"
    except Exception as e:
        logger.error(f"Error creating PPT: {e}", exc_info=True)
        return f"Error creating presentation: {e}"


@mcp.tool()
async def list_themes_tool() -> str:
    """List all available visual themes for presentations."""
    themes = _list_themes()
    lines = ["Available themes:\n"]
    for t in themes:
        lines.append(f"  - **{t['name']}**: {t['description']}")
    return "\n".join(lines)


@mcp.tool()
async def get_slide_types_tool() -> str:
    """List all supported slide types and their use cases."""
    types_info = [
        ("title", "封面页 — 演示文稿标题和副标题"),
        ("agenda", "议程/目录页 — 列出各章节标题"),
        ("section", "章节分隔页 — 标记新章节开始"),
        ("content", "内容页 — 带要点列表的标准内容页"),
        ("two_column", "双栏对比页 — 左右对比或并列展示"),
        ("chart", "图表页 — 柱状图、折线图、饼图等数据可视化"),
        ("table", "表格页 — 结构化数据表格展示"),
        ("quote", "引用页 — 突出展示关键引言或洞察"),
        ("key_takeaway", "关键要点页 — 强调最重要的一个结论"),
        ("closing", "结尾页 — 致谢、联系方式、行动号召"),
    ]
    lines = ["Supported slide types:\n"]
    for type_name, desc in types_info:
        lines.append(f"  - **{type_name}**: {desc}")
    return "\n".join(lines)
