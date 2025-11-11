# Numbeo API MCP Server - Usage Guide

## Quick Start

1. **Install the server:**
   ```bash
   pip install -e .
   ```

2. **Set your API key:**
   ```bash
   export NUMBEO_API_KEY="your-api-key-here"
   ```
   
   Or create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

3. **Start the server:**
   ```bash
   numbeo-mcp
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

## Using with MCP Clients

### Claude Desktop

1. Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "numbeo": {
      "command": "numbeo-mcp",
      "env": {
        "NUMBEO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. You can now ask Claude questions like:
   - "What is the cost of living in Tokyo?"
   - "Compare crime rates between New York and London"
   - "Show me the healthcare quality index for Berlin"

### Other MCP Clients

The server supports standard MCP protocol over stdio. Consult your MCP client's documentation for configuration.

## Direct API Usage

You can also use the Numbeo client directly in your Python code:

```python
from numbeo_mcp.client import NumberoAPIClient

# Initialize client
client = NumberoAPIClient(api_key="your-api-key")

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

## API Rate Limits

The Numbeo API may have rate limits depending on your subscription level. Refer to [Numbeo API documentation](https://www.numbeo.com/api/doc.jsp) for details.

## Troubleshooting

### "Numbeo API key is required" error

Make sure the `NUMBEO_API_KEY` environment variable is set:
```bash
export NUMBEO_API_KEY="your-key"
```

Or use a `.env` file in the project root.

### Connection timeout

Check your internet connection and verify that the Numbeo API is accessible.

### Invalid API response

Ensure your API key is valid and your subscription is active.

## Support

For issues specific to this MCP server implementation, please file an issue on GitHub.

For Numbeo API questions, refer to the [official documentation](https://www.numbeo.com/api/doc.jsp).
