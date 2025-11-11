"""Numbeo MCP Server - FastMCP server for the Numbeo API.

This server provides MCP tools for accessing Numbeo API data with
strict validation and proper authentication handling.
"""

__version__ = "0.1.0"

from .server import main, mcp

__all__ = ["main", "mcp"]
