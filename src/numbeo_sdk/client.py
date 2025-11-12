"""Numbeo API client for fetching cost of living, property prices, and crime data."""

from typing import Any

import httpx


class Numbeo:
    """Client for interacting with the Numbeo API.

    This client handles all HTTP communication with the Numbeo API endpoints.
    The API key is required and should be passed during initialization.
    """

    URL = "https://www.numbeo.com/api"

    def __init__(self, key: str):
        """Initialize the Numbeo API client.

        Args:
            key: Numbeo API key for authentication.

        Raises:
            ValueError: If key is not provided.
        """
        if not key:
            raise ValueError("Numbeo API key is required.")
        self.key = key
        self._client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._client.aclose()

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def _make_request(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a request to the Numbeo API.

        Args:
            endpoint: API endpoint path
            params: Additional query parameters

        Returns:
            JSON response from the API

        Raises:
            httpx.HTTPError: If the API request fails
        """
        if params is None:
            params = {}

        # Add API key to query parameters
        params["api_key"] = self.key

        url = f"{self.URL}/{endpoint}"
        response = await self._client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    async def get_city_prices(
        self, city: str, country: str | None = None
    ) -> dict[str, Any]:
        """Get cost of living prices for a specific city.

        Args:
            city: City name
            country: Optional country name for disambiguation

        Returns:
            Dictionary with price data for the city
        """
        params = {"query": city}
        if country:
            params["country"] = country

        return await self._make_request("city_prices", params)

    async def get_city_prices_archive(
        self, city: str, country: str | None = None, currency: str | None = None
    ) -> dict[str, Any]:
        """Get historical cost of living data for a city.

        Args:
            city: City name
            country: Optional country name
            currency: Optional currency code (e.g., USD, EUR)

        Returns:
            Dictionary with historical price data
        """
        params = {"query": city}
        if country:
            params["country"] = country
        if currency:
            params["currency"] = currency

        return await self._make_request("city_prices_archive", params)

    async def get_indices(self, city: str, country: str | None = None) -> dict[str, Any]:
        """Get various indices for a city (cost of living, rent, etc.).

        Args:
            city: City name
            country: Optional country name

        Returns:
            Dictionary with various city indices
        """
        params = {"query": city}
        if country:
            params["country"] = country

        return await self._make_request("indices", params)

    async def get_city_healthcare(
        self, city: str, country: str | None = None
    ) -> dict[str, Any]:
        """Get healthcare quality indices for a city.

        Args:
            city: City name
            country: Optional country name

        Returns:
            Dictionary with healthcare indices
        """
        params = {"query": city}
        if country:
            params["country"] = country

        return await self._make_request("city_healthcare", params)

    async def get_city_traffic(
        self, city: str, country: str | None = None
    ) -> dict[str, Any]:
        """Get traffic and commute data for a city.

        Args:
            city: City name
            country: Optional country name

        Returns:
            Dictionary with traffic indices
        """
        params = {"query": city}
        if country:
            params["country"] = country

        return await self._make_request("city_traffic", params)

    async def get_city_pollution(
        self, city: str, country: str | None = None
    ) -> dict[str, Any]:
        """Get pollution indices for a city.

        Args:
            city: City name
            country: Optional country name

        Returns:
            Dictionary with pollution data
        """
        params = {"query": city}
        if country:
            params["country"] = country

        return await self._make_request("city_pollution", params)

    async def get_city_crime(
        self, city: str, country: str | None = None
    ) -> dict[str, Any]:
        """Get crime statistics for a city.

        Args:
            city: City name
            country: Optional country name

        Returns:
            Dictionary with crime data
        """
        params = {"query": city}
        if country:
            params["country"] = country

        return await self._make_request("city_crime", params)

    async def get_country_prices(self, country: str) -> dict[str, Any]:
        """Get average prices for a country.

        Args:
            country: Country name

        Returns:
            Dictionary with country-level price data
        """
        params = {"country": country}
        return await self._make_request("country_prices", params)

    async def get_rankings(self, section: str = "cost-of-living") -> dict[str, Any]:
        """Get city rankings for various categories.

        Args:
            section: Section to get rankings for (e.g., 'cost-of-living', 'crime', 'health-care')

        Returns:
            Dictionary with rankings data
        """
        params = {"section": section}
        return await self._make_request("rankings", params)

    async def get_rankings_by_country(
        self, country: str, section: str = "cost-of-living"
    ) -> dict[str, Any]:
        """Get city rankings within a specific country.

        Args:
            country: Country name
            section: Section to get rankings for

        Returns:
            Dictionary with country-specific rankings
        """
        params = {"country": country, "section": section}
        return await self._make_request("rankings_by_country", params)

    async def get_cities(self, country: str | None = None) -> dict[str, Any]:
        """Get a list of cities in the Numbeo database.

        Args:
            country: Optional country name or ISO 3166 code

        Returns:
            Dictionary with list of cities
        """
        params = {}
        if country:
            params["country"] = country
        return await self._make_request("cities", params)

    async def get_items(self) -> dict[str, Any]:
        """Get a list of items from the cost of living section.

        Returns:
            Dictionary with list of items
        """
        return await self._make_request("items", {})

    async def get_currency_exchange_rates(self) -> dict[str, Any]:
        """Get current exchange rates used by Numbeo.

        Returns:
            Dictionary with exchange rates
        """
        return await self._make_request("currency_exchange_rates", {})

    async def get_city_cost_estimator(
        self,
        query: str | None = None,
        city: str | None = None,
        country: str | None = None,
        city_id: int | None = None,
        strict_matching: bool | None = None,
        currency: str | None = None,
        household_members: int | None = None,
        children: int | None = None,
        include_rent: bool | None = None,
    ) -> dict[str, Any]:
        """Estimate the cost of living for an individual or family in a city.

        Args:
            query: Name of place or lat/long coordinates
            city: City name as listed in Numbeo database
            country: Country name or ISO 3166 code
            city_id: Internal city id
            strict_matching: If False, resolves to major city when possible
            currency: Currency for the result
            household_members: Number of household members (default: 4)
            children: Number of children for preschool/school fees (default: 0)
            include_rent: Include rental cost in estimate (default: false)

        Returns:
            Dictionary with cost estimate and breakdown
        """
        params = {}
        if query:
            params["query"] = query
        if city:
            params["city"] = city
        if country:
            params["country"] = country
        if city_id is not None:
            params["city_id"] = city_id
        if strict_matching is not None:
            params["strict_matching"] = strict_matching
        if currency:
            params["currency"] = currency
        if household_members is not None:
            params["household_members"] = household_members
        if children is not None:
            params["children"] = children
        if include_rent is not None:
            params["include_rent"] = include_rent
        return await self._make_request("city_cost_estimator", params)

    async def get_close_cities_with_prices(
        self,
        query: str,
        max_distance: int | None = None,
        min_contributors: int | None = None,
    ) -> dict[str, Any]:
        """Get nearby cities that have price data.

        Args:
            query: Name of place or lat/long coordinates
            max_distance: Max distance in km to look for cities (default: 200)
            min_contributors: Minimum number of contributors (default: 10)

        Returns:
            Dictionary with nearby cities
        """
        params = {"query": query}
        if max_distance is not None:
            params["max_distance"] = max_distance
        if min_contributors is not None:
            params["min_contributors"] = min_contributors
        return await self._make_request("close_cities_with_prices", params)

    async def get_country_administrative_units(self, country: str) -> list[str]:
        """Get list of administrative units within a country.

        Args:
            country: Country name or ISO 3166 code

        Returns:
            List of administrative unit names
        """
        params = {"country": country}
        return await self._make_request("country_administrative_units", params)

    async def get_administrative_unit_prices(
        self,
        country: str,
        administrative_unit: str | None = None,
        admin_name: str | None = None,
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Get prices for a specified administrative unit.

        Args:
            country: Country name or ISO 3166 code
            administrative_unit: Name of the administrative unit
            admin_name: Alternative parameter for administrative unit name
            currency: Currency for the result

        Returns:
            Dictionary with price data for the administrative unit
        """
        params = {"country": country}
        # Support both parameter names from the API spec
        if administrative_unit:
            params["administrative_unit"] = administrative_unit
        if admin_name:
            params["admin_name"] = admin_name
        if currency:
            params["currency"] = currency
        return await self._make_request("administrative_unit_prices", params)

    async def get_historical_city_prices(
        self,
        query: str | None = None,
        city: str | None = None,
        country: str | None = None,
        city_id: int | None = None,
        strict_matching: bool | None = None,
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Get historical average prices per year for a city.

        Args:
            query: Name of place or lat/long coordinates
            city: City name as listed in Numbeo database
            country: Country name or ISO 3166 code
            city_id: Internal city id
            strict_matching: If False, resolves to major city when possible
            currency: Currency for the result

        Returns:
            Dictionary with historical price data
        """
        params = {}
        if query:
            params["query"] = query
        if city:
            params["city"] = city
        if country:
            params["country"] = country
        if city_id is not None:
            params["city_id"] = city_id
        if strict_matching is not None:
            params["strict_matching"] = strict_matching
        if currency:
            params["currency"] = currency
        return await self._make_request("historical_city_prices", params)

    async def get_historical_country_prices(
        self, country: str, currency: str | None = None
    ) -> dict[str, Any]:
        """Get historical average prices per year for a country.

        Args:
            country: Country name or ISO 3166 code
            currency: Currency for the result

        Returns:
            Dictionary with historical price data
        """
        params = {"country": country}
        if currency:
            params["currency"] = currency
        return await self._make_request("historical_country_prices", params)

    async def get_historical_country_prices_monthly(
        self, country: str, currency: str | None = None
    ) -> dict[str, Any]:
        """Get historical average prices per month for a country.

        Args:
            country: Country name or ISO 3166 code
            currency: Currency for the result

        Returns:
            Dictionary with historical monthly price data
        """
        params = {"country": country}
        if currency:
            params["currency"] = currency
        return await self._make_request("historical_country_prices_monthly", params)

    async def get_historical_currency_exchange_rates(
        self, month: int, year: int
    ) -> dict[str, Any]:
        """Get historical exchange rates for a specific month and year.

        Args:
            month: Month (1-12)
            year: Year

        Returns:
            Dictionary with historical exchange rates
        """
        params = {"month": month, "year": year}
        return await self._make_request("historical_currency_exchange_rates", params)

    async def get_city_prices_raw(
        self,
        query: str | None = None,
        city: str | None = None,
        country: str | None = None,
        city_id: int | None = None,
        strict_matching: bool | None = None,
        since_internal_id: int | None = None,
    ) -> dict[str, Any]:
        """Get raw recent price data entries for a city.

        Args:
            query: Name of place or lat/long coordinates
            city: City name as listed in Numbeo database
            country: Country name or ISO 3166 code
            city_id: Internal city id
            strict_matching: If False, resolves to major city when possible
            since_internal_id: Return only entries with internal_id >= this value

        Returns:
            Dictionary with raw price entries
        """
        params = {}
        if query:
            params["query"] = query
        if city:
            params["city"] = city
        if country:
            params["country"] = country
        if city_id is not None:
            params["city_id"] = city_id
        if strict_matching is not None:
            params["strict_matching"] = strict_matching
        if since_internal_id is not None:
            params["since_internal_id"] = since_internal_id
        return await self._make_request("city_prices_raw", params)

    async def get_city_prices_raw_deletion_log(
        self, since_log_id: int | None = None
    ) -> dict[str, Any]:
        """Get IDs of entries removed from city_prices_raw as spam.

        Args:
            since_log_id: Return only entries with log_id >= this value

        Returns:
            Dictionary with deletion log entries
        """
        params = {}
        if since_log_id is not None:
            params["since_log_id"] = since_log_id
        return await self._make_request("city_prices_raw_deletion_log", params)

    async def get_city_prices_archive_raw(
        self,
        query: str | None = None,
        city: str | None = None,
        country: str | None = None,
        city_id: int | None = None,
        strict_matching: bool | None = None,
    ) -> dict[str, Any]:
        """Get archived raw price data entries for a city.

        Args:
            query: Name of place or lat/long coordinates
            city: City name as listed in Numbeo database
            country: Country name or ISO 3166 code
            city_id: Internal city id
            strict_matching: If False, resolves to major city when possible

        Returns:
            Dictionary with archived raw price entries
        """
        params = {}
        if query:
            params["query"] = query
        if city:
            params["city"] = city
        if country:
            params["country"] = country
        if city_id is not None:
            params["city_id"] = city_id
        if strict_matching is not None:
            params["strict_matching"] = strict_matching
        return await self._make_request("city_prices_archive_raw", params)
