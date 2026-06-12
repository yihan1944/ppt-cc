# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PPT-CC is an MCP server that generates native editable PowerPoint presentations for Claude Code. It produces McKinsey/BCG-style consulting decks from text, PDF, DOCX, Markdown, or URLs.

## Commands

```bash
# Install dependencies
uv sync

# Run MCP server (stdio transport)
uv run python -m server.main

# Register with Claude Code
claude mcp add --transport stdio ppt-cc -- uv --directory . run python -m server.main
```

## Architecture

Three-stage pipeline: **Parse → Plan → Render**

```
Input (text/PDF/DOCX/MD/URL)
        │
        ▼
   ┌─────────────┐
   │  Parser      │  Extract plain text
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │  Planner     │  LLM structures content → DeckPlan JSON
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │  Renderer    │  python-pptx generates .pptx
   └──────┬──────┘
          ▼
   output.pptx
```

### Key Components

- **`server/main.py`** — MCP server entry point (stdio transport)
- **`server/tools.py`** — MCP tool definitions (parse_input, get_planning_prompt, create_ppt, list_themes, get_slide_types)
- **`server/models/schema.py`** — Pydantic v2 data models (DeckPlan, SlideContent, BulletItem, ChartData)
- **`server/parsers/`** — Input parsers for PDF, DOCX, Markdown, URL
- **`server/planner/slide_planner.py`** — LLM prompt generation and deck plan validation
- **`server/renderer/engine.py`** — Render orchestrator (theme + layout → PPTX)
- **`server/renderer/components.py`** — Reusable slide components (title bar, bullets, page numbers)
- **`server/renderer/themes/`** — Theme registry and definitions
- **`server/renderer/layouts/`** — Slide type renderers (10 types)

### Data Flow

1. **Parser** extracts plain text from input (auto-detects format)
2. **Planner** generates LLM prompt with DeckPlan JSON schema
3. **LLM** returns structured JSON matching DeckPlan schema
4. **Renderer** validates JSON, loads theme, renders each slide via layout-specific renderer
5. **Output** saved to `./output/` directory (auto-generates timestamped filename)

### Key Design Patterns

- **MCP Tools**: All tools defined in `tools.py` using `@mcp.tool()` decorator
- **Data Models**: Pydantic v2 models in `schema.py` — DeckPlan is the contract between planner and renderer
- **Theme System**: Themes registered in `themes/__init__.py`, inherit from `base.Theme`
- **Layout System**: Each slide type has a dedicated renderer in `layouts/`, registered in `layouts/__init__.py`
- **Parser Chain**: Parsers registered in `parsers/__init__.py`, each implements `BaseParser.can_handle()` and `parse()`

## Slide Types

10 supported types: `title`, `agenda`, `section`, `content`, `two_column`, `chart`, `table`, `quote`, `key_takeaway`, `closing`

## Adding New Features

### New Slide Type
1. Create `server/renderer/layouts/<type>.py` with `render_<type>()` function
2. Add to `server/renderer/layouts/__init__.py` exports
3. Register in `server/renderer/engine.py` `_get_layout_map()`
4. Add type to `server/models/schema.py` `SlideType` enum

### New Theme
1. Create `server/renderer/themes/<name>.py` inheriting from `base.Theme`
2. Register in `server/renderer/themes/__init__.py` `_THEMES` dict

### New Parser
1. Create `server/parsers/<format>_parser.py` inheriting from `base.BaseParser`
2. Implement `can_handle()` and `parse()` methods
3. Register in `server/parsers/__init__.py` `_PARSERS` list

## Output Directory

Generated PPTX files are saved to `./output/` (git-ignored). The code auto-generates timestamped filenames like `presentation_20260612_142300.pptx`.
