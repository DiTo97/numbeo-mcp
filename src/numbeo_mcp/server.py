"""FastMCP server for the Numbeo API."""

import os
from typing import Optional

from fastmcp import FastMCP

from .client import NumberoAPIClient

# Initialize FastMCP server
mcp = FastMCP("Numbeo API")


def get_client() -> NumberoAPIClient:
    """Get or create the Numbeo API client."""
    api_key = os.getenv("NUMBEO_API_KEY")
    return NumberoAPIClient(api_key=api_key)


@mcp.tool()
def get_city_cost_of_living(city: str, country: Optional[str] = None) -> dict:
    """Get cost of living prices for a specific city.

    This tool retrieves current prices for various goods and services in a city,
    including food, restaurants, transportation, utilities, and more.

    Args:
        city: Name of the city (e.g., "New York", "London", "Tokyo")
        country: Optional country name for disambiguation (e.g., "United States", "United Kingdom")

    Returns:
        Dictionary containing price data for various items and services in the city
    """
    client = get_client()
    return client.get_city_prices(city, country)


@mcp.tool()
def get_city_cost_of_living_archive(
    city: str, country: Optional[str] = None, currency: Optional[str] = None
) -> dict:
    """Get historical cost of living data for a city.

    Retrieve archived price information to analyze trends over time.

    Args:
        city: Name of the city
        country: Optional country name for disambiguation
        currency: Optional currency code (e.g., "USD", "EUR", "GBP")

    Returns:
        Dictionary with historical price data
    """
    client = get_client()
    return client.get_city_prices_archive(city, country, currency)


@mcp.tool()
def get_city_indices(city: str, country: Optional[str] = None) -> dict:
    """Get various quality of life indices for a city.

    Provides composite indices including cost of living index, rent index,
    groceries index, restaurant price index, and purchasing power index.

    Args:
        city: Name of the city
        country: Optional country name for disambiguation

    Returns:
        Dictionary with various city indices
    """
    client = get_client()
    return client.get_indices(city, country)


@mcp.tool()
def get_city_crime_statistics(city: str, country: Optional[str] = None) -> dict:
    """Get crime statistics and safety indices for a city.

    Provides information about crime levels and safety perceptions in the city.

    Args:
        city: Name of the city
        country: Optional country name for disambiguation

    Returns:
        Dictionary with crime statistics and safety indices
    """
    client = get_client()
    return client.get_city_crime(city, country)


@mcp.tool()
def get_city_healthcare(city: str, country: Optional[str] = None) -> dict:
    """Get healthcare quality indices for a city.

    Provides information about healthcare system quality, accessibility,
    and other health-related metrics.

    Args:
        city: Name of the city
        country: Optional country name for disambiguation

    Returns:
        Dictionary with healthcare quality indices
    """
    client = get_client()
    return client.get_city_healthcare(city, country)


@mcp.tool()
def get_city_traffic(city: str, country: Optional[str] = None) -> dict:
    """Get traffic and commute information for a city.

    Provides data about traffic conditions, commute times, and transportation efficiency.

    Args:
        city: Name of the city
        country: Optional country name for disambiguation

    Returns:
        Dictionary with traffic and commute data
    """
    client = get_client()
    return client.get_city_traffic(city, country)


@mcp.tool()
def get_city_pollution(city: str, country: Optional[str] = None) -> dict:
    """Get pollution and environmental quality data for a city.

    Provides information about air quality, pollution levels, and environmental indices.

    Args:
        city: Name of the city
        country: Optional country name for disambiguation

    Returns:
        Dictionary with pollution and environmental data
    """
    client = get_client()
    return client.get_city_pollution(city, country)


@mcp.tool()
def get_country_prices(country: str) -> dict:
    """Get average cost of living prices for an entire country.

    Provides country-level aggregated price data.

    Args:
        country: Name of the country (e.g., "United States", "Germany", "Japan")

    Returns:
        Dictionary with country-level price data
    """
    client = get_client()
    return client.get_country_prices(country)


@mcp.tool()
def get_city_rankings(section: str = "cost-of-living") -> dict:
    """Get global city rankings for various categories.

    Provides rankings of cities worldwide based on different metrics.

    Args:
        section: Category for rankings. Options include:
                - "cost-of-living": Overall cost of living rankings
                - "crime": Crime and safety rankings
                - "health-care": Healthcare quality rankings
                - "pollution": Environmental quality rankings
                - "traffic": Traffic and commute rankings
                - "quality-of-life": Overall quality of life rankings

    Returns:
        Dictionary with city rankings for the specified category
    """
    client = get_client()
    return client.get_rankings(section)


@mcp.tool()
def get_country_city_rankings(country: str, section: str = "cost-of-living") -> dict:
    """Get city rankings within a specific country.

    Provides rankings of cities within a country based on different metrics.

    Args:
        country: Name of the country
        section: Category for rankings (same options as get_city_rankings)

    Returns:
        Dictionary with city rankings within the specified country
    """
    client = get_client()
    return client.get_rankings_by_country(country, section)


def main():
    """Run the Numbeo MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
