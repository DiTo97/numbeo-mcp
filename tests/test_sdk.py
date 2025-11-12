"""Tests for the Numbeo SDK client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from numbeo_sdk import Numbeo


class TestNumbeo:
    """Test suite for Numbeo."""

    def test_client_requires_api_key(self):
        """Test that client raises error without API key."""
        with pytest.raises(ValueError, match="Numbeo API key is required"):
            Numbeo(key="")

    def test_client_accepts_api_key_parameter(self):
        """Test that client accepts API key via parameter."""
        client = Numbeo(key="test-key")
        assert client.key == "test-key"

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_client_timeout_set(self, mock_client_class):
        """Test that client is initialized with timeout."""
        _ = Numbeo(key="test-key")
        
        # Check that AsyncClient was called with timeout
        mock_client_class.assert_called_once_with(timeout=30.0)

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_city_prices_without_country(self, mock_client_class):
        """Test get_city_prices without country parameter."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Paris", "prices": []}
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_city_prices("Paris")

        assert result == {"city": "Paris", "prices": []}
        call_args = mock_client.get.call_args
        assert call_args.kwargs["params"]["query"] == "Paris"
        assert "country" not in call_args.kwargs["params"]

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_indices(self, mock_client_class):
        """Test get_indices method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "city": "London",
            "cost_of_living_index": 85.5,
            "rent_index": 75.2,
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_indices("London", "United Kingdom")

        assert "cost_of_living_index" in result
        assert result["city"] == "London"

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_city_crime(self, mock_client_class):
        """Test get_city_crime method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Tokyo", "crime_index": 15.3}
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_city_crime("Tokyo", "Japan")

        assert result["city"] == "Tokyo"
        assert "crime_index" in result

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_api_key_included_in_params(self, mock_client_class):
        """Test that API key is always included in request parameters."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="secret-key")
        await client.get_city_prices("TestCity")

        call_args = mock_client.get.call_args
        assert call_args.kwargs["params"]["api_key"] == "secret-key"

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_cities(self, mock_client_class):
        """Test get_cities method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cities": [
                {"country": "Brazil", "city": "Sao Paulo", "city_id": 7392}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_cities()

        assert "cities" in result
        assert len(result["cities"]) > 0

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_items(self, mock_client_class):
        """Test get_items method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {"category": "Restaurants", "item_id": 3, "name": "McMeal"}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_items()

        assert "items" in result

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_currency_exchange_rates(self, mock_client_class):
        """Test get_currency_exchange_rates method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "exchange_rates": [
                {"currency": "AED", "one_usd_to_currency": 3.67}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_currency_exchange_rates()

        assert "exchange_rates" in result

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_city_cost_estimator(self, mock_client_class):
        """Test get_city_cost_estimator method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "city_name": "London, United Kingdom",
            "overall_estimate": 11745.34
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_city_cost_estimator(
            query="London, United Kingdom",
            household_members=4,
            children=2,
            include_rent=True
        )

        assert "overall_estimate" in result
        assert result["city_name"] == "London, United Kingdom"

    @patch("numbeo_sdk.client.httpx.AsyncClient")
    @pytest.mark.asyncio
    async def test_get_historical_currency_exchange_rates(self, mock_client_class):
        """Test get_historical_currency_exchange_rates method."""
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "month": 3,
            "year": 2014,
            "exchange_rates": []
        }
        mock_response.raise_for_status = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = Numbeo(key="test-key")
        result = await client.get_historical_currency_exchange_rates(month=3, year=2014)

        assert result["month"] == 3
        assert result["year"] == 2014
