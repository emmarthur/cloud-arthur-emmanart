"""
View and display metrics from the Retail Intelligence Platform.

This script reads metrics data from JSON files and displays summary statistics.
"""
import json
import os
from pathlib import Path

# Paths to metrics files
CLIENT_METRICS_FILE = os.path.join(os.path.dirname(__file__), "logs", "client_metrics.json")
SERVER_METRICS_FILE = os.path.join(os.path.dirname(__file__), "..", "server", "logs", "server_metrics.json")

def load_metrics(file_path: str) -> dict:
    """Load metrics from JSON file."""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading metrics from {file_path}: {e}")
        return None


def print_metrics_summary(metrics: dict, title: str):
    """Print formatted metrics summary."""
    if not metrics:
        print(f"\n{title}: No metrics data available")
        return
    
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")
    
    # Print summary section
    if "summary" in metrics:
        summary = metrics["summary"]
        print("\n📊 SUMMARY")
        print("-" * 80)
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Print tool usage
    if "tool_usage" in metrics:
        print("\n🔧 TOOL USAGE")
        print("-" * 80)
        for tool, count in sorted(metrics["tool_usage"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {tool}: {count} calls")
    
    # Print API usage (server metrics)
    if "api_usage" in metrics:
        print("\n🌐 API USAGE")
        print("-" * 80)
        for api, count in sorted(metrics["api_usage"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {api}: {count} calls")
    
    # Print average response times
    if "average_response_times" in metrics:
        print("\n⏱️  AVERAGE RESPONSE TIMES")
        print("-" * 80)
        for api, times in metrics["average_response_times"].items():
            print(f"  {api}:")
            print(f"    Average: {times['avg_ms']} ms")
            print(f"    Min: {times['min_ms']} ms")
            print(f"    Max: {times['max_ms']} ms")
            print(f"    Count: {times['count']}")
    
    # Print agent activity (client metrics)
    if "agent_activity_summary" in metrics:
        print("\n🤖 AGENT ACTIVITY")
        print("-" * 80)
        for agent, count in sorted(metrics["agent_activity_summary"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {agent}: {count} activities")
    
    # Print recent sessions (client metrics)
    if "recent_sessions" in metrics and metrics["recent_sessions"]:
        print("\n📋 RECENT ANALYSIS SESSIONS")
        print("-" * 80)
        for session in metrics["recent_sessions"][-5:]:  # Last 5 sessions
            status_emoji = "✅" if session.get("status") == "completed" else "❌" if session.get("status") == "failed" else "⏳"
            duration = session.get("duration_seconds", "N/A")
            if isinstance(duration, (int, float)):
                duration = f"{duration:.2f}s"
            print(f"  {status_emoji} {session.get('session_id', 'Unknown')}: {duration}")
            print(f"    Project: {session.get('project_description', 'N/A')[:60]}...")
            print(f"    Tools used: {len(session.get('tool_calls', []))}")
            print(f"    Agents: {', '.join(session.get('agents_used', []))}")
    
    # Print errors if any
    if "errors" in metrics and metrics["errors"]:
        print("\n❌ RECENT ERRORS")
        print("-" * 80)
        for error in metrics["errors"][-5:]:  # Last 5 errors
            print(f"  [{error.get('timestamp', 'Unknown')}] {error.get('api_name', 'Unknown API')}")
            print(f"    Error: {error.get('error_message', 'Unknown error')[:100]}")


def main():
    """Main function to display metrics."""
    print("\n" + "="*80)
    print("RETAIL INTELLIGENCE PLATFORM - METRICS DASHBOARD")
    print("="*80)
    
    # Load client metrics
    from metrics import get_metrics_summary as get_client_summary
    client_summary = get_client_summary()
    print_metrics_summary(client_summary, "CLIENT METRICS")
    
    # Try to load server metrics (may not be available locally)
    server_metrics = load_metrics(SERVER_METRICS_FILE)
    if server_metrics:
        from server.metrics import get_metrics_summary as get_server_summary
        server_summary = get_server_summary()
        print_metrics_summary(server_summary, "SERVER METRICS")
    else:
        print("\n" + "="*80)
        print("SERVER METRICS: Not available (server metrics are tracked on Cloud Run)")
        print("="*80)
    
    print("\n" + "="*80)
    print("End of Metrics Report")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

