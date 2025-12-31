#!/bin/bash

# Script to run the Retail Intelligence Platform
# 
# Execution order:
# 1. Starts server.py (MCP server) in background on port 8080
# 2. Waits for server to be ready
# 3. Runs client.py (main client application)
# 
# Note: mcp_client.py is a module imported by client.py, not run directly.
#       It provides MCP client functions that client.py uses.

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}Retail Intelligence Platform - Application Launcher${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Function to check if venv is activated
is_venv_activated() {
    if [ -n "$VIRTUAL_ENV" ]; then
        return 0
    else
        return 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    local venv_path=""
    
    if [ -f "venv/bin/activate" ]; then
        venv_path="venv/bin/activate"
    elif [ -f "venv/Scripts/activate" ]; then
        venv_path="venv/Scripts/activate"
    else
        echo -e "${RED}Error: Virtual environment not found!${NC}"
        echo "Please create and activate a virtual environment first:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate  # or venv/Scripts/activate on Windows"
        exit 1
    fi
    
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source "$venv_path"
}

# Check if virtual environment is activated
if ! is_venv_activated; then
    echo -e "${YELLOW}Virtual environment is not activated.${NC}"
    activate_venv
else
    echo -e "${GREEN}Virtual environment is activated${NC}"
fi

# Check if required files exist
if [ ! -f "server/server.py" ]; then
    echo -e "${RED}Error: server/server.py not found!${NC}"
    exit 1
fi

if [ ! -f "client/client.py" ]; then
    echo -e "${RED}Error: client/client.py not found!${NC}"
    exit 1
fi

# Get port from environment or use default
PORT=${PORT:-8080}
MCP_URL="http://localhost:${PORT}"

echo ""
echo -e "${BLUE}Step 1: Starting MCP Server (server.py)${NC}"
echo "------------------------------------------------------------"
echo -e "Server will run on: ${GREEN}${MCP_URL}${NC}"
echo ""

# Check if port is already in use and kill the process
echo -e "${YELLOW}Checking if port ${PORT} is available...${NC}"

# Try to find and kill any Python processes that might be using the port
# Use a simple approach that won't hang
EXISTING_PID=""

# Quick check: look for python processes that might be servers
if command -v pgrep >/dev/null 2>&1; then
    # Find any python processes running server.py
    EXISTING_PID=$(pgrep -f "server.py" 2>/dev/null | head -1)
fi

# If we found a process, kill it
if [ -n "$EXISTING_PID" ] && [ "$EXISTING_PID" != "" ]; then
    echo -e "${YELLOW}Found existing server process (PID ${EXISTING_PID}). Killing it...${NC}"
    kill $EXISTING_PID 2>/dev/null || true
    sleep 2
    # Check if it's still running and force kill if needed
    if kill -0 $EXISTING_PID 2>/dev/null; then
        echo -e "${YELLOW}Force killing process...${NC}"
        kill -9 $EXISTING_PID 2>/dev/null || true
        sleep 1
    fi
    echo -e "${GREEN}Previous server process terminated${NC}"
else
    echo -e "${GREEN}No existing server process found${NC}"
fi

echo ""

# Start server in background
echo -e "${YELLOW}Starting server in background...${NC}"
cd server
python server.py > ../server.log 2>&1 &
SERVER_PID=$!
cd ..

echo -e "Server started with PID: ${GREEN}${SERVER_PID}${NC}"
echo ""

# Wait for server to show "Uvicorn running on" message
echo -e "${YELLOW}Waiting for server to initialize...${NC}"
echo -e "${YELLOW}(This may take a moment, checking every 2 seconds)${NC}"
SERVER_READY=false
CHECK_INTERVAL=2

while true; do
    # Check if process is still running
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "\n${RED}Error: Server process died!${NC}"
        echo "Check server.log for errors:"
        if [ -f "server.log" ]; then
            cat server.log
        fi
        exit 1
    fi
    
    # Check log for "Uvicorn running on" message
    if [ -f "server.log" ]; then
        if grep -q "Uvicorn running on" server.log 2>/dev/null; then
            echo -e "\n${GREEN}✓ Server is running!${NC}"
            echo ""
            echo "Server log (last few lines):"
            echo "------------------------------------------------------------"
            tail -5 server.log 2>/dev/null | grep -E "(Uvicorn|Server URL|Transport)" 2>/dev/null || tail -5 server.log 2>/dev/null
            echo "------------------------------------------------------------"
            SERVER_READY=true
            break
        fi
    fi
    
    echo -n "."
    sleep $CHECK_INTERVAL
done

# Give server a moment to fully initialize after we see the message
sleep 2

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up...${NC}"
    if kill -0 $SERVER_PID 2>/dev/null; then
        echo -e "Stopping server (PID: ${SERVER_PID})..."
        kill $SERVER_PID 2>/dev/null || true
        wait $SERVER_PID 2>/dev/null || true
    fi
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Register cleanup function
trap cleanup EXIT INT TERM


echo ""
echo -e "${BLUE}Step 2: Running Client (client.py)${NC}"
echo "------------------------------------------------------------"
echo -e "Note: ${YELLOW}mcp_client.py${NC} is imported by client.py automatically"
echo ""

# Set MCP_URL environment variable for client
export MCP_URL="${MCP_URL}/mcp"

# Check if .env file exists and load it
if [ -f ".env" ]; then
    echo -e "${GREEN}Loading environment variables from .env${NC}"
    # Safely load .env file, handling empty lines and special characters
    set -a
    source .env 2>/dev/null || true
    set +a
fi

# Run client
echo -e "${GREEN}Starting client application...${NC}"
echo ""

# Store current directory
SCRIPT_DIR="$(pwd)"

cd client
python client.py
CLIENT_EXIT_CODE=$?
cd "$SCRIPT_DIR"

echo ""
echo -e "${BLUE}============================================================${NC}"
if [ $CLIENT_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Application completed successfully!${NC}"
else
    echo -e "${RED}Client exited with code: ${CLIENT_EXIT_CODE}${NC}"
fi
echo -e "${BLUE}============================================================${NC}"

# Show metrics summary if available
echo ""
echo -e "${BLUE}Metrics Summary${NC}"
echo "------------------------------------------------------------"

# Wait a moment for metrics to be saved
sleep 2

METRICS_FILE="$SCRIPT_DIR/client/logs/client_metrics.json"
if [ -f "$METRICS_FILE" ]; then
    echo -e "${GREEN}Client metrics saved to: client/logs/client_metrics.json${NC}"
    # Try to show a quick summary - use absolute path to be sure
    if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
        PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
        export METRICS_FILE_PATH="$METRICS_FILE"
        $PYTHON_CMD -c "
import json
import sys
import os
try:
    metrics_file = os.environ.get('METRICS_FILE_PATH', '')
    if os.path.exists(metrics_file):
        with open(metrics_file, 'r', encoding='utf-8') as f:
            metrics = json.load(f)
        # Get summary from metrics directly (not from 'summary' key)
        total_analyses = metrics.get('total_analyses', 0)
        total_tool_calls = metrics.get('total_tool_calls', 0)
        successful_tool_calls = metrics.get('successful_tool_calls', 0)
        failed_tool_calls = metrics.get('failed_tool_calls', 0)
        total_mcp_calls = metrics.get('total_mcp_calls', 0)
        
        # Calculate success rate
        success_rate = 0.0
        if total_tool_calls > 0:
            success_rate = (successful_tool_calls / total_tool_calls) * 100
        
        # Calculate average MCP response time
        mcp_times = metrics.get('mcp_response_times', [])
        avg_mcp_time = 0.0
        if mcp_times:
            avg_mcp_time = sum(mcp_times) / len(mcp_times)
        
        print(f'Total analyses: {total_analyses}')
        print(f'Total tool calls: {total_tool_calls}')
        print(f'Successful tool calls: {successful_tool_calls}')
        print(f'Failed tool calls: {failed_tool_calls}')
        print(f'Success rate: {success_rate:.1f}%')
        print(f'Total MCP calls: {total_mcp_calls}')
        print(f'Average MCP response time: {avg_mcp_time:.1f}ms')
        
        # Show tool usage
        tool_usage = metrics.get('tool_usage', {})
        if tool_usage:
            print('')
            print('Tool usage:')
            for tool, count in sorted(tool_usage.items(), key=lambda x: x[1], reverse=True):
                print(f'  {tool}: {count} calls')
    else:
        print('Metrics file not found at: ' + metrics_file)
except Exception as e:
    print(f'Error reading metrics: {e}')
    import traceback
    traceback.print_exc()
" 2>/dev/null || echo "Metrics file exists (use 'python client/view_metrics.py' to view details)"
    fi
else
    echo -e "${YELLOW}Client metrics not yet available${NC}"
fi

SERVER_METRICS_FILE="$SCRIPT_DIR/server/logs/server_metrics.json"
if [ -f "$SERVER_METRICS_FILE" ]; then
    echo -e "${GREEN}Server metrics saved to: server/logs/server_metrics.json${NC}"
    # Show server metrics summary
    if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
        PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
        export SERVER_METRICS_FILE_PATH="$SERVER_METRICS_FILE"
        $PYTHON_CMD -c "
import json
import os
import sys
try:
    metrics_file = os.environ.get('SERVER_METRICS_FILE_PATH', '')
    if os.path.exists(metrics_file):
        with open(metrics_file, 'r', encoding='utf-8') as f:
            metrics = json.load(f)
        total_calls = metrics.get('total_calls', 0)
        successful_calls = metrics.get('successful_calls', 0)
        failed_calls = metrics.get('failed_calls', 0)
        print('')
        print('Server API calls:')
        print(f'  Total API calls: {total_calls}')
        print(f'  Successful: {successful_calls}')
        print(f'  Failed: {failed_calls}')
        if total_calls > 0:
            success_rate = (successful_calls / total_calls) * 100
            print(f'  Success rate: {success_rate:.1f}%')
except Exception:
    pass
" 2>/dev/null
    fi
else
    echo -e "${YELLOW}Server metrics: Available in Cloud Run logs (local metrics in server/logs/ if server ran locally)${NC}"
fi

echo ""
echo -e "${BLUE}To view detailed metrics, run:${NC}"
echo -e "  ${GREEN}cd client && python view_metrics.py${NC}"
echo ""

# Cleanup will be called automatically via trap

