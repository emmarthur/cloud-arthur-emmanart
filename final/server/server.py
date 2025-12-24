"""
MCP Server for Retail Project Analysis.

Model Context Protocol (MCP) Server Implementation:
This server follows the MCP standard protocol for LLMs to retrieve and invoke remote tools.
Rather than having every LLM agent implement all tools it needs, agents can invoke tools
implemented by this MCP server running remotely on Cloud Run.

Reference: Lab 8 - Model Context Protocol (MCP) - MCP servers allow agents to access
services without implementing tools themselves. Tool descriptions in docstrings are
utilized by the server to instruct clients on how to access tools. LLM agents are better
equipped to call MCP tools if these descriptions are detailed, specific, and accurate.

Exposes 5 API tools: BigQuery, REST Countries, Alpha Vantage, FRED, Fake Store.
Returns JSON data for client agents to analyze.
"""
from fastmcp import FastMCP
import sys
import os
from dotenv import load_dotenv

# Load environment variables (local: .env file, Cloud Run: env vars)
load_dotenv()

# Import tool implementations from separate modules
from tools.bigquery import bigquery_query
from tools.rest_countries import rest_countries
from tools.alpha_vantage import alpha_vantage
from tools.fred import fred
from tools.fake_store import fake_store

# Initialize MCP server using FastMCP (similar to lab8_reference.txt vulnerable_sqlite_mcp_server.py)
# FastMCP creates the server and allows tool registration via @mcp.tool() decorator
mcp = FastMCP("retail-analysis")

# Register MCP tools (wrappers around tool implementations)
# Note: Tool descriptions in docstrings are critical - they instruct LLM agents on how to use tools
# Reference: Lab 8 - "The description of the tool is provided within the comments of the tool
# declaration. This description is utilized by the server to instruct clients on how to access
# the tool. An LLM agent is better equipped to call MCP tools if these descriptions are detailed,
# specific, and accurate."
@mcp.tool()
def bigquery(query: str) -> str:
    """Execute BigQuery SQL query against bigquery-public-data datasets.
    
    Args:
        query: SQL query string (must query bigquery-public-data datasets)
    
    Returns:
        JSON string with query results
    """
    return bigquery_query(query)

@mcp.tool()
def rest_countries_api(country: str = "", region: str = "") -> str:
    """Retrieve country/region data from REST Countries API.
    
    Args:
        country: Optional country name (e.g., "United States"). Pass empty string "" if not needed.
        region: Optional region name (e.g., "Europe"). Pass empty string "" if not needed.
        Both parameters must be provided (use empty string "" if not needed).
    
    Returns:
        JSON string with country/region data
    """
    # Convert empty strings to None for the underlying function
    country_param = country if country and country.strip() else None
    region_param = region if region and region.strip() else None
    return rest_countries(country_param, region_param)

@mcp.tool()
def alpha_vantage_api(stock_symbol: str = None) -> str:
    """Retrieve financial market data from Alpha Vantage API.
    
    Args:
        stock_symbol: Optional stock symbol (e.g., 'AAPL', 'WMT'). None = general indicators.
    
    Returns:
        JSON string with financial data
    """
    return alpha_vantage(stock_symbol)

@mcp.tool()
def fred_api(series_id: str = None, industry: str = None) -> str:
    """Retrieve macroeconomic indicators from FRED API.
    
    Args:
        series_id: Optional FRED series ID (e.g., 'GDP', 'UNRATE'). None = general indicators.
        industry: Optional industry context (not used in API call)
    
    Returns:
        JSON string with economic data
    """
    return fred(series_id, industry)

@mcp.tool()
def fake_store_api(category: str = None) -> str:
    """Retrieve product data from Fake Store API.
    
    Args:
        category: Optional category (e.g., "electronics", "jewelery"). None = all products.
    
    Returns:
        JSON string with product data
    """
    return fake_store(category)

if __name__ == "__main__":
    # Support both STDIO (local testing) and HTTP (Cloud Run deployment)
    # Reference: Lab 8 - "There are two main ways of running an MCP server. One way is to run
    # the MCP server locally and communicate with it over standard input/output (STDIO) while
    # another is to run the MCP server remotely and communicate with it over HTTP."
    if len(sys.argv) > 1 and sys.argv[1] == 'stdio':
        # STDIO mode: for local testing, communicates over standard input/output
        mcp.run(transport="stdio")
    else:
        # HTTP mode: for Cloud Run deployment, communicates over HTTP
        # Cloud Run sets PORT env var, default 8080 for local dev
        # Reference: Lab 8 - "By default, CloudRun routes all incoming requests to port 80 and
        # 443 to port 8080 when a container is deployed unless specifically requested to do otherwise."
        port = int(os.environ.get('PORT', 8080))
        mcp.run(transport="http", host="0.0.0.0", port=port)
