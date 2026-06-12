# PPT-CC

> AI-powered PPT generation skill for Claude Code — generate professional PowerPoint presentations from text, PDF, DOCX, Markdown, or URLs.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/MCP-compatible-purple.svg" alt="MCP">
</p>

## What is this?

PPT-CC is a Claude Code Skill that generates **native editable .pptx files** using a McKinsey/BCG-style consulting theme. It's an MCP server that Claude Code can call to create presentations from any input.

## Demo

```
/ppt 帮我做一个关于AI趋势的演示文稿
```

```
/ppt 把这份报告做成PPT: ./report.pdf
```

## Features

- **Multi-format input** — Plain text, Markdown, PDF, DOCX, URL
- **Native editable PPTX** — Real PowerPoint objects, not images or SVGs
- **Consulting theme** — Deep ink blue + sage green, Calibri typography
- **10 slide types** — Title, agenda, section, content, two-column, chart, table, quote, key takeaway, closing
- **MCP Server** — Integrates directly with Claude Code via `/ppt` command
- **Structured pipeline** — Parse → Plan → Render, each layer decoupled

## Quick Start

### 1. Install

```bash
git clone https://github.com/your-username/ppt-cc.git
cd ppt-cc
uv sync
```

### 2. Register MCP Server

```bash
claude mcp add --transport stdio ppt-cc -- uv --directory . run python -m server.main
```

### 3. Use

In Claude Code, type `/ppt` followed by your request.

## Architecture

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

## Slide Types

| Type | Description |
|------|-------------|
| `title` | Cover slide with name and subtitle |
| `agenda` | Table of contents with numbered items |
| `section` | Section divider |
| `content` | Standard bullet point slide |
| `two_column` | Side-by-side comparison |
| `chart` | Data visualization (bar, column, line, pie) |
| `table` | Structured data table |
| `quote` | Highlighted quote or insight |
| `key_takeaway` | Single most important point |
| `closing` | Thank you / contact slide |

## MCP Tools

| Tool | Description |
|------|-------------|
| `parse_input_tool` | Extract text from PDF/DOCX/URL/Markdown |
| `get_planning_prompt_tool` | Get LLM prompt for deck planning |
| `create_ppt` | Generate PPTX from structured DeckPlan JSON |
| `list_themes_tool` | List available themes |
| `get_slide_types_tool` | List supported slide types |

## Project Structure

```
ppt-cc/
├── .claude/skills/ppt/SKILL.md   # Skill definition
├── .mcp.json                      # MCP server config
├── server/
│   ├── main.py                    # MCP server entry
│   ├── tools.py                   # Tool definitions
│   ├── models/schema.py           # Pydantic data models
│   ├── parsers/                   # Input parsers (PDF, DOCX, MD, URL)
│   ├── planner/                   # LLM planning logic
│   └── renderer/                  # PPTX rendering engine
│       ├── engine.py              # Render orchestrator
│       ├── components.py          # Reusable slide components
│       ├── themes/                # Visual themes
│       └── layouts/               # Slide type renderers
├── templates/                     # Sample templates
├── output/                        # Generated PPTX output (git-ignored)
└── pyproject.toml
```

## Tech Stack

- **Python 3.11+**
- **python-pptx** — PPTX generation
- **FastMCP** — MCP server framework
- **Pydantic v2** — Data validation
- **PyMuPDF** — PDF parsing
- **python-docx** — DOCX parsing
- **httpx + BeautifulSoup4** — URL parsing

## Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

## License

MIT
