#!/bin/bash

# Debug script to run server and see actual errors

echo "============================================================"
echo "Debugging Server Startup"
echo "============================================================"
echo ""

# Check if venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        echo "Error: Virtual environment not found!"
        exit 1
    fi
fi

echo "Python: $(which python)"
echo "Python version: $(python --version)"
echo ""

# Check dependencies
echo "Checking dependencies..."
cd server
python -c "import fastmcp; print('✓ fastmcp installed')" 2>&1 || echo "✗ fastmcp not installed"
python -c "import requests; print('✓ requests installed')" 2>&1 || echo "✗ requests not installed"
python -c "from dotenv import load_dotenv; print('✓ python-dotenv installed')" 2>&1 || echo "✗ python-dotenv not installed"
python -c "from google.cloud import bigquery; print('✓ google-cloud-bigquery installed')" 2>&1 || echo "✗ google-cloud-bigquery not installed"
echo ""

# Try to import server modules
echo "Testing imports..."
python -c "
import sys
sys.path.insert(0, '.')
try:
    from tools.bigquery import bigquery_query
    print('✓ bigquery tool imported')
except Exception as e:
    print(f'✗ bigquery tool import failed: {e}')

try:
    from tools.rest_countries import rest_countries
    print('✓ rest_countries tool imported')
except Exception as e:
    print(f'✗ rest_countries tool import failed: {e}')

try:
    from tools.alpha_vantage import alpha_vantage
    print('✓ alpha_vantage tool imported')
except Exception as e:
    print(f'✗ alpha_vantage tool import failed: {e}')

try:
    from tools.fred import fred
    print('✓ fred tool imported')
except Exception as e:
    print(f'✗ fred tool import failed: {e}')

try:
    from tools.fake_store import fake_store
    print('✓ fake_store tool imported')
except Exception as e:
    print(f'✗ fake_store tool import failed: {e}')
"
echo ""

# Check if port is in use
PORT=${PORT:-8080}
echo "Checking if port $PORT is available..."
if command -v lsof >/dev/null 2>&1; then
    if lsof -i :$PORT >/dev/null 2>&1; then
        echo "⚠ Port $PORT is already in use:"
        lsof -i :$PORT
        echo ""
        read -p "Kill the process? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill $(lsof -t -i :$PORT) 2>/dev/null
            sleep 1
        fi
    else
        echo "✓ Port $PORT is available"
    fi
fi
echo ""

# Try to run server (will show actual errors)
echo "============================================================"
echo "Starting server (press Ctrl+C to stop)..."
echo "============================================================"
echo ""

python server.py

