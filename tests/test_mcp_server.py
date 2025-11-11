"""Integration tests for the Numbeo MCP server."""

import pytest

from numbeo_mcp_new.server import mcp


class TestMCPServerIntegration:
    """Integration tests for the MCP server."""

    @pytest.mark.asyncio
    async def test_server_has_all_tools(self):
        """Test that server has all expected tools."""
        tools = await mcp.get_tools()

        expected_tools = [
            "get_city_cost_of_living",
            "get_city_cost_of_living_archive",
            "get_city_indices",
            "get_city_crime_statistics",
            "get_city_healthcare",
            "get_city_traffic",
            "get_city_pollution",
            "get_country_prices",
            "get_city_rankings",
            "get_country_city_rankings",
        ]

        for tool_name in expected_tools:
            assert tool_name in tools, f"Tool {tool_name} not found in MCP server"

    @pytest.mark.asyncio
    async def test_tool_count(self):
        """Test that server has exactly 10 tools."""
        tools = await mcp.get_tools()
        assert len(tools) == 10, f"Expected 10 tools, got {len(tools)}"

    @pytest.mark.asyncio
    async def test_mcp_server_name(self):
        """Test that server has correct name."""
        assert mcp.name == "Numbeo API", f"Expected 'Numbeo API', got {mcp.name}"

    @pytest.mark.asyncio
    async def test_server_has_vocabulary_resource(self):
        """Test that server has vocabulary resource."""
        resources = await mcp.get_resources()
        assert "vocabulary://numbeo-terms" in resources, "Vocabulary resource not found"

    @pytest.mark.asyncio
    async def test_vocabulary_resource_exists(self):
        """Test that vocabulary resource exists."""
        resources = await mcp.get_resources()
        assert "vocabulary://numbeo-terms" in resources, "Vocabulary resource not found"
        # Just verify it exists - the content is tested through actual resource calls

    @pytest.mark.asyncio
    async def test_strict_validation_enabled(self):
        """Test that strict validation is enabled."""
        assert mcp.strict_input_validation is True

    def test_server_imports(self):
        """Test that all necessary modules can be imported."""
        from numbeo_mcp_new import main, mcp
        from numbeo_sdk import NumbeoClient

        # Verify imports are successful
        assert main is not None
        assert mcp is not None
        assert NumbeoClient is not None
