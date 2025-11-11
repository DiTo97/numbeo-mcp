"""Pydantic schemas for Numbeo MCP server tool validation."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class CityQueryParams(BaseModel):
    """Parameters for city-based queries."""

    city: str = Field(
        ..., description="Name of the city (e.g., 'New York', 'London', 'Tokyo')"
    )
    country: Optional[str] = Field(
        None,
        description="Optional country name for disambiguation (e.g., 'United States', 'United Kingdom')",
    )


class CityArchiveQueryParams(BaseModel):
    """Parameters for city archive queries."""

    city: str = Field(..., description="Name of the city")
    country: Optional[str] = Field(
        None, description="Optional country name for disambiguation"
    )
    currency: Optional[str] = Field(
        None, description="Optional currency code (e.g., 'USD', 'EUR', 'GBP')"
    )


class CountryQueryParams(BaseModel):
    """Parameters for country-based queries."""

    country: str = Field(
        ...,
        description="Name of the country (e.g., 'United States', 'Germany', 'Japan')",
    )


class RankingsQueryParams(BaseModel):
    """Parameters for rankings queries."""

    section: Literal[
        "cost-of-living",
        "crime",
        "health-care",
        "pollution",
        "traffic",
        "quality-of-life",
    ] = Field(
        "cost-of-living",
        description="Category for rankings: 'cost-of-living', 'crime', 'health-care', 'pollution', 'traffic', or 'quality-of-life'",
    )


class CountryRankingsQueryParams(BaseModel):
    """Parameters for country-specific rankings queries."""

    country: str = Field(..., description="Name of the country")
    section: Literal[
        "cost-of-living",
        "crime",
        "health-care",
        "pollution",
        "traffic",
        "quality-of-life",
    ] = Field(
        "cost-of-living",
        description="Category for rankings",
    )
