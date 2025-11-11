# Numbeo API MCP Server 🌍

FastMCP server wrapping the [Numbeo API](https://www.numbeo.com/api/doc.jsp), providing data on cost of living, property prices, and crime rates worldwide.

## Features

- 🏙️ **Cost of Living Data**: Get current and historical prices for cities and countries
- 🏠 **Property Prices**: Access real estate market data
- 🚨 **Crime Statistics**: Retrieve safety and crime indices
- 📊 **City Indices**: Compare quality of life, healthcare, traffic, and pollution metrics
- 🏆 **Rankings**: Global and country-specific city rankings
- 🔐 **Secure API Access**: Uses API key as query parameter (as per Numbeo API specification)

## Getting Started

### Prerequisites

- Python 3.12 or higher
- A Numbeo API key (obtain from [Numbeo API](https://www.numbeo.com/api/))

### Installation

To set up and run:

```bash
pip install -e .
```

Or using uv:

```bash
uv sync
```

### Configuration

Set your Numbeo API key as an environment variable:

```bash
export NUMBEO_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```
NUMBEO_API_KEY=your-api-key-here
```

### Running the Server

Start the MCP server:

```bash
numbeo-mcp
```

The server will start and expose the following MCP tools:

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

### Example Usage

```python
# Using the MCP tools through your MCP client
# Example: Get cost of living for New York
result = get_city_cost_of_living(city="New York", country="United States")

# Get crime statistics for London
crime_data = get_city_crime_statistics(city="London", country="United Kingdom")

# Get global cost of living rankings
rankings = get_city_rankings(section="cost-of-living")
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

## API Reference

This server wraps the Numbeo API endpoints. For detailed information about the data returned, see the [Numbeo API Documentation](https://www.numbeo.com/api/doc.jsp).

Key API features:
- All requests include the API key as a query parameter
- No authentication headers required
- Returns JSON data with comprehensive city/country statistics

## License

See [LICENSE](LICENSE) file for details.
