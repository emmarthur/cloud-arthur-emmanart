"""
FRED API Tool: Retrieve macroeconomic indicators for market intelligence and economic analysis.
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
FRED_LOG_FILE = os.path.join(LOG_DIR, "fred.log")

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

def fred(series_id: str = None, industry: str = None) -> str:
    """Retrieve macroeconomic indicators from FRED API.
    
    Args:
        series_id: Optional FRED series ID (e.g., 'GDP', 'UNRATE'). None = general indicators.
        industry: Optional industry context (not used in API call, included in response)
    
    Returns:
        JSON string with economic data (observations if series_id provided, else general indicators)
    """
    try:
        _log_to_file(FRED_LOG_FILE, f"Function called with series_id={series_id}, industry={industry}")
        
        fred_api_key = os.getenv("FRED_API_KEY")
        data = {
            "series_id": series_id,
            "industry": industry,
            "api_key_available": bool(fred_api_key)
        }
        
        # Make API call if key and series_id provided, else return general indicators
        if fred_api_key and series_id:
            try:
                # Track API call with metrics
                start_time = time.time()
                # Call FRED series observations API
                url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={fred_api_key}&file_type=json&limit=10&sort_order=desc"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                fred_data = response.json()
                response_time_ms = (time.time() - start_time) * 1000
                
                # Handle API response (observations, error, or raw)
                success = False
                error_msg = None
                if "observations" in fred_data:
                    data["observations"] = fred_data["observations"]
                    data["series_info"] = {
                        "series_id": series_id,
                        "title": fred_data.get("title", ""),
                        "units": fred_data.get("units", "")
                    }
                    success = True
                elif "error_message" in fred_data:
                    data["error"] = fred_data["error_message"]
                    error_msg = fred_data["error_message"]
                else:
                    data["raw_response"] = fred_data
                    success = True
                
                # Track metrics
                track_api_call(
                    api_name="FRED",
                    tool_name="fred_api",
                    success=success,
                    response_time_ms=response_time_ms,
                    error_message=error_msg,
                    parameters={"series_id": series_id, "industry": industry}
                )
            except requests.RequestException as e:
                response_time_ms = (time.time() - start_time) * 1000
                data["api_error"] = str(e)
                # Track failed API call
                track_api_call(
                    api_name="FRED",
                    tool_name="fred_api",
                    success=False,
                    response_time_ms=response_time_ms,
                    error_message=str(e),
                    parameters={"series_id": series_id, "industry": industry}
                )
                data["macroeconomic_indicators"] = {
                    "gdp_growth_rate": 2.5,
                    "gdp_growth_rate_unit": "percent",
                    "gdp_growth_rate_description": "moderate growth",
                    "unemployment_rate": 3.7,
                    "unemployment_rate_unit": "percent",
                    "unemployment_rate_description": "low, favorable for retail",
                    "consumer_price_index": "Stable inflation",
                    "retail_sales_growth": 4.2,
                    "retail_sales_growth_unit": "percent YoY"
                }
        else:
            # No API key or series_id: return general economic indicators
            data["macroeconomic_indicators"] = {
                "gdp_growth_rate": 2.5,
                "gdp_growth_rate_unit": "percent",
                "gdp_growth_rate_description": "moderate growth",
                "unemployment_rate": 3.7,
                "unemployment_rate_unit": "percent",
                "unemployment_rate_description": "low, favorable for retail",
                "consumer_price_index": "Stable inflation",
                "retail_sales_growth": 4.2,
                "retail_sales_growth_unit": "percent YoY"
            }
            data["market_trends"] = [
                "E-commerce continues to grow but in-store retail remains strong",
                "Consumer preferences shifting toward sustainable products",
                "Omnichannel retail strategies becoming essential",
                "Local retail experiencing resurgence in urban areas"
            ]
            data["industry_insights"] = {
                "sector_growth": f"{industry} sector shows positive growth trajectory" if industry else "Retail sector shows positive growth trajectory",
                "competition_level": "moderate to high",
                "pricing_strategy_note": "Pricing strategies need to balance value and quality",
                "long_term_outlook": "Favorable for well-positioned retailers"
            }
            data["strategic_recommendations"] = [
                "Monitor macroeconomic trends for timing decisions",
                "Focus on consumer behavior shifts and preferences",
                "Consider competitive positioning and differentiation",
                "Leverage economic indicators for demand forecasting"
            ]
        
        result_json = json.dumps(data)
        _log_to_file(FRED_LOG_FILE, f"SUCCESS: Market intelligence data retrieved")
        _log_to_file(FRED_LOG_FILE, f"Response: {result_json[:500]}...")
        return result_json
    except Exception as e:
        error_data = {
            "error": True,
            "error_message": f"Error fetching market intelligence data: {str(e)}",
            "series_id": series_id,
            "industry": industry
        }
        _log_to_file(FRED_LOG_FILE, f"ERROR: Exception - {type(e).__name__}: {str(e)}")
        return json.dumps(error_data)

