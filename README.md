# Numbeo API MCP Server 🌍

FastMCP server wrapping the [Numbeo API](https://www.numbeo.com/api/doc.jsp), providing data on cost of living, property prices, and crime rates worldwide.

## Architecture

This repository contains two Python packages:

### 📦 `numbeo-sdk`
The Numbeo SDK is a standalone Python client library for the Numbeo API. It handles all HTTP communication and provides a clean interface to access Numbeo data.

### 🖥️ `numbeo-mcp`  
The Numbeo MCP server is a FastMCP server that exposes the SDK functionality as MCP tools with:
- **Strict validation** using Pydantic schemas
- **Bearer token authentication** - API key provided by client and propagated to SDK
- **Vocabulary resource** - explains Numbeo API terminology
- **10 MCP tools** - covering all major Numbeo endpoints

## Features

- 🏙️ **Cost of Living Data**: Get current and historical prices for cities and countries
- 🏠 **Property Prices**: Access real estate market data
- 🚨 **Crime Statistics**: Retrieve safety and crime indices
- 📊 **City Indices**: Compare quality of life, healthcare, traffic, and pollution metrics
- 🏆 **Rankings**: Global and country-specific city rankings
- 🔐 **Secure Authentication**: API key passed from MCP client to SDK

## Getting Started

### Prerequisites

- Python 3.12 or higher
- A Numbeo API key (obtain from [Numbeo API](https://www.numbeo.com/api/))

### Installation

Install the package:

```bash
pip install -e .
```

Or using uv:

```bash
uv sync
```

### Running the MCP Server

Start the MCP server:

```bash
numbeo-mcp
```

The server will start and expose 10 MCP tools plus a vocabulary resource.

### Authentication

The MCP server expects the API key to be provided by the client through one of:
- `api_key` field in the request metadata
- `Authorization: Bearer <api-key>` header

The API key is not verified by the MCP server but is propagated to the Numbeo SDK, which uses it in API calls.

## Available Tools

### Cost of Living Tools

- **`get_city_cost_of_living`**: Get current prices for goods and services in a city
- **`get_city_cost_of_living_archive`**: Get historical price data  
- **`get_city_indices`**: Get cost of living, rent, and purchasing power indices
- **`get_country_prices`**: Get average prices for an entire country

### Quality of Life Tools

- **`get_city_healthcare`**: Healthcare quality indices
- **`get_city_traffic`**: Traffic and commute data
- **`get_city_pollution`**: Environmental quality metrics

### Safety Tools

- **`get_city_crime_statistics`**: Crime rates and safety indices

### Rankings Tools

- **`get_city_rankings`**: Global city rankings by category
- **`get_country_city_rankings`**: City rankings within a specific country

## Vocabulary Resource

The server provides a `vocabulary://numbeo-terms` resource that explains Numbeo API terminology:
- `contributors12months`: Contributors in past 12 months
- `monthLastUpdate`: Month of last update
- `yearLastUpdate`: Year of last update
- `contributors`: Total contributors (adaptive archive policy)
- `cpi_factor`: Consumer Price Index calculation factor
- `rent_factor`: Rent Index calculation factor

## Using the SDK Directly

You can also use the Numbeo SDK directly in your Python code:

```python
from numbeo_sdk import NumbeoClient

# Initialize client with API key
client = NumbeoClient(api_key="your-api-key")

# Get cost of living data
data = client.get_city_prices("London", "United Kingdom")
print(data)

# Get crime statistics
crime = client.get_city_crime("Tokyo", "Japan")
print(crime)

# Get rankings
rankings = client.get_rankings("cost-of-living")
print(rankings)
```

## Development

### Linting

```bash
ruff check
```

### Formatting

```bash
ruff format
```

### Running Tests

```bash
pytest tests/
```

## Package Structure

```
src/
├── numbeo_sdk/          # Numbeo API SDK
│   ├── __init__.py
│   └── client.py        # HTTP client for Numbeo API
└── numbeo_mcp_new/      # FastMCP server
    ├── __init__.py
    ├── server.py        # MCP server with tools
    └── schemas.py       # Pydantic validation schemas
```

## API Reference

This server wraps the Numbeo API endpoints. For detailed information about the data returned, see the [Numbeo API Documentation](https://www.numbeo.com/api/doc.jsp).

Key features:
- All SDK requests include the API key as a query parameter
- MCP server uses strict input validation with Pydantic
- No authentication headers required (Bearer token from client → SDK)
- Returns JSON data with comprehensive city/country statistics

## License

See [LICENSE](LICENSE) file for details.
