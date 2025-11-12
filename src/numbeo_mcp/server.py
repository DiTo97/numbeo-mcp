"""FastMCP server for the Numbeo API with authentication and resources."""

from __future__ import annotations

from typing import Any

from fastmcp import Context, FastMCP
from numbeo_sdk import Numbeo, modeling

from .schemas import (
    CityArchiveQueryParams,
    CityQueryParams,
    CountryQueryParams,
    CountryRankingsQueryParams,
    RankingsQueryParams,
)

# Initialize FastMCP server with strict validation
mcp = FastMCP("Numbeo API", strict_input_validation=True)


SECTION_CODES = {
    "cost-of-living": 1,
    "crime": 2,
    "health-care": 3,
    "pollution": 4,
    "traffic": 5,
    "quality-of-life": 6,
}


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


def _resolve_api_key(ctx: Context) -> str:
    """Extract the Numbeo API key from the request context."""

    api_key = ctx.request_context.meta.get("api_key")
    if not api_key:
        auth_header = ctx.request_context.meta.get("authorization", "")
        if auth_header.startswith("Bearer "):
            api_key = auth_header[7:]

    if not api_key:
        raise ValueError(
            "Numbeo API key is required. Please provide it via 'api_key' in meta or 'Authorization: Bearer <key>' header."
        )

    return api_key


def _section_code(section: str) -> int:
    try:
        return SECTION_CODES[section]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Unsupported rankings section: {section}") from exc


def get_client(ctx: Context) -> Numbeo:
    """Instantiate a Numbeo SDK client using context metadata."""

    key = _resolve_api_key(ctx)
    return Numbeo(key=key)


@mcp.tool()
async def get_city_cost_of_living(
    params: CityQueryParams, ctx: Context
) -> dict[str, Any]:
    """Get cost of living prices for a specific city.

    This tool retrieves current prices for various goods and services in a city,
    including food, restaurants, transportation, utilities, and more.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary containing price data for various items and services in the city
    """
    request = modeling.GetCityPricesRequest(city=params.city, country=params.country)
    async with get_client(ctx) as client:
        response = await client.get_city_prices(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_cost_of_living_archive(
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
    request = modeling.GetHistoricalCityPricesRequest(
        city=params.city,
        country=params.country,
        currency=params.currency,
    )
    async with get_client(ctx) as client:
        response = await client.get_historical_city_prices(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_indices(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get various quality of life indices for a city.

    Provides composite indices including cost of living index, rent index,
    groceries index, restaurant price index, and purchasing power index.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with various city indices
    """
    request = modeling.GetIndicesRequest(city=params.city, country=params.country)
    async with get_client(ctx) as client:
        response = await client.get_indices(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_crime_statistics(
    params: CityQueryParams, ctx: Context
) -> dict[str, Any]:
    """Get crime statistics and safety indices for a city.

    Provides information about crime levels and safety perceptions in the city.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with crime statistics and safety indices
    """
    request = modeling.GetCityCrimeRequest(city=params.city, country=params.country)
    async with get_client(ctx) as client:
        response = await client.get_city_crime(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_healthcare(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get healthcare quality indices for a city.

    Provides information about healthcare system quality, accessibility,
    and other health-related metrics.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with healthcare quality indices
    """
    request = modeling.GetCityHealthcareRequest(
        city=params.city,
        country=params.country,
    )
    async with get_client(ctx) as client:
        response = await client.get_city_healthcare(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_traffic(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get traffic and commute information for a city.

    Provides data about traffic conditions, commute times, and transportation efficiency.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with traffic and commute data
    """
    request = modeling.GetCityTrafficRequest(city=params.city, country=params.country)
    async with get_client(ctx) as client:
        response = await client.get_city_traffic(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_pollution(params: CityQueryParams, ctx: Context) -> dict[str, Any]:
    """Get pollution and environmental quality data for a city.

    Provides information about air quality, pollution levels, and environmental indices.

    Args:
        params: Query parameters with city and optional country
        ctx: Request context containing API key

    Returns:
        Dictionary with pollution and environmental data
    """
    request = modeling.GetCityPollutionRequest(
        city=params.city,
        country=params.country,
    )
    async with get_client(ctx) as client:
        response = await client.get_city_pollution(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_country_prices(
    params: CountryQueryParams, ctx: Context
) -> dict[str, Any]:
    """Get average cost of living prices for an entire country.

    Provides country-level aggregated price data.

    Args:
        params: Query parameters with country name
        ctx: Request context containing API key

    Returns:
        Dictionary with country-level price data
    """
    request = modeling.GetCountryPricesRequest(country=params.country)
    async with get_client(ctx) as client:
        response = await client.get_country_prices(request)
    return response.model_dump(by_alias=True)


@mcp.tool()
async def get_city_rankings(
    params: RankingsQueryParams, ctx: Context
) -> list[dict[str, Any]]:
    """Get global city rankings for various categories.

    Provides rankings of cities worldwide based on different metrics.

    Args:
        params: Query parameters with ranking section
        ctx: Request context containing API key

    Returns:
        List of city ranking entries for the specified category
    """
    section = _section_code(params.section)
    request = modeling.GetRankingsByCityCurrentRequest(section=section)
    async with get_client(ctx) as client:
        response = await client.get_rankings_by_city_current(request)
    return [entry.model_dump(by_alias=True) for entry in response.root]


@mcp.tool()
async def get_country_city_rankings(
    params: CountryRankingsQueryParams, ctx: Context
) -> list[dict[str, Any]]:
    """Get city rankings within a specific country.

    Provides rankings of cities within a country based on different metrics.

    Args:
        params: Query parameters with country and ranking section
        ctx: Request context containing API key

    Returns:
        List of ranking entries filtered to the specified country
    """
    section = _section_code(params.section)
    request = modeling.GetRankingsByCityCurrentRequest(section=section)
    async with get_client(ctx) as client:
        rankings = await client.get_rankings_by_city_current(request)

    return [
        entry.model_dump(by_alias=True)
        for entry in rankings.root
        if entry.country == params.country
    ]


def main() -> None:
    """Run the Numbeo MCP server."""

    mcp.run()


if __name__ == "__main__":
    main()
