"""
Metrics Tracking Module for MCP Server.

Tracks API calls, response times, success/failure rates, and other performance metrics.
Metrics are logged to files and can be exported for analysis.
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import threading

# Thread-safe metrics storage
_metrics_lock = threading.Lock()
_metrics = {
    "api_calls": [],  # List of API call records
    "tool_calls": defaultdict(int),  # Tool name -> call count
    "api_call_counts": defaultdict(int),  # API name -> call count
    "errors": [],  # List of error records
    "response_times": defaultdict(list),  # API name -> list of response times
    "start_time": datetime.now().isoformat(),
    "total_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0
}

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
METRICS_LOG_FILE = os.path.join(LOG_DIR, "server_metrics.log")
METRICS_JSON_FILE = os.path.join(LOG_DIR, "server_metrics.json")


def _log_metric(message: str):
    """Log metric message to file and stdout."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Write to file
        try:
            with open(METRICS_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{log_entry}\n")
        except Exception:
            pass  # Continue if file write fails
        
        # Print to stdout for Cloud Run logging
        print(log_entry, flush=True)
    except Exception:
        pass


def track_api_call(
    api_name: str,
    tool_name: str,
    success: bool,
    response_time_ms: float,
    error_message: Optional[str] = None,
    parameters: Optional[Dict] = None
):
    """Track an API call with metrics.
    
    Args:
        api_name: Name of the external API (e.g., 'Alpha Vantage', 'FRED', 'REST Countries')
        tool_name: Name of the MCP tool (e.g., 'alpha_vantage_api', 'fred_api')
        success: Whether the API call was successful
        response_time_ms: Response time in milliseconds
        error_message: Error message if call failed
        parameters: Parameters used in the API call
    """
    with _metrics_lock:
        timestamp = datetime.now().isoformat()
        
        # Record API call
        call_record = {
            "timestamp": timestamp,
            "api_name": api_name,
            "tool_name": tool_name,
            "success": success,
            "response_time_ms": round(response_time_ms, 2),
            "parameters": parameters or {}
        }
        
        if error_message:
            call_record["error_message"] = error_message
        
        _metrics["api_calls"].append(call_record)
        
        # Update counters
        _metrics["total_calls"] += 1
        _metrics["tool_calls"][tool_name] += 1
        _metrics["api_call_counts"][api_name] += 1
        
        if success:
            _metrics["successful_calls"] += 1
            _metrics["response_times"][api_name].append(response_time_ms)
        else:
            _metrics["failed_calls"] += 1
            _metrics["errors"].append({
                "timestamp": timestamp,
                "api_name": api_name,
                "tool_name": tool_name,
                "error_message": error_message or "Unknown error",
                "parameters": parameters or {}
            })
        
        # Log metric
        status = "SUCCESS" if success else "FAILED"
        _log_metric(f"API Call: {api_name} via {tool_name} - {status} ({response_time_ms:.2f}ms)")
        
        # Periodically save metrics to JSON file
        if _metrics["total_calls"] % 10 == 0:
            save_metrics_to_file()


def track_tool_call(tool_name: str, parameters: Optional[Dict] = None):
    """Track an MCP tool call (before API call).
    
    Args:
        tool_name: Name of the MCP tool
        parameters: Parameters passed to the tool
    """
    with _metrics_lock:
        timestamp = datetime.now().isoformat()
        _log_metric(f"Tool Call: {tool_name} with params: {json.dumps(parameters or {})}")


def get_metrics_summary() -> Dict:
    """Get summary of all metrics.
    
    Returns:
        Dictionary with metrics summary
    """
    with _metrics_lock:
        # Calculate average response times
        avg_response_times = {}
        for api_name, times in _metrics["response_times"].items():
            if times:
                avg_response_times[api_name] = {
                    "avg_ms": round(sum(times) / len(times), 2),
                    "min_ms": round(min(times), 2),
                    "max_ms": round(max(times), 2),
                    "count": len(times)
                }
        
        # Calculate success rate
        success_rate = 0.0
        if _metrics["total_calls"] > 0:
            success_rate = (_metrics["successful_calls"] / _metrics["total_calls"]) * 100
        
        return {
            "summary": {
                "start_time": _metrics["start_time"],
                "current_time": datetime.now().isoformat(),
                "total_api_calls": _metrics["total_calls"],
                "successful_calls": _metrics["successful_calls"],
                "failed_calls": _metrics["failed_calls"],
                "success_rate_percent": round(success_rate, 2)
            },
            "tool_usage": dict(_metrics["tool_calls"]),
            "api_usage": dict(_metrics["api_call_counts"]),
            "average_response_times": avg_response_times,
            "errors": _metrics["errors"][-50:],  # Last 50 errors
            "detailed_calls": _metrics["api_calls"][-100:]  # Last 100 calls
        }


def get_all_metrics() -> Dict:
    """Get all metrics data.
    
    Returns:
        Complete metrics dictionary
    """
    with _metrics_lock:
        return {
            "start_time": _metrics["start_time"],
            "current_time": datetime.now().isoformat(),
            "total_calls": _metrics["total_calls"],
            "successful_calls": _metrics["successful_calls"],
            "failed_calls": _metrics["failed_calls"],
            "tool_calls": dict(_metrics["tool_calls"]),
            "api_call_counts": dict(_metrics["api_call_counts"]),
            "api_calls": _metrics["api_calls"],
            "errors": _metrics["errors"],
            "response_times": {k: v for k, v in _metrics["response_times"].items()}
        }


def save_metrics_to_file():
    """Save current metrics to JSON file."""
    try:
        metrics_data = get_all_metrics()
        with open(METRICS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=2)
    except Exception as e:
        _log_metric(f"Error saving metrics to file: {e}")


def reset_metrics():
    """Reset all metrics (useful for testing)."""
    global _metrics
    with _metrics_lock:
        _metrics = {
            "api_calls": [],
            "tool_calls": defaultdict(int),
            "api_call_counts": defaultdict(int),
            "errors": [],
            "response_times": defaultdict(list),
            "start_time": datetime.now().isoformat(),
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0
        }
        _log_metric("Metrics reset")

