"""PPT-CC MCP Server entry point."""

from __future__ import annotations

import logging
import sys

# IMPORTANT: For stdio servers, never print to stdout. Use stderr for logging.
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("ppt-cc")

from server.tools import mcp

logger.info("PPT-CC MCP Server starting...")

if __name__ == "__main__":
    mcp.run(transport="stdio")
