"""
BigQuery Tool: Execute SQL queries against Google Cloud BigQuery Public Datasets.
Client agents provide SQL queries; this tool executes them and returns JSON results.
"""
import json
import os
import time
from datetime import datetime
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from google.auth.exceptions import DefaultCredentialsError
import sys
from pathlib import Path

# Add parent directory to path for metrics import
sys.path.insert(0, str(Path(__file__).parent.parent))
from metrics import track_api_call

# Logging setup: create logs directory and define log file path
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
BIGQUERY_LOG_FILE = os.path.join(LOG_DIR, "bigquery.log")

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

def bigquery_query(query: str) -> str:
    """Execute BigQuery SQL query against bigquery-public-data datasets.
    
    Args:
        query: SQL query string (must query bigquery-public-data datasets)
    
    Returns:
        JSON string with query results and metadata
    """
    try:
        _log_to_file(BIGQUERY_LOG_FILE, f"Function called with query: {query[:200] if query else 'None'}...")
        
        # Initialize BigQuery client (uses GOOGLE_APPLICATION_CREDENTIALS or default)
        client = bigquery.Client()
        
        # Validate query parameter
        if not query or not isinstance(query, str) or not query.strip():
            error_data = {
                "error": True,
                "error_message": "No BigQuery query provided. The client agent must construct and provide a SQL query.",
                "note": "The query should select from bigquery-public-data datasets. Available tables: census_bureau_international.midyear_population (columns: country_name, country_code, year, midyear_population)"
            }
            _log_to_file(BIGQUERY_LOG_FILE, f"ERROR: No query provided")
            return json.dumps(error_data)
        
        # Security check: ensure query only accesses public datasets (case-insensitive)
        query_upper = query.upper()
        if "BIGQUERY-PUBLIC-DATA" not in query_upper:
            error_data = {
                "error": True,
                "error_message": "Query must only access bigquery-public-data datasets for security.",
                "query_provided": query[:200] + "..." if len(query) > 200 else query
            }
            return json.dumps(error_data)
        
        # Execute query and process results
        try:
            # Track API call with metrics
            start_time = time.time()
            query_job = client.query(query)
            results = query_job.result()
            response_time_ms = (time.time() - start_time) * 1000
            
            # Convert BigQuery Row objects to dictionaries for JSON serialization
            rows = []
            for row in results:
                row_dict = {}
                for key in row.keys():
                    value = row[key]
                    # Handle non-serializable types (datetime, etc.)
                    if hasattr(value, 'isoformat'):  # datetime objects
                        value = value.isoformat()
                    elif not isinstance(value, (str, int, float, bool, type(None))):
                        value = str(value)
                    row_dict[key] = value
                rows.append(row_dict)
            
            # Build response with query results
            data = {
                "query_executed": query,
                "data_source": "Google Cloud BigQuery Public Datasets",
                "row_count": len(rows),
                "results": rows,
                "query_job_id": query_job.job_id if hasattr(query_job, 'job_id') else None
            }
            
            result_json = json.dumps(data)
            _log_to_file(BIGQUERY_LOG_FILE, f"SUCCESS: Query executed, returned {len(rows)} rows")
            _log_to_file(BIGQUERY_LOG_FILE, f"Response: {result_json[:500]}...")
            
            # Track successful API call
            track_api_call(
                api_name="BigQuery",
                tool_name="bigquery",
                success=True,
                response_time_ms=response_time_ms,
                parameters={"query_length": len(query), "rows_returned": len(rows)}
            )
            
            return result_json
        except GoogleCloudError as e:
            response_time_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0
            error_data = {
                "error": True,
                "error_message": f"BigQuery error: {str(e)}",
                "query": query[:200] + "..." if len(query) > 200 else query,
                "note": "Check that the query syntax is correct and the table/dataset exists in bigquery-public-data. Available table: census_bureau_international.midyear_population (columns: country_name, country_code, year, midyear_population)"
            }
            _log_to_file(BIGQUERY_LOG_FILE, f"ERROR: BigQuery error - {str(e)}")
            
            # Track failed API call
            track_api_call(
                api_name="BigQuery",
                tool_name="bigquery",
                success=False,
                response_time_ms=response_time_ms,
                error_message=str(e),
                parameters={"query_length": len(query)}
            )
            
            return json.dumps(error_data)
        except Exception as e:
            # Handle unexpected errors during query execution
            response_time_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0
            error_data = {
                "error": True,
                "error_message": f"Error executing query: {str(e)}",
                "query": query[:200] + "..." if len(query) > 200 else query,
                "error_type": type(e).__name__
            }
            _log_to_file(BIGQUERY_LOG_FILE, f"ERROR: Exception - {type(e).__name__}: {str(e)}")
            
            # Track failed API call
            track_api_call(
                api_name="BigQuery",
                tool_name="bigquery",
                success=False,
                response_time_ms=response_time_ms,
                error_message=str(e),
                parameters={"query_length": len(query)}
            )
            
            return json.dumps(error_data)
    except DefaultCredentialsError as e:
        # Handle missing credentials (common in local testing, auto-resolved on Cloud Run)
        error_data = {
            "error": True,
            "error_message": f"Google Cloud credentials not found: {str(e)}",
            "note": "This is expected in local testing. On Cloud Run, the service account will provide credentials automatically. For local testing, set GOOGLE_APPLICATION_CREDENTIALS environment variable or use 'gcloud auth application-default login'."
        }
        _log_to_file(BIGQUERY_LOG_FILE, f"ERROR: Credentials not found - {str(e)}")
        return json.dumps(error_data)
    except Exception as e:
        error_data = {
            "error": True,
            "error_message": f"Unexpected error: {str(e)}",
            "error_type": type(e).__name__
        }
        _log_to_file(BIGQUERY_LOG_FILE, f"ERROR: Unexpected error - {type(e).__name__}: {str(e)}")
        return json.dumps(error_data)

