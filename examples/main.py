"""Example of using the Numbeo MCP server.

This example shows how to import and use the Numbeo API client directly.
The MCP server exposes these same functions as MCP tools.
"""

import os

from numbeo_mcp.client import NumberoAPIClient


def main():
    """Example usage of the Numbeo API client."""
    # Ensure API key is set
    api_key = os.getenv("NUMBEO_API_KEY")
    if not api_key:
        print("Error: NUMBEO_API_KEY environment variable not set")
        print("Please set it with: export NUMBEO_API_KEY='your-api-key'")
        return

    # Initialize the client
    client = NumberoAPIClient(api_key=api_key)

    print("Numbeo API Examples")
    print("=" * 50)

    # Example 1: Get cost of living for a city
    print("\n1. Cost of Living for New York:")
    try:
        data = client.get_city_prices("New York", "United States")
        print(f"   API Response: {list(data.keys())}")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 2: Get city indices
    print("\n2. City Indices for London:")
    try:
        data = client.get_indices("London", "United Kingdom")
        print(f"   API Response: {list(data.keys())}")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 3: Get crime statistics
    print("\n3. Crime Statistics for Tokyo:")
    try:
        data = client.get_city_crime("Tokyo", "Japan")
        print(f"   API Response: {list(data.keys())}")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 4: Get rankings
    print("\n4. Global Cost of Living Rankings:")
    try:
        data = client.get_rankings("cost-of-living")
        print(f"   API Response: {list(data.keys())}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n" + "=" * 50)
    print("To use these functions via MCP, run: numbeo-mcp")
    print("Then connect your MCP client to access the tools.")


if __name__ == "__main__":
    main()
