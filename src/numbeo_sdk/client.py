"""Asynchronous Numbeo API client."""

from typing import Any

import httpx

from . import modeling


class Numbeo:
    """Client for interacting with the Numbeo HTTP API."""

    URL = "https://www.numbeo.com/api"

    def __init__(self, key: str, *, timeout: float = 30.0):
        """Initialize the Numbeo API client.

        Args:
            key: Numbeo API key for authentication.

        Raises:
            ValueError: If key is not provided.
        """
        if not key:
            raise ValueError("Numbeo API key is required.")
        self.key = key
        self._client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self) -> "Numbeo":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client if owned by this instance."""
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

        response = await self._client.get(f"{self.URL}/{endpoint}", params=query)
        response.raise_for_status()
        return response.json()

    def _prepare_params(self, request: modeling.RequestModel | None) -> dict[str, Any]:
        if request is None:
            return {}
        return request.model_dump(by_alias=True, exclude_none=True)

    async def get_cities(
        self, request: modeling.GetCitiesRequest | None = None
    ) -> modeling.GetCitiesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("cities", params)
        return modeling.GetCitiesResponse.model_validate(data)

    async def get_items(
        self, request: modeling.GetItemsRequest | None = None
    ) -> modeling.GetItemsResponse:
        params = self._prepare_params(request)
        data = await self._make_request("items", params)
        return modeling.GetItemsResponse.model_validate(data)

    async def get_currency_exchange_rates(
        self, request: modeling.GetCurrencyExchangeRatesRequest | None = None
    ) -> modeling.GetCurrencyExchangeRatesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("currency_exchange_rates", params)
        return modeling.GetCurrencyExchangeRatesResponse.model_validate(data)

    async def get_city_prices(
        self, request: modeling.GetCityPricesRequest
    ) -> modeling.GetCityPricesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("city_prices", params)
        return modeling.GetCityPricesResponse.model_validate(data)

    async def get_country_prices(
        self, request: modeling.GetCountryPricesRequest
    ) -> modeling.GetCountryPricesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_prices", params)
        return modeling.GetCountryPricesResponse.model_validate(data)

    async def get_city_cost_estimator(
        self, request: modeling.GetCityCostEstimatorRequest
    ) -> modeling.GetCityCostEstimatorResponse:
        params = self._prepare_params(request)
        data = await self._make_request("city_cost_estimator", params)
        return modeling.GetCityCostEstimatorResponse.model_validate(data)

    async def get_close_cities_with_prices(
        self, request: modeling.GetCloseCitiesWithPricesRequest
    ) -> modeling.GetCloseCitiesWithPricesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("close_cities_with_prices", params)
        return modeling.GetCloseCitiesWithPricesResponse.model_validate(data)

    async def get_country_administrative_units(
        self, request: modeling.GetCountryAdministrativeUnitsRequest
    ) -> modeling.GetCountryAdministrativeUnitsResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_administrative_units", params)
        return modeling.GetCountryAdministrativeUnitsResponse.model_validate(data)

    async def get_administrative_unit_prices(
        self, request: modeling.GetAdministrativeUnitPricesRequest
    ) -> modeling.GetAdministrativeUnitPricesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("administrative_unit_prices", params)
        return modeling.GetAdministrativeUnitPricesResponse.model_validate(data)

    async def get_historical_city_prices(
        self, request: modeling.GetHistoricalCityPricesRequest
    ) -> modeling.GetHistoricalCityPricesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("historical_city_prices", params)
        return modeling.GetHistoricalCityPricesResponse.model_validate(data)

    async def get_historical_country_prices(
        self, request: modeling.GetHistoricalCountryPricesRequest
    ) -> modeling.GetHistoricalCountryPricesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("historical_country_prices", params)
        return modeling.GetHistoricalCountryPricesResponse.model_validate(data)

    async def get_historical_country_prices_monthly(
        self, request: modeling.GetHistoricalCountryPricesMonthlyRequest
    ) -> modeling.GetHistoricalCountryPricesMonthlyResponse:
        params = self._prepare_params(request)
        data = await self._make_request("historical_country_prices_monthly", params)
        return modeling.GetHistoricalCountryPricesMonthlyResponse.model_validate(data)

    async def get_historical_currency_exchange_rates(
        self, request: modeling.GetHistoricalCurrencyExchangeRatesRequest
    ) -> modeling.GetHistoricalCurrencyExchangeRatesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("historical_currency_exchange_rates", params)
        return modeling.GetHistoricalCurrencyExchangeRatesResponse.model_validate(data)

    async def get_indices(
        self, request: modeling.GetIndicesRequest
    ) -> modeling.GetIndicesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("indices", params)
        return modeling.GetIndicesResponse.model_validate(data)

    async def get_country_indices(
        self, request: modeling.GetCountryIndicesRequest | None = None
    ) -> modeling.GetCountryIndicesResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_indices", params)
        return modeling.GetCountryIndicesResponse.model_validate(data)

    async def get_city_crime(
        self, request: modeling.GetCityCrimeRequest
    ) -> modeling.GetCityCrimeResponse:
        params = self._prepare_params(request)
        data = await self._make_request("city_crime", params)
        return modeling.GetCityCrimeResponse.model_validate(data)

    async def get_city_healthcare(
        self, request: modeling.GetCityHealthcareRequest
    ) -> modeling.GetCityHealthcareResponse:
        params = self._prepare_params(request)
        data = await self._make_request("city_healthcare", params)
        return modeling.GetCityHealthcareResponse.model_validate(data)

    async def get_city_pollution(
        self, request: modeling.GetCityPollutionRequest
    ) -> modeling.GetCityPollutionResponse:
        params = self._prepare_params(request)
        data = await self._make_request("city_pollution", params)
        return modeling.GetCityPollutionResponse.model_validate(data)

    async def get_city_traffic(
        self, request: modeling.GetCityTrafficRequest
    ) -> modeling.GetCityTrafficResponse:
        params = self._prepare_params(request)
        data = await self._make_request("city_traffic", params)
        return modeling.GetCityTrafficResponse.model_validate(data)

    async def get_country_crime(
        self, request: modeling.GetCountryCrimeRequest | None = None
    ) -> modeling.GetCountryCrimeResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_crime", params)
        return modeling.GetCountryCrimeResponse.model_validate(data)

    async def get_country_healthcare(
        self, request: modeling.GetCountryHealthcareRequest | None = None
    ) -> modeling.GetCountryHealthcareResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_healthcare", params)
        return modeling.GetCountryHealthcareResponse.model_validate(data)

    async def get_country_pollution(
        self, request: modeling.GetCountryPollutionRequest | None = None
    ) -> modeling.GetCountryPollutionResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_pollution", params)
        return modeling.GetCountryPollutionResponse.model_validate(data)

    async def get_country_traffic(
        self, request: modeling.GetCountryTrafficRequest | None = None
    ) -> modeling.GetCountryTrafficResponse:
        params = self._prepare_params(request)
        data = await self._make_request("country_traffic", params)
        return modeling.GetCountryTrafficResponse.model_validate(data)

    async def get_rankings_by_city_current(
        self, request: modeling.GetRankingsByCityCurrentRequest
    ) -> modeling.GetRankingsByCityCurrentResponse:
        params = self._prepare_params(request)
        data = await self._make_request("rankings_by_city_current", params)
        return modeling.GetRankingsByCityCurrentResponse.model_validate(data)

    async def get_rankings_by_city_historical(
        self, request: modeling.GetRankingsByCityHistoricalRequest
    ) -> modeling.GetRankingsByCityHistoricalResponse:
        params = self._prepare_params(request)
        data = await self._make_request("rankings_by_city_historical", params)
        return modeling.GetRankingsByCityHistoricalResponse.model_validate(data)

    async def get_rankings_by_country_historical(
        self, request: modeling.GetRankingsByCountryHistoricalRequest
    ) -> modeling.GetRankingsByCountryHistoricalResponse:
        params = self._prepare_params(request)
        data = await self._make_request("rankings_by_country_historical", params)
        return modeling.GetRankingsByCountryHistoricalResponse.model_validate(data)
