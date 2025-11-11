"""FastMCP server for the Numbeo API with authentication and resources."""

from typing import Any

from fastmcp import Context, FastMCP
from numbeo_sdk import NumbeoClient

from .schemas import (
    CityArchiveQueryParams,
    CityQueryParams,
    CountryQueryParams,
    CountryRankingsQueryParams,
    RankingsQueryParams,
)

# Initialize FastMCP server with strict validation
mcp = FastMCP("Numbeo API", strict_input_validation=True)


# Vocabulary resource
VOCABULARY_CONTENT = """This is the explanation of the terms used:
contributors12months: The number of contributors who have submitted data in the past 12 months
monthLastUpdate: The month when the data was last updated
yearLastUpdate: The year of the last update
contributors: The total number of contributors whose data was used in the calculations (as we use an adaptive archive policy)
cpi_factor: A factor used to calculate our Consumer Price Index. Multiply this factor by the prices and add the result to the overall sum to compute the Cost of Living Index.
rent_factor: A factor used to calculate our Rent Index. Multiply this factor by the prices and add the result to the overall sum to compute the Rent Index."""


@mcp.resource("vocabulary://numbeo-terms")
def get_vocabulary() -> str:
    """Get the vocabulary of Numbeo API terms.

    Returns:
        Explanation of terms used in Numbeo API responses
    """
    return VOCABULARY_CONTENT


def get_client(ctx: Context) -> NumbeoClient:
    """Get Numbeo client with API key from context.

    The API key should be provided by the client through the authorization context.
    It will be propagated to the Numbeo SDK which uses it for API calls.

    Args:
        ctx: FastMCP context containing authorization metadata

    Returns:
        Initialized NumbeoClient

    Raises:
        ValueError: If API key is not provided in the context
    """
    # Get API key from context metadata
    # The client should provide it via Bearer token or custom header
    api_key = ctx.request_context.meta.get("api_key")

    if not api_key:
        # Try to get from authorization header
        auth_header = ctx.request_context.meta.get("authorization", "")
        if auth_header.startswith("Bearer "):
            api_key = auth_header[7:]  # Remove "Bearer " prefix

    if not api_key:
        raise ValueError(
            "Numbeo API key is required. Please provide it via 'api_key' in meta or 'Authorization: Bearer <key>' header."
        )

    return NumbeoClient(api_key=api_key)


@mcp.tool()
def get_city_cost_of_living(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get cost of living prices for a specific city.

    This tool retrieves current prices for various goods and services in a city,
    including food, restaurants, transportation, utilities, and more.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary containing price data for various items and services in the city
    """
    client = get_client(ctx)
    return client.get_city_prices(params.city, params.country)


@mcp.tool()
def get_city_cost_of_living_archive(
    params: CityArchiveQueryParams, ctx: Context
) -> dict[str, Any]:
    """Get historical cost of living data for a city.

    Retrieve archived price information to analyze trends over time.

    Args:
        params: Query parameters with city, optional country, and currency
        ctx: Request context containing API key

    Returns:
        Dictionary with historical price data
    """
    client = get_client(ctx)
    return client.get_city_prices_archive(params.city, params.country, params.currency)


@mcp.tool()
def get_city_indices(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get various quality of life indices for a city.

    Provides composite indices including cost of living index, rent index,
    groceries index, restaurant price index, and purchasing power index.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with various city indices
    """
    client = get_client(ctx)
    return client.get_indices(params.city, params.country)


@mcp.tool()
def get_city_crime_statistics(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get crime statistics and safety indices for a city.

    Provides information about crime levels and safety perceptions in the city.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with crime statistics and safety indices
    """
    client = get_client(ctx)
    return client.get_city_crime(params.city, params.country)


@mcp.tool()
def get_city_healthcare(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get healthcare quality indices for a city.

    Provides information about healthcare system quality, accessibility,
    and other health-related metrics.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with healthcare quality indices
    """
    client = get_client(ctx)
    return client.get_city_healthcare(params.city, params.country)


@mcp.tool()
def get_city_traffic(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get traffic and commute information for a city.

    Provides data about traffic conditions, commute times, and transportation efficiency.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with traffic and commute data
    """
    client = get_client(ctx)
    return client.get_city_traffic(params.city, params.country)


@mcp.tool()
def get_city_pollution(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get pollution and environmental quality data for a city.

    Provides information about air quality, pollution levels, and environmental indices.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with pollution and environmental data
    """
    client = get_client(ctx)
    return client.get_city_pollution(params.city, params.country)


@mcp.tool()
def get_country_prices(params: CountryQueryParams, ctx: Context) -> dict[str, Any]:
    """Get average cost of living prices for an entire country.

    Provides country-level aggregated price data.

    Args:
        params: Query parameters with country name
        ctx: Request context containing API key

    Returns:
        Dictionary with country-level price data
    """
    client = get_client(ctx)
    return client.get_country_prices(params.country)


@mcp.tool()
def get_city_rankings(params: RankingsQueryParams, ctx: Context) -> dict[str, Any]:
    """Get global city rankings for various categories.

    Provides rankings of cities worldwide based on different metrics.

    Args:
        params: Query parameters with ranking section
        ctx: Request context containing API key

    Returns:
        Dictionary with city rankings for the specified category
    """
    client = get_client(ctx)
    return client.get_rankings(params.section)


@mcp.tool()
def get_country_city_rankings(
    params: CountryRankingsQueryParams, ctx: Context
) -> dict[str, Any]:
    """Get city rankings within a specific country.

    Provides rankings of cities within a country based on different metrics.

    Args:
        params: Query parameters with country and ranking section
        ctx: Request context containing API key

    Returns:
        Dictionary with city rankings within the specified country
    """
    client = get_client(ctx)
    return client.get_rankings_by_country(params.country, params.section)


def main():
    """Run the Numbeo MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
