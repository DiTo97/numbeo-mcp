"""Tests for the Numbeo SDK client."""

from unittest.mock import MagicMock, patch

import pytest

from numbeo_sdk import NumbeoClient


class TestNumbeoClient:
    """Test suite for NumbeoClient."""

    def test_client_requires_api_key(self):
        """Test that client raises error without API key."""
        with pytest.raises(ValueError, match="Numbeo API key is required"):
            NumbeoClient(api_key="")

    def test_client_accepts_api_key_parameter(self):
        """Test that client accepts API key via parameter."""
        client = NumbeoClient(api_key="test-key")
        assert client.api_key == "test-key"

    @patch("numbeo_sdk.client.requests.get")
    def test_get_city_prices(self, mock_get):
        """Test get_city_prices method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "New York", "prices": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumbeoClient(api_key="test-key")
        result = client.get_city_prices("New York", "United States")

        assert result == {"city": "New York", "prices": []}
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "api_key" in call_args.kwargs["params"]
        assert call_args.kwargs["params"]["query"] == "New York"
        assert call_args.kwargs["params"]["country"] == "United States"

    @patch("numbeo_sdk.client.requests.get")
    def test_get_city_prices_without_country(self, mock_get):
        """Test get_city_prices without country parameter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Paris", "prices": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumbeoClient(api_key="test-key")
        result = client.get_city_prices("Paris")

        assert result == {"city": "Paris", "prices": []}
        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["query"] == "Paris"
        assert "country" not in call_args.kwargs["params"]

    @patch("numbeo_sdk.client.requests.get")
    def test_get_indices(self, mock_get):
        """Test get_indices method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "city": "London",
            "cost_of_living_index": 85.5,
            "rent_index": 75.2,
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumbeoClient(api_key="test-key")
        result = client.get_indices("London", "United Kingdom")

        assert "cost_of_living_index" in result
        assert result["city"] == "London"

    @patch("numbeo_sdk.client.requests.get")
    def test_get_city_crime(self, mock_get):
        """Test get_city_crime method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Tokyo", "crime_index": 15.3}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumbeoClient(api_key="test-key")
        result = client.get_city_crime("Tokyo", "Japan")

        assert result["city"] == "Tokyo"
        assert "crime_index" in result

    @patch("numbeo_sdk.client.requests.get")
    def test_api_key_included_in_params(self, mock_get):
        """Test that API key is always included in request parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumbeoClient(api_key="secret-key")
        client.get_city_prices("TestCity")

        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["api_key"] == "secret-key"

    @patch("numbeo_sdk.client.requests.get")
    def test_request_timeout(self, mock_get):
        """Test that requests include timeout."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumbeoClient(api_key="test-key")
        client.get_city_prices("TestCity")

        call_args = mock_get.call_args
        assert call_args.kwargs["timeout"] == 30
