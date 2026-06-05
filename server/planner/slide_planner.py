"""Slide planning logic — validates LLM-structured deck plans."""

from __future__ import annotations

import json
import logging

from server.models.schema import DeckPlan

logger = logging.getLogger(__name__)

PLANNING_PROMPT_TEMPLATE = """You are a world-class presentation designer specializing in McKinsey/BCG-style consulting decks.

Given the following content, create a structured presentation plan.

## Content
{content}

## Requirements
- Maximum {max_slides} slides
- Theme: {theme}
- Style: Professional consulting deck (McKinsey/BCG)
- Structure: Clear narrative flow with agenda → content → key takeaways
- Each slide should have a clear title and concise bullet points (max 4 bullets, max 12 words each)
- Use appropriate slide types: content, two_column, chart, table, quote, key_takeaway

## Slide Type Guide
- **title**: Cover slide with presentation title and subtitle
- **agenda**: Table of contents with section names
- **section**: Section divider with section title
- **content**: Main content with bullet points (use for most slides)
- **two_column**: Compare/contrast with left and right columns
- **chart**: Data visualization (bar, pie, line, column charts)
- **table**: Tabular data presentation
- **quote**: Highlight a key quote or insight
- **key_takeaway**: Emphasize the single most important point
- **closing**: Final slide with contact info or call to action

## Output Format
Return a JSON object matching this exact schema:
{schema}

Return ONLY the JSON, no other text."""


def get_planning_prompt(content: str, max_slides: int = 15, theme: str = "consulting") -> str:
    """Generate the prompt for LLM deck planning.

    Args:
        content: The parsed input text.
        max_slides: Maximum number of slides.
        theme: Theme name.

    Returns:
        Formatted prompt string for the LLM.
    """
    schema_json = json.dumps(DeckPlan.model_json_schema(), indent=2, ensure_ascii=False)
    return PLANNING_PROMPT_TEMPLATE.format(
        content=content,
        max_slides=max_slides,
        theme=theme,
        schema=schema_json,
    )


def validate_deck_plan(data: dict) -> DeckPlan:
    """Validate and parse a deck plan from JSON data.

    Args:
        data: Dictionary representation of a deck plan.

    Returns:
        Validated DeckPlan instance.

    Raises:
        ValueError: If the data doesn't match the expected schema.
    """
    try:
        return DeckPlan.model_validate(data)
    except Exception as e:
        logger.error(f"Deck plan validation failed: {e}")
        raise ValueError(f"Invalid deck plan: {e}") from e


def parse_deck_plan_json(json_str: str) -> DeckPlan:
    """Parse a JSON string into a validated DeckPlan.

    Handles common LLM output quirks like markdown code fences.

    Args:
        json_str: JSON string from LLM output.

    Returns:
        Validated DeckPlan instance.
    """
    text = json_str.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        # Remove first line (```json or ```)
        first_newline = text.index("\n")
        text = text[first_newline + 1 :]
        # Remove trailing ```
        if text.rstrip().endswith("```"):
            text = text.rstrip()[: -len("```")]

    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e

    return validate_deck_plan(data)
