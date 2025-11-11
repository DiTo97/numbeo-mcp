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

**Authentication Flow:**
```
MCP Client → MCP Server → Numbeo SDK → Numbeo API
  (Bearer)    (propagate)   (use in query params)
```

## Available MCP Tools

### Cost of Living Tools

#### `get_city_cost_of_living`
Get current prices for goods and services in a city.

**Parameters:**
- `city` (string, required): Name of the city (e.g., "New York", "London")
- `country` (string, optional): Country name for disambiguation

**Example:**
```json
{
  "city": "New York",
  "country": "United States"
}
```

#### `get_city_cost_of_living_archive`
Get historical cost of living data for trend analysis.

**Parameters:**
- `city` (string, required): Name of the city
- `country` (string, optional): Country name
- `currency` (string, optional): Currency code (e.g., "USD", "EUR")

#### `get_city_indices`
Get composite indices including cost of living, rent, groceries, and purchasing power.

**Parameters:**
- `city` (string, required): Name of the city
- `country` (string, optional): Country name

#### `get_country_prices`
Get average prices at the country level.

**Parameters:**
- `country` (string, required): Name of the country

### Quality of Life Tools

#### `get_city_healthcare`
Get healthcare quality and accessibility indices.

**Parameters:**
- `city` (string, required): Name of the city
- `country` (string, optional): Country name

#### `get_city_traffic`
Get traffic conditions and commute time data.

**Parameters:**
- `city` (string, required): Name of the city
- `country` (string, optional): Country name

#### `get_city_pollution`
Get air quality and environmental indices.

**Parameters:**
- `city` (string, required): Name of the city
- `country` (string, optional): Country name

### Safety Tools

#### `get_city_crime_statistics`
Get crime rates and safety perception indices.

**Parameters:**
- `city` (string, required): Name of the city
- `country` (string, optional): Country name

### Rankings Tools

#### `get_city_rankings`
Get global city rankings for various categories.

**Parameters:**
- `section` (string, optional, default: "cost-of-living"): Category for rankings
  - `"cost-of-living"`: Overall cost of living
  - `"crime"`: Safety rankings
  - `"health-care"`: Healthcare quality
  - `"pollution"`: Environmental quality
  - `"traffic"`: Traffic and commute
  - `"quality-of-life"`: Overall quality of life

#### `get_country_city_rankings`
Get city rankings within a specific country.

**Parameters:**
- `country` (string, required): Name of the country
- `section` (string, optional): Same options as `get_city_rankings`

## Vocabulary Resource

The server provides a `vocabulary://numbeo-terms` resource that explains terminology used in Numbeo API responses:

- **`contributors12months`**: The number of contributors who have submitted data in the past 12 months
- **`monthLastUpdate`**: The month when the data was last updated
- **`yearLastUpdate`**: The year of the last update
- **`contributors`**: The total number of contributors whose data was used in the calculations (adaptive archive policy)
- **`cpi_factor`**: A factor used to calculate our Consumer Price Index. Multiply this factor by the prices and add the result to the overall sum to compute the Cost of Living Index
- **`rent_factor`**: A factor used to calculate our Rent Index. Multiply this factor by the prices and add the result to the overall sum to compute the Rent Index

## Using with MCP Clients

### Claude Desktop

The MCP client should provide the API key through request metadata or authorization headers. Example configuration:

```json
{
  "mcpServers": {
    "numbeo": {
      "command": "numbeo-mcp"
    }
  }
}
```

Then pass the API key in tool calls via the client's authorization mechanism.

### Other MCP Clients

The server supports standard MCP protocol over stdio. API key should be passed through:
- Request metadata (`api_key` field), or
- Authorization header (`Authorization: Bearer <key>`)

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

### Setup

```bash
uv sync --dev
```

### Linting

```bash
make linting
```

### Formatting

```bash
make style
```

### Running Tests

```bash
make test
```

### Export Requirements

```bash
make export
```

## Package Structure

```
src/
├── numbeo_sdk/          # Numbeo API SDK
│   ├── __init__.py
│   └── client.py        # HTTP client for Numbeo API
└── numbeo_mcp/          # FastMCP server
    ├── __init__.py
    ├── server.py        # MCP server with tools
    └── schemas.py       # Pydantic validation schemas
```

## Validation

The MCP server uses **strict input validation** with Pydantic schemas. All tool parameters are validated before being passed to the SDK:

- **CityQueryParams**: city (required), country (optional)
- **CityArchiveQueryParams**: city, country, currency (all validated)
- **RankingsQueryParams**: section with enum validation
- And more...

Invalid inputs will be rejected with clear error messages.

## API Reference

This server wraps the Numbeo API endpoints. For detailed information about the data returned, see the [Numbeo API Documentation](https://www.numbeo.com/api/doc.jsp).

Key features:
- All SDK requests include the API key as a query parameter
- MCP server uses strict input validation with Pydantic
- No authentication headers required (Bearer token from client → SDK)
- Returns JSON data with comprehensive city/country statistics

## API Rate Limits

The Numbeo API may have rate limits depending on your subscription level. Refer to [Numbeo API documentation](https://www.numbeo.com/api/doc.jsp) for details.

## Troubleshooting

### "Numbeo API key is required" error

The API key must be provided by the MCP client through authorization headers or request metadata, not environment variables. Check your MCP client configuration.

### Connection timeout

Check your internet connection and verify that the Numbeo API is accessible.

### Invalid API response

Ensure your API key is valid and your subscription is active.

### Validation errors

The server uses strict Pydantic validation. Make sure all required fields are provided and enum values are correct (e.g., section must be one of: "cost-of-living", "crime", "health-care", "pollution", "traffic", "quality-of-life").

## License

See [LICENSE](LICENSE) file for details.
