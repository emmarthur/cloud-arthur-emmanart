"""
Metrics Tracking Module for Client.

Tracks tool usage, agent activity, analysis sessions, and performance metrics.
Metrics are logged to files and can be exported for analysis.
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

# Metrics storage
_metrics = {
    "analysis_sessions": [],  # List of analysis session records
    "tool_calls": [],  # List of tool call records
    "agent_activity": defaultdict(list),  # Agent name -> list of activities
    "tool_usage": defaultdict(int),  # Tool name -> call count
    "mcp_calls": [],  # List of MCP server calls
    "start_time": datetime.now().isoformat(),
    "total_tool_calls": 0,
    "total_analyses": 0,
    "total_mcp_calls": 0,
    "successful_tool_calls": 0,
    "failed_tool_calls": 0,
    "mcp_response_times": []  # List of MCP response times
}

# Logging setup
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
METRICS_LOG_FILE = os.path.join(LOG_DIR, "client_metrics.log")
METRICS_JSON_FILE = os.path.join(LOG_DIR, "client_metrics.json")


def _log_metric(message: str):
    """Log metric message to file."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        with open(METRICS_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{log_entry}\n")
    except Exception:
        pass  # Continue if logging fails


def start_analysis_session(project_description: str) -> str:
    """Start tracking a new analysis session.
    
    Args:
        project_description: Description of the project being analyzed
        
    Returns:
        Session ID for tracking
    """
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    timestamp = datetime.now().isoformat()
    
    session_record = {
        "session_id": session_id,
        "timestamp": timestamp,
        "project_description": project_description[:200] + "..." if len(project_description) > 200 else project_description,
        "status": "started",
        "tool_calls": [],
        "agents_used": [],
        "duration_seconds": None
    }
    
    _metrics["analysis_sessions"].append(session_record)
    _metrics["total_analyses"] += 1
    
    _log_metric(f"Analysis session started: {session_id}")
    return session_id


def end_analysis_session(session_id: str, success: bool = True):
    """End an analysis session and record duration.
    
    Args:
        session_id: Session ID to end
        success: Whether the analysis completed successfully
    """
    # Find the session
    session = None
    for s in _metrics["analysis_sessions"]:
        if s["session_id"] == session_id:
            session = s
            break
    
    if session:
        start_time = datetime.fromisoformat(session["timestamp"])
        duration = (datetime.now() - start_time).total_seconds()
        session["duration_seconds"] = round(duration, 2)
        session["status"] = "completed" if success else "failed"
        session["end_timestamp"] = datetime.now().isoformat()
        
        _log_metric(f"Analysis session ended: {session_id} - Duration: {duration:.2f}s - Status: {session['status']}")


def track_tool_call(
    tool_name: str,
    agent_name: str,
    session_id: Optional[str] = None,
    parameters: Optional[Dict] = None,
    success: bool = True,
    response_time_ms: Optional[float] = None,
    error_message: Optional[str] = None
):
    """Track a tool call by an agent.
    
    Args:
        tool_name: Name of the tool called
        agent_name: Name of the agent making the call
        session_id: Optional session ID
        parameters: Parameters passed to the tool
        success: Whether the call was successful
        response_time_ms: Response time in milliseconds
        error_message: Error message if call failed
    """
    timestamp = datetime.now().isoformat()
    
    call_record = {
        "timestamp": timestamp,
        "tool_name": tool_name,
        "agent_name": agent_name,
        "session_id": session_id,
        "success": success,
        "parameters": parameters or {}
    }
    
    if response_time_ms is not None:
        call_record["response_time_ms"] = round(response_time_ms, 2)
    
    if error_message:
        call_record["error_message"] = error_message
    
    _metrics["tool_calls"].append(call_record)
    _metrics["total_tool_calls"] += 1
    _metrics["tool_usage"][tool_name] += 1
    
    # Track agent activity
    _metrics["agent_activity"][agent_name].append({
        "timestamp": timestamp,
        "action": "tool_call",
        "tool": tool_name,
        "success": success
    })
    
    # Update session record if provided
    if session_id:
        for session in _metrics["analysis_sessions"]:
            if session["session_id"] == session_id:
                session["tool_calls"].append(call_record)
                if agent_name not in session["agents_used"]:
                    session["agents_used"].append(agent_name)
                break
    
    if success:
        _metrics["successful_tool_calls"] += 1
    else:
        _metrics["failed_tool_calls"] += 1
    
    status = "SUCCESS" if success else "FAILED"
    _log_metric(f"Tool Call: {tool_name} by {agent_name} - {status}")


def track_mcp_call(
    tool_name: str,
    response_time_ms: float,
    success: bool = True,
    error_message: Optional[str] = None
):
    """Track an MCP server call.
    
    Args:
        tool_name: Name of the MCP tool called
        response_time_ms: Response time in milliseconds
        success: Whether the call was successful
        error_message: Error message if call failed
    """
    timestamp = datetime.now().isoformat()
    
    call_record = {
        "timestamp": timestamp,
        "tool_name": tool_name,
        "response_time_ms": round(response_time_ms, 2),
        "success": success
    }
    
    if error_message:
        call_record["error_message"] = error_message
    
    _metrics["mcp_calls"].append(call_record)
    _metrics["total_mcp_calls"] += 1
    _metrics["mcp_response_times"].append(response_time_ms)
    
    _log_metric(f"MCP Call: {tool_name} - {response_time_ms:.2f}ms - {'SUCCESS' if success else 'FAILED'}")


def get_metrics_summary() -> Dict:
    """Get summary of all metrics.
    
    Returns:
        Dictionary with metrics summary
    """
    # Calculate average MCP response time
    avg_mcp_response_time = 0.0
    if _metrics["mcp_response_times"]:
        avg_mcp_response_time = sum(_metrics["mcp_response_times"]) / len(_metrics["mcp_response_times"])
    
    # Calculate tool call success rate
    success_rate = 0.0
    if _metrics["total_tool_calls"] > 0:
        success_rate = (_metrics["successful_tool_calls"] / _metrics["total_tool_calls"]) * 100
    
    # Calculate average analysis duration
    completed_sessions = [s for s in _metrics["analysis_sessions"] if s.get("duration_seconds") is not None]
    avg_duration = 0.0
    if completed_sessions:
        avg_duration = sum(s["duration_seconds"] for s in completed_sessions) / len(completed_sessions)
    
    return {
        "summary": {
            "start_time": _metrics["start_time"],
            "current_time": datetime.now().isoformat(),
            "total_analyses": _metrics["total_analyses"],
            "total_tool_calls": _metrics["total_tool_calls"],
            "successful_tool_calls": _metrics["successful_tool_calls"],
            "failed_tool_calls": _metrics["failed_tool_calls"],
            "tool_call_success_rate_percent": round(success_rate, 2),
            "total_mcp_calls": _metrics["total_mcp_calls"],
            "average_mcp_response_time_ms": round(avg_mcp_response_time, 2),
            "average_analysis_duration_seconds": round(avg_duration, 2)
        },
        "tool_usage": dict(_metrics["tool_usage"]),
        "agent_activity_summary": {
            agent: len(activities) for agent, activities in _metrics["agent_activity"].items()
        },
        "recent_sessions": _metrics["analysis_sessions"][-10:],  # Last 10 sessions
        "recent_tool_calls": _metrics["tool_calls"][-50:]  # Last 50 tool calls
    }


def get_all_metrics() -> Dict:
    """Get all metrics data.
    
    Returns:
        Complete metrics dictionary
    """
    return {
        "start_time": _metrics["start_time"],
        "current_time": datetime.now().isoformat(),
        "total_analyses": _metrics["total_analyses"],
        "total_tool_calls": _metrics["total_tool_calls"],
        "successful_tool_calls": _metrics["successful_tool_calls"],
        "failed_tool_calls": _metrics["failed_tool_calls"],
        "total_mcp_calls": _metrics["total_mcp_calls"],
        "analysis_sessions": _metrics["analysis_sessions"],
        "tool_calls": _metrics["tool_calls"],
        "tool_usage": dict(_metrics["tool_usage"]),
        "agent_activity": {k: v for k, v in _metrics["agent_activity"].items()},
        "mcp_calls": _metrics["mcp_calls"],
        "mcp_response_times": _metrics["mcp_response_times"]
    }


def save_metrics_to_file():
    """Save current metrics to JSON file."""
    try:
        metrics_data = get_all_metrics()
        with open(METRICS_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=2)
        _log_metric("Metrics saved to file")
    except Exception as e:
        _log_metric(f"Error saving metrics to file: {e}")


def reset_metrics():
    """Reset all metrics (useful for testing)."""
    global _metrics
    _metrics = {
        "analysis_sessions": [],
        "tool_calls": [],
        "agent_activity": defaultdict(list),
        "tool_usage": defaultdict(int),
        "mcp_calls": [],
        "start_time": datetime.now().isoformat(),
        "total_tool_calls": 0,
        "total_analyses": 0,
        "total_mcp_calls": 0,
        "successful_tool_calls": 0,
        "failed_tool_calls": 0,
        "mcp_response_times": []
    }
    _log_metric("Metrics reset")

