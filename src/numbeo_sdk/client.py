"""Numbeo API client for fetching cost of living, property prices, and crime data."""

from typing import Any, Optional

import requests


class NumbeoClient:
    """Client for interacting with the Numbeo API.

    This client handles all HTTP communication with the Numbeo API endpoints.
    The API key is required and should be passed during initialization.
    """

    BASE_URL = "https://www.numbeo.com/api"

    def __init__(self, api_key: str):
        """Initialize the Numbeo API client.

        Args:
            api_key: Numbeo API key for authentication.

        Raises:
            ValueError: If api_key is not provided.
        """
        if not api_key:
            raise ValueError("Numbeo API key is required.")
        self.api_key = api_key

    def _make_request(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a request to the Numbeo API.

        Args:
            endpoint: API endpoint path
            params: Additional query parameters

        Returns:
            JSON response from the API

        Raises:
            requests.HTTPError: If the API request fails
        """
        if params is None:
            params = {}

        # Add API key to query parameters
        params["api_key"] = self.api_key

        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        return response.json()

    def get_city_prices(
        self, city: str, country: Optional[str] = None
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

        return self._make_request("city_prices", params)

    def get_city_prices_archive(
        self, city: str, country: Optional[str] = None, currency: Optional[str] = None
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

        return self._make_request("city_prices_archive", params)

    def get_indices(self, city: str, country: Optional[str] = None) -> dict[str, Any]:
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

        return self._make_request("indices", params)

    def get_city_healthcare(
        self, city: str, country: Optional[str] = None
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

        return self._make_request("city_healthcare", params)

    def get_city_traffic(
        self, city: str, country: Optional[str] = None
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

        return self._make_request("city_traffic", params)

    def get_city_pollution(
        self, city: str, country: Optional[str] = None
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

        return self._make_request("city_pollution", params)

    def get_city_crime(
        self, city: str, country: Optional[str] = None
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

        return self._make_request("city_crime", params)

    def get_country_prices(self, country: str) -> dict[str, Any]:
        """Get average prices for a country.

        Args:
            country: Country name

        Returns:
            Dictionary with country-level price data
        """
        params = {"country": country}
        return self._make_request("country_prices", params)

    def get_rankings(self, section: str = "cost-of-living") -> dict[str, Any]:
        """Get city rankings for various categories.

        Args:
            section: Section to get rankings for (e.g., 'cost-of-living', 'crime', 'health-care')

        Returns:
            Dictionary with rankings data
        """
        params = {"section": section}
        return self._make_request("rankings", params)

    def get_rankings_by_country(
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
        return self._make_request("rankings_by_country", params)
