"""
MCP Client: Connect to MCP server on Cloud Run via HTTP.

Model Context Protocol (MCP) Client Implementation:
This client adapts agent code to be an MCP client, leveraging MCP adapter support to invoke
tools on the remote MCP server. The client creates a connection to the MCP server and loads
the server's tools into agents, allowing agents to package MCP calls over HTTP and retrieve results.

Reference: Lab 8 - "To leverage the tool that the server now supports, we can adapt our prior
agent code to be an MCP client, leveraging LangChain's MCP adapter support to invoke the tool
on the server... the agent will package an MCP call over STDIO via the session's connection
and retrieve the results." (This implementation uses HTTP instead of STDIO for remote access)

Provides synchronous wrapper functions for CrewAI agents to call MCP server tools.
All agents have access to all tools.
"""
import asyncio
import time
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from typing import Optional
import os
from dotenv import load_dotenv
from metrics import track_mcp_call

load_dotenv()

# Cloud Run service URL (can be overridden via MCP_URL env var)
# Reference: Lab 8 - "set the MCP_URL environment variable to the URL that is returned by Cloud Run"
CLOUD_RUN_URL = os.getenv("MCP_URL", "https://final-325950842705.us-west1.run.app")
MCP_ENDPOINT = f"{CLOUD_RUN_URL}/mcp"


async def call_mcp_tool(tool_name: str, **kwargs) -> str:
    """Call MCP tool on deployed server via HTTP.
    
    Reference: Lab 8 - "To adapt the MCP client to utilize the remote MCP server, we simply
    tweak the client to utilize the Streamable HTTP interface to the MCP server's endpoint URL...
    keeping the rest of the client the same."
    
    Args:
        tool_name: MCP tool name (e.g., 'bigquery', 'rest_countries_api')
        **kwargs: Parameters to pass to the tool
        
    Returns:
        Tool result as JSON string
    """
    start_time = time.time()
    success = False
    error_message = None
    
    try:
        # Use streamablehttp_client for HTTP transport (Lab 8: streamablehttp_client pattern)
        # Creates connection to remote MCP server over HTTP
        async with streamablehttp_client(MCP_ENDPOINT) as (read, write, _):
            # Create ClientSession to manage MCP protocol communication
            # Reference: Lab 8 - "async with ClientSession(read, write) as session: await session.initialize()"
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Call tool via MCP protocol and extract text content from response
                # The session packages the MCP call over HTTP and retrieves results
                result = await session.call_tool(tool_name, kwargs)
                if result.content:
                    text_content = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                    success = True
                    return text_content
                else:
                    success = True
                    return str(result)
                    
    except Exception as e:
        error_message = str(e)
        return f"Error calling {tool_name}: {str(e)}"
    finally:
        # Track MCP call metrics
        response_time_ms = (time.time() - start_time) * 1000
        track_mcp_call(tool_name, response_time_ms, success, error_message)


def call_mcp_tool_sync(tool_name: str, **kwargs) -> str:
    """Synchronous wrapper for call_mcp_tool (CrewAI tools must be synchronous).
    
    Converts async MCP tool calls to synchronous calls using asyncio.run().
    This is necessary because CrewAI tool functions must be synchronous, while
    MCP client operations are asynchronous.
    
    Args:
        tool_name: MCP tool name
        **kwargs: Parameters to pass to the tool
        
    Returns:
        Tool result as JSON string
    """
    return asyncio.run(call_mcp_tool(tool_name, **kwargs))


# Tool functions for each MCP server tool (all agents can use any tool)

def bigquery_tool(query: str) -> str:
    """Execute BigQuery SQL query against BigQuery Public Datasets."""
    return call_mcp_tool_sync("bigquery", query=query)


def rest_countries_tool(country: Optional[str] = None, region: Optional[str] = None) -> str:
    """Retrieve country/region data from REST Countries API."""
    # Always pass both parameters explicitly as empty strings if None
    # FastMCP/Pydantic requires all parameters to be present in the MCP protocol message
    # Empty strings are valid values that satisfy Pydantic validation
    params = {
        "country": country if country is not None and country != "" else "",
        "region": region if region is not None and region != "" else ""
    }
    return call_mcp_tool_sync("rest_countries_api", **params)


def alpha_vantage_tool(stock_symbol: Optional[str] = None) -> str:
    """Retrieve financial market data from Alpha Vantage API."""
    params = {}
    if stock_symbol and stock_symbol.strip():
        params["stock_symbol"] = stock_symbol
    return call_mcp_tool_sync("alpha_vantage_api", **params)


def fred_tool(series_id: Optional[str] = None, industry: Optional[str] = None) -> str:
    """Retrieve macroeconomic indicators from FRED API."""
    params = {}
    if series_id:
        params["series_id"] = series_id
    if industry:
        params["industry"] = industry
    return call_mcp_tool_sync("fred_api", **params)


def fake_store_tool(category: Optional[str] = None) -> str:
    """Retrieve product data from Fake Store API."""
    params = {}
    if category:
        params["category"] = category
    return call_mcp_tool_sync("fake_store_api", **params)
