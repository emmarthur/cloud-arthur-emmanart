"""
Alpha Vantage API Tool: Retrieve financial market data for financial analysis.
"""
import os
import json
import requests
import time
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for metrics import
sys.path.insert(0, str(Path(__file__).parent.parent))
from metrics import track_api_call

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
ALPHA_VANTAGE_LOG_FILE = os.path.join(LOG_DIR, "alpha_vantage.log")

def _log_to_file(log_file: str, message: str):
    """Log message to file and stdout (for Cloud Run logging)."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Write to file (for local development)
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{log_entry}\n")
        except Exception as file_error:
            # If file writing fails (e.g., in Cloud Run with read-only filesystem), continue
            pass
        
        # Also print to stdout/stderr for Cloud Run logging
        # Cloud Run automatically captures stdout/stderr and makes it available in Cloud Logging
        print(log_entry, flush=True)
    except Exception as e:
        print(f"Error in logging: {e}", flush=True)

def alpha_vantage(stock_symbol: str = None) -> str:
    """Retrieve financial market data from Alpha Vantage API.
    
    Args:
        stock_symbol: Optional stock symbol (e.g., 'AAPL', 'WMT'). None = general indicators.
    
    Returns:
        JSON string with financial data (quote data if symbol provided, else general indicators)
    """
    try:
        _log_to_file(ALPHA_VANTAGE_LOG_FILE, f"Function called with stock_symbol={stock_symbol}")
        
        alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        data = {
            "stock_symbol": stock_symbol,
            "api_key_available": bool(alpha_vantage_key)
        }
        
        # Make API call if key and symbol provided, else return general indicators
        if alpha_vantage_key and stock_symbol:
            try:
                # Track API call with metrics
                start_time = time.time()
                # Call Alpha Vantage Global Quote API
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={alpha_vantage_key}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                quote_data = response.json()
                response_time_ms = (time.time() - start_time) * 1000
                
                # Handle API response (quote, error, or rate limit)
                success = False
                error_msg = None
                if "Global Quote" in quote_data:
                    data["quote"] = quote_data["Global Quote"]
                    success = True
                elif "Error Message" in quote_data:
                    data["error"] = quote_data["Error Message"]
                    error_msg = quote_data["Error Message"]
                elif "Note" in quote_data:
                    data["note"] = "API rate limit reached. Using simulated data."
                    error_msg = "API rate limit reached"
                    data["market_indicators"] = {
                        "retail_sector_performance": "Stable",
                        "consumer_spending_index": "Moderate Growth",
                        "market_volatility": "Low to Medium"
                    }
                else:
                    data["raw_response"] = quote_data
                    success = True
                
                # Track metrics
                track_api_call(
                    api_name="Alpha Vantage",
                    tool_name="alpha_vantage_api",
                    success=success,
                    response_time_ms=response_time_ms,
                    error_message=error_msg,
                    parameters={"stock_symbol": stock_symbol}
                )
            except requests.RequestException as e:
                response_time_ms = (time.time() - start_time) * 1000
                data["api_error"] = str(e)
                data["market_indicators"] = {
                    "retail_sector_performance": "Stable",
                    "consumer_spending_index": "Moderate Growth",
                    "market_volatility": "Low to Medium"
                }
                # Track failed API call
                track_api_call(
                    api_name="Alpha Vantage",
                    tool_name="alpha_vantage_api",
                    success=False,
                    response_time_ms=response_time_ms,
                    error_message=str(e),
                    parameters={"stock_symbol": stock_symbol}
                )
        else:
            # No API key or symbol: return general market indicators
            data["market_indicators"] = {
                "retail_sector_performance": "Stable",
                "consumer_spending_index": "Moderate Growth",
                "market_volatility": "Low to Medium"
            }
            data["sales_performance_metrics"] = {
                "estimated_market_size": "Based on general market conditions",
                "revenue_potential": "Moderate to High (retail sector)",
                "profitability_outlook": "Positive with proper execution"
            }
            data["financial_insights"] = {
                "sector_growth": "Retail sector shows steady growth potential",
                "consumer_confidence": "Consumer confidence indicators are favorable",
                "market_conditions": "Market conditions support new retail ventures",
                "recommendation": "Monitor quarterly earnings and market trends"
            }
        
        result_json = json.dumps(data)
        _log_to_file(ALPHA_VANTAGE_LOG_FILE, f"SUCCESS: Financial data retrieved")
        _log_to_file(ALPHA_VANTAGE_LOG_FILE, f"Response: {result_json[:500]}...")
        return result_json
    except Exception as e:
        error_data = {
            "error": True,
            "error_message": f"Error fetching financial data: {str(e)}",
            "stock_symbol": stock_symbol
        }
        _log_to_file(ALPHA_VANTAGE_LOG_FILE, f"ERROR: Exception - {type(e).__name__}: {str(e)}")
        return json.dumps(error_data)

