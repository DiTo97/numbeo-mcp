"""Tests for the Numbeo API client and MCP server."""

import os
from unittest.mock import MagicMock, patch

import pytest

from numbeo_mcp.client import NumberoAPIClient


class TestNumbeoAPIClient:
    """Test suite for NumberoAPIClient."""

    def test_client_requires_api_key(self):
        """Test that client raises error without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Numbeo API key is required"):
                NumberoAPIClient()

    def test_client_accepts_api_key_parameter(self):
        """Test that client accepts API key via parameter."""
        client = NumberoAPIClient(api_key="test-key")
        assert client.api_key == "test-key"

    def test_client_reads_api_key_from_env(self):
        """Test that client reads API key from environment variable."""
        with patch.dict(os.environ, {"NUMBEO_API_KEY": "env-test-key"}):
            client = NumberoAPIClient()
            assert client.api_key == "env-test-key"

    @patch("numbeo_mcp.client.requests.get")
    def test_get_city_prices(self, mock_get):
        """Test get_city_prices method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "New York", "prices": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_city_prices("New York", "United States")

        assert result == {"city": "New York", "prices": []}
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "api_key" in call_args.kwargs["params"]
        assert call_args.kwargs["params"]["query"] == "New York"
        assert call_args.kwargs["params"]["country"] == "United States"

    @patch("numbeo_mcp.client.requests.get")
    def test_get_city_prices_without_country(self, mock_get):
        """Test get_city_prices without country parameter."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Paris", "prices": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_city_prices("Paris")

        assert result == {"city": "Paris", "prices": []}
        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["query"] == "Paris"
        assert "country" not in call_args.kwargs["params"]

    @patch("numbeo_mcp.client.requests.get")
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

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_indices("London", "United Kingdom")

        assert "cost_of_living_index" in result
        assert result["city"] == "London"

    @patch("numbeo_mcp.client.requests.get")
    def test_get_city_crime(self, mock_get):
        """Test get_city_crime method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Tokyo", "crime_index": 15.3}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_city_crime("Tokyo", "Japan")

        assert result["city"] == "Tokyo"
        assert "crime_index" in result

    @patch("numbeo_mcp.client.requests.get")
    def test_get_city_healthcare(self, mock_get):
        """Test get_city_healthcare method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"city": "Berlin", "healthcare_index": 75.0}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_city_healthcare("Berlin", "Germany")

        assert result["city"] == "Berlin"
        assert "healthcare_index" in result

    @patch("numbeo_mcp.client.requests.get")
    def test_get_rankings(self, mock_get):
        """Test get_rankings method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"rankings": [{"city": "City1", "rank": 1}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_rankings("cost-of-living")

        assert "rankings" in result
        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["section"] == "cost-of-living"

    @patch("numbeo_mcp.client.requests.get")
    def test_get_country_prices(self, mock_get):
        """Test get_country_prices method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"country": "Germany", "prices": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        result = client.get_country_prices("Germany")

        assert result["country"] == "Germany"
        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["country"] == "Germany"

    @patch("numbeo_mcp.client.requests.get")
    def test_api_key_included_in_params(self, mock_get):
        """Test that API key is always included in request parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="secret-key")
        client.get_city_prices("TestCity")

        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["api_key"] == "secret-key"

    @patch("numbeo_mcp.client.requests.get")
    def test_request_timeout(self, mock_get):
        """Test that requests include timeout."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        client.get_city_prices("TestCity")

        call_args = mock_get.call_args
        assert call_args.kwargs["timeout"] == 30

    @patch("numbeo_mcp.client.requests.get")
    def test_http_error_handling(self, mock_get):
        """Test that HTTP errors are properly raised."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_response

        client = NumberoAPIClient(api_key="test-key")
        with pytest.raises(Exception, match="HTTP Error"):
            client.get_city_prices("TestCity")
