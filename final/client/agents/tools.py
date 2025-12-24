"""
Shared tool wrappers for all CrewAI agents.

Tool Descriptions for LLM Agents:
These tool wrappers provide CrewAI agents with access to MCP server tools. The docstrings
are critical for agent understanding - they must be detailed, specific, and accurate so that
LLM agents can intelligently determine when and how to use each tool.

Reference: Lab 8 - "The description of the tool is provided within the comments of the tool
declaration. This description is utilized by the server to instruct clients on how to access
the tool. An LLM agent is better equipped to call MCP tools if these descriptions are detailed,
specific, and accurate."

All agents have access to all tools and can use them based on their analysis needs.
Includes logging for tool calls, inputs, outputs, and errors.
"""
from crewai.tools import tool
import sys
import json
import os
from datetime import datetime
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from mcp_client import (
    bigquery_tool, rest_countries_tool, alpha_vantage_tool, 
    fred_tool, fake_store_tool
)

# Logging setup: create logs directory and define log file paths
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths - tool-specific
BIGQUERY_LOG_FILE = os.path.join(LOG_DIR, "bigquery.log")
REST_COUNTRIES_LOG_FILE = os.path.join(LOG_DIR, "rest_countries.log")
ALPHA_VANTAGE_LOG_FILE = os.path.join(LOG_DIR, "alpha_vantage.log")
FRED_LOG_FILE = os.path.join(LOG_DIR, "fred.log")
FAKE_STORE_LOG_FILE = os.path.join(LOG_DIR, "fake_store.log")

# Log file paths - agent-specific
OPERATIONS_AGENT_LOG_FILE = os.path.join(LOG_DIR, "operations_agent.log")
CUSTOMER_ANALYTICS_AGENT_LOG_FILE = os.path.join(LOG_DIR, "customer_analytics_agent.log")
FINANCIAL_AGENT_LOG_FILE = os.path.join(LOG_DIR, "financial_agent.log")
MARKET_INTELLIGENCE_AGENT_LOG_FILE = os.path.join(LOG_DIR, "market_intelligence_agent.log")
PRODUCT_ECOMMERCE_AGENT_LOG_FILE = os.path.join(LOG_DIR, "product_ecommerce_agent.log")

# Global context for project name (set by client.py)
_current_project_name = "Unknown Project"

def set_project_name(project_name: str):
    """Set current project name for logging (called by client.py)."""
    global _current_project_name
    _current_project_name = project_name

# Enable console logging of tool data (set to False to disable)
SHOW_TOOL_DATA = True

def _log_to_file(log_file: str, message: str):
    """Log message to file with timestamp."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{log_entry}\n")
    except Exception as e:
        print(f"Error writing to log file {log_file}: {e}")

def _get_agent_log_file(agent_name: str) -> str:
    """Get log file path for a specific agent based on role name."""
    agent_name_lower = agent_name.lower()
    # Match agent role names to their log files
    if "operations" in agent_name_lower or "supply chain" in agent_name_lower:
        return OPERATIONS_AGENT_LOG_FILE
    elif "customer" in agent_name_lower or "marketing" in agent_name_lower:
        return CUSTOMER_ANALYTICS_AGENT_LOG_FILE
    elif "financial" in agent_name_lower or "sales" in agent_name_lower:
        return FINANCIAL_AGENT_LOG_FILE
    elif "market" in agent_name_lower or "intelligence" in agent_name_lower or "research" in agent_name_lower:
        return MARKET_INTELLIGENCE_AGENT_LOG_FILE
    elif "product" in agent_name_lower or "ecommerce" in agent_name_lower or "e-commerce" in agent_name_lower:
        return PRODUCT_ECOMMERCE_AGENT_LOG_FILE
    else:
        # Default fallback
        return OPERATIONS_AGENT_LOG_FILE

def _log_tool_data(tool_name: str, input_data: dict, output_data: str, log_file: str, agent_name: str = "Unknown Agent"):
    """Log tool input/output data to tool-specific and agent-specific log files, and console if enabled."""
    global _current_project_name
    
    # Log to tool-specific file
    try:
        _log_to_file(log_file, f"Input: {json.dumps(input_data, indent=2)}")
        
        # Parse and log JSON output (handle errors gracefully)
        try:
            output_json = json.loads(output_data)
            if isinstance(output_json, dict) and output_json.get("error"):
                _log_to_file(log_file, f"ERROR: {output_json.get('error_message', 'Unknown error')}")
            else:
                _log_to_file(log_file, f"SUCCESS: Response received")
            _log_to_file(log_file, f"Output: {json.dumps(output_json, indent=2)[:2000]}...")  # Limit size
        except:
            _log_to_file(log_file, f"Output (raw): {output_data[:1000]}...")  # Limit size
        
        _log_to_file(log_file, "-" * 80)
    except Exception as e:
        _log_to_file(log_file, f"Error logging tool data: {e}")
    
    # Log to agent-specific file
    try:
        agent_log_file = _get_agent_log_file(agent_name)
        _log_to_file(agent_log_file, f"Project: {_current_project_name}")
        _log_to_file(agent_log_file, f"Tool Called: {tool_name}")
        _log_to_file(agent_log_file, f"Input: {json.dumps(input_data, indent=2)}")
        
        # Parse and log JSON output
        try:
            output_json = json.loads(output_data)
            if isinstance(output_json, dict) and output_json.get("error"):
                _log_to_file(agent_log_file, f"ERROR: {output_json.get('error_message', 'Unknown error')}")
            else:
                _log_to_file(agent_log_file, f"SUCCESS: Response received")
        except:
            _log_to_file(agent_log_file, f"Response received (non-JSON)")
        
        _log_to_file(agent_log_file, "-" * 80)
    except Exception as e:
        print(f"Error logging to agent file: {e}")
    
    # Print to console if enabled (for debugging)
    if SHOW_TOOL_DATA:
        print(f"\n{'='*80}")
        print(f"[TOOL DATA] {tool_name}")
        print(f"{'='*80}")
        print(f"Input: {json.dumps(input_data, indent=2)}")
        try:
            output_json = json.loads(output_data)
            print(f"Output (JSON): {json.dumps(output_json, indent=2)[:2000]}...")  # Limit size
        except:
            print(f"Output (raw): {output_data[:1000]}...")  # Limit size
        print(f"{'='*80}\n")

@tool("BigQuery Tool")
def bigquery_tool_wrapper(query: str, agent_name: str = "Unknown Agent") -> str:
    """Execute BigQuery SQL query against bigquery-public-data datasets.
    
    This tool wrapper provides CrewAI agents access to the MCP server's BigQuery tool.
    The detailed description below helps LLM agents understand when and how to use this tool.
    
    Reference: Lab 8 - Tool descriptions must be "detailed, specific, and accurate" for
    LLM agents to effectively call MCP tools. This docstring serves that purpose.
    
    CRITICAL: Call ONCE at a time. Do NOT batch multiple tool calls.
    
    INPUT: SQL query string (REQUIRED). Must query bigquery-public-data datasets.
    
    AVAILABLE TABLE: bigquery-public-data.census_bureau_international.midyear_population
    Columns: country_name, country_code, year, midyear_population
    
    IMPORTANT: 
    - Use country_name with LIKE patterns (e.g., LOWER(country_name) LIKE '%united kingdom%')
    - Table uses non-standard country codes ('UK' not 'GB')
    - Only use 'midyear_population' table (others don't exist)
    
    Example: SELECT country_name, midyear_population FROM `bigquery-public-data.census_bureau_international.midyear_population` WHERE year = 2020 AND LOWER(country_name) LIKE '%united kingdom%'
    
    Args:
        query: BigQuery SQL query string (REQUIRED)
        agent_name: Your role name for logging
    
    Returns:
        JSON string with query results
    """
    result = bigquery_tool(query)
    _log_tool_data("BigQuery Tool", {"query": query[:200] + "..." if len(query) > 200 else query}, result, BIGQUERY_LOG_FILE, agent_name)
    return result

# Track tool call attempts to prevent infinite recursion
_rest_countries_call_count = {}

@tool("REST Countries Tool")
def rest_countries_tool_wrapper(country: str = "", region: str = "", agent_name: str = "Unknown Agent") -> str:
    """Retrieve country/region data from REST Countries API.
    
    CRITICAL: Call ONCE at a time. Do NOT batch multiple tool calls.
    
    INPUT: String parameters (country name or region name, both optional).
    - country: Country name (e.g., "United States", "France"). Pass "" if not needed.
    - region: Region name (e.g., "Europe", "Americas"). Pass "" if not needed.
    - Leave both empty to get all countries.
    
    IMPORTANT: You MUST always provide BOTH parameters when calling this tool:
    - If you only need country: country="United States", region=""
    - If you only need region: country="", region="Europe"
    - If you need all countries: country="", region=""
    
    Use for supply chain network analysis, regional distribution, logistics planning.
    
    Args:
        country: Country name string ("" if not needed, but MUST be provided)
        region: Region name string ("" if not needed, but MUST be provided)
        agent_name: Your role name for logging
    
    Returns:
        JSON string with country/region data
    """
    # Prevent infinite recursion: limit retry attempts
    call_key = f"{agent_name}_{country}_{region}"
    if call_key not in _rest_countries_call_count:
        _rest_countries_call_count[call_key] = 0
    _rest_countries_call_count[call_key] += 1
    
    if _rest_countries_call_count[call_key] > 3:
        error_response = {
            "error": True,
            "error_message": "Tool call limit exceeded. Please check your parameters and try a different approach.",
            "note": "Both 'country' and 'region' parameters must be explicitly provided (use empty string '' if not needed)"
        }
        import json
        return json.dumps(error_response)
    
    # Ensure both parameters are always provided (even if empty) to avoid Pydantic validation errors
    # Convert empty strings to None for the underlying tool, but ensure both are passed
    country_param = country if country and country.strip() else None
    region_param = region if region and region.strip() else None
    
    try:
        # Always pass both parameters explicitly to prevent Pydantic validation errors
        result = rest_countries_tool(country_param, region_param)
        
        # Check if result contains a validation error and provide helpful message
        # This prevents infinite retry loops by giving clear error messages
        try:
            import json
            result_str = str(result)
            # Check for validation errors in the result (could be JSON or plain text)
            if "validation error" in result_str.lower() or "field required" in result_str.lower() or "missing" in result_str.lower():
                try:
                    result_dict = json.loads(result)
                    if isinstance(result_dict, dict) and ("error" in result_dict or "error_message" in result_dict):
                        # Return a clear error that tells the agent what went wrong and how to fix it
                        error_response = {
                            "error": True,
                            "error_message": "Tool validation failed. Both 'country' and 'region' parameters must be provided (use empty string '' if not needed).",
                            "suggestion": "When calling this tool, always provide both parameters: country='United States', region='' (or both as empty strings if querying all countries)",
                            "original_error": result_dict.get("error_message", str(result_dict))
                        }
                        result = json.dumps(error_response)
                except:
                    # If result is not JSON but contains error keywords, create error response
                    error_response = {
                        "error": True,
                        "error_message": f"Tool validation failed: {result_str[:200]}",
                        "suggestion": "When calling REST Countries Tool, always provide both 'country' and 'region' parameters (use empty string '' if not needed)"
                    }
                    result = json.dumps(error_response)
        except:
            pass  # If error detection fails, continue with original result
        
        _log_tool_data("REST Countries Tool", {"country": country, "region": region}, result, REST_COUNTRIES_LOG_FILE, agent_name)
        return result
    except Exception as e:
        # Catch any unexpected errors and return a clear error message
        error_response = {
            "error": True,
            "error_message": f"Error calling REST Countries Tool: {str(e)}",
            "note": "Ensure both 'country' and 'region' parameters are provided (use empty string '' if not needed)"
        }
        import json
        error_result = json.dumps(error_response)
        _log_tool_data("REST Countries Tool", {"country": country, "region": region}, error_result, REST_COUNTRIES_LOG_FILE, agent_name)
        return error_result

@tool("Alpha Vantage Tool")
def alpha_vantage_tool_wrapper(stock_symbol: str = "", agent_name: str = "Unknown Agent") -> str:
    """Retrieve financial market data from Alpha Vantage API.
    
    CRITICAL: Call ONCE at a time. Do NOT batch multiple tool calls.
    
    INPUT: Stock symbol string (optional). Pass "" for general market indicators.
    
    STOCK SYMBOL SELECTION (choose based on project type):
    - General retail/grocery: 'WMT', 'TGT', 'COST'
    - E-commerce: 'AMZN'
    - Home improvement: 'HD', 'LOW'
    - Fashion/apparel: 'NKE', 'LULU'
    - Electronics: 'AAPL', 'BBY'
    - General market conditions: "" (empty string)
    
    Use for: Market conditions, financial analysis, consumer confidence, market trends.
    
    Args:
        stock_symbol: Stock symbol (e.g., 'WMT', 'AMZN', 'HD') or "" for general indicators
        agent_name: Your role name for logging
    
    Returns:
        JSON string with financial data
    """
    symbol_param = stock_symbol if stock_symbol and stock_symbol.strip() else None
    result = alpha_vantage_tool(symbol_param)
    _log_tool_data("Alpha Vantage Tool", {"stock_symbol": stock_symbol}, result, ALPHA_VANTAGE_LOG_FILE, agent_name)
    return result

@tool("FRED Tool")
def fred_tool_wrapper(series_id: str = "", industry: str = "", agent_name: str = "Unknown Agent") -> str:
    """Retrieve macroeconomic indicators from FRED API.
    
    CRITICAL: Call ONCE at a time. Do NOT batch multiple tool calls.
    
    INPUT: FRED series ID string (optional), industry context string (optional).
    
    Common series IDs: 'GDP', 'UNRATE', 'CPIAUCSL', 'RETAIL_SALES', 'PCE'
    - Provide series_id for specific data, "" for general indicators
    - Industry is context only (doesn't affect API call)
    
    Use for: Macroeconomic analysis, market intelligence, economic forecasting.
    
    Args:
        series_id: FRED series ID (e.g., 'GDP', 'UNRATE') or "" for general indicators
        industry: Industry context (e.g., 'Retail') or "" if not needed
        agent_name: Your role name for logging
    
    Returns:
        JSON string with economic data
    """
    series_param = series_id if series_id and series_id.strip() else None
    industry_param = industry if industry and industry.strip() else None
    result = fred_tool(series_param, industry_param)
    _log_tool_data("FRED Tool", {"series_id": series_id, "industry": industry}, result, FRED_LOG_FILE, agent_name)
    return result

@tool("Fake Store Tool")
def fake_store_tool_wrapper(category: str = "", agent_name: str = "Unknown Agent") -> str:
    """Retrieve product data from Fake Store API.
    
    CRITICAL: Call ONCE at a time. Do NOT batch multiple tool calls.
    
    INPUT: Product category string (optional). Pass "" for all products.
    
    Valid categories: "electronics", "jewelery", "men's clothing", "women's clothing"
    
    Use for: Product assortment analysis, pricing strategies, e-commerce metrics.
    
    Args:
        category: Product category (e.g., "electronics", "jewelery") or "" for all products
        agent_name: Your role name for logging
    
    Returns:
        JSON string with product data
    """
    category_param = category if category and category.strip() else None
    result = fake_store_tool(category_param)
    _log_tool_data("Fake Store Tool", {"category": category}, result, FAKE_STORE_LOG_FILE, agent_name)
    return result

# Export all tools as a list for easy import
ALL_TOOLS = [
    bigquery_tool_wrapper,
    rest_countries_tool_wrapper,
    alpha_vantage_tool_wrapper,
    fred_tool_wrapper,
    fake_store_tool_wrapper
]
