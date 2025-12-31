# Retail Intelligence Platform - Setup and Run Guide

This guide explains how to set up and run the Retail Intelligence Platform using the provided bash scripts.

## Prerequisites

- Python 3.8 or higher
- Git (to clone the repository)
- Bash shell (Linux, Mac, or WSL on Windows)
- Google Cloud account (for BigQuery access - optional, but recommended)
- API keys (optional, for enhanced functionality):
  - Alpha Vantage API key (for financial data)
  - FRED API key (for economic indicators)

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd final
```

### 2. Create Virtual Environment

**Linux/Mac/WSL:**
```bash
python3 -m venv venv
```

**Windows (PowerShell):**
```bash
python -m venv venv
```

### 3. Install Requirements

Use the provided bash script to automatically install all dependencies:

```bash
# Make the script executable (one-time)
chmod +x install_requirements.sh

# Run the installation script
./install_requirements.sh
```

**What the script does:**
- Checks if virtual environment is activated
- Activates it if needed (supports both Linux and Windows paths)
- Upgrades pip
- Installs all requirements from `client/requirements.txt`
- Installs all requirements from `server/requirements.txt`
- Shows a summary of installed packages

**Manual installation (alternative):**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r client/requirements.txt
pip install -r server/requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# MCP Server URL (for client to connect to server)
MCP_URL=http://localhost:8080/mcp

# OpenAI API Key (required for CrewAI agents)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # or gpt-4, gpt-3.5-turbo, etc.

# Optional: API Keys for enhanced functionality
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
FRED_API_KEY=your_fred_key_here

# Google Cloud (for BigQuery - uses default credentials if not set)
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

**Note:** The system will work without Alpha Vantage and FRED API keys, but will use simulated data instead of real API responses.

## Running the Application

### Quick Start (Recommended)

Use the provided bash script to run everything automatically:

```bash
# Make the script executable (one-time)
chmod +x run_application.sh

# Run the application
./run_application.sh
```

**What the script does:**
1. Checks and activates virtual environment if needed
2. Checks for and kills any existing server processes on port 8080
3. Starts the MCP server (`server.py`) in the background
4. Waits for server to be ready (checks for "Uvicorn running on" message)
5. Runs the client application (`client.py`)
6. Displays metrics summary after completion
7. Cleans up by stopping the server

### Manual Method (Two Terminals)

If you prefer to run components separately:

**Terminal 1 - Start the Server:**
```bash
cd server
source ../venv/bin/activate  # or ..\venv\Scripts\activate on Windows
python server.py
```

Keep this terminal open. You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**Terminal 2 - Run the Client:**
```bash
cd client
source ../venv/bin/activate  # or ..\venv\Scripts\activate on Windows
python client.py
```

Enter your retail project description when prompted.

## Using the Application

1. **Start the application** using `./run_application.sh` or manually
2. **Enter a project description** when prompted, for example:
   ```
   Opening a new grocery store chain in the Pacific Northwest focusing on organic products
   ```
3. **Wait for analysis** - The system will:
   - Coordinate multiple specialist agents
   - Gather data from various APIs
   - Generate comprehensive analysis reports
4. **Review the results** - A detailed analysis will be displayed covering:
   - Operations & Supply Chain
   - Customer Analytics & Marketing
   - Financial & Sales Performance
   - Market Intelligence & Research
   - Product & E-commerce Strategy

## Viewing Metrics

After running the application, view detailed metrics:

```bash
cd client
python view_metrics.py
```

This displays:
- Total analyses performed
- Tool usage statistics
- API call metrics
- Success rates
- Response times
- Agent activity summaries

Metrics are automatically saved to:
- `client/logs/client_metrics.json` - Client-side metrics
- `server/logs/server_metrics.json` - Server-side metrics (if server ran locally)

## Troubleshooting

### Server Won't Start

**Port 8080 already in use:**
```bash
# Find what's using the port
lsof -i :8080  # Linux/Mac
netstat -ano | findstr :8080  # Windows

# Kill the process
kill $(lsof -t -i :8080)  # Linux/Mac
# Or use a different port:
PORT=8081 ./run_application.sh
```

**Missing dependencies:**
```bash
# Reinstall requirements
./install_requirements.sh
```

### Client Can't Connect to Server

1. **Check server is running** - Look for "Uvicorn running on" message
2. **Verify MCP_URL in .env file:**
   ```
   MCP_URL=http://localhost:8080/mcp
   ```
3. **Test server connection:**
   ```bash
   curl http://localhost:8080/
   ```

### Virtual Environment Issues

**WSL/Linux:**
```bash
# Create new venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
./install_requirements.sh
```

**Windows:**
```bash
# Create new venv
rmdir /s venv
python -m venv venv
venv\Scripts\activate
./install_requirements.sh
```

### Module Not Found Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac/WSL
# or
venv\Scripts\activate  # Windows

# Reinstall requirements
./install_requirements.sh
```

### BigQuery Credentials

If you see BigQuery credential errors:
- **Local development:** Run `gcloud auth application-default login`
- **Cloud Run:** Credentials are provided automatically via service account
- **Manual setup:** Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

## Project Structure

```
final/
├── server/                 # MCP server (runs on Cloud Run)
│   ├── server.py          # Main server file
│   ├── tools/             # API tool implementations
│   │   ├── bigquery.py
│   │   ├── alpha_vantage.py
│   │   ├── fred.py
│   │   ├── rest_countries.py
│   │   └── fake_store.py
│   ├── metrics.py         # Server-side metrics tracking
│   └── requirements.txt
├── client/                 # Client application
│   ├── client.py          # Main client file
│   ├── mcp_client.py      # MCP client implementation
│   ├── orchestrator.py    # Orchestrator agent
│   ├── agents/            # Specialist agents
│   │   ├── operations_agent.py
│   │   ├── customer_analytics_agent.py
│   │   ├── financial_agent.py
│   │   ├── market_intelligence_agent.py
│   │   ├── product_ecommerce_agent.py
│   │   └── tools.py
│   ├── metrics.py         # Client-side metrics tracking
│   ├── view_metrics.py    # Metrics viewer
│   └── requirements.txt
├── install_requirements.sh  # Installation script
├── run_application.sh       # Application launcher script
└── .env                     # Environment variables (create this)
```

## Bash Scripts Overview

### `install_requirements.sh`

**Purpose:** Installs all Python dependencies for both client and server.

**Features:**
- Automatically detects and activates virtual environment
- Supports both Linux/Mac and Windows venv paths
- Upgrades pip before installing
- Installs from both `client/requirements.txt` and `server/requirements.txt`
- Shows summary of installed packages

**Usage:**
```bash
chmod +x install_requirements.sh
./install_requirements.sh
```

### `run_application.sh`

**Purpose:** Runs the complete application (server + client).

**Features:**
- Automatically activates virtual environment if needed
- Kills any existing server processes on port 8080
- Starts MCP server in background
- Waits for server to be ready (checks for "Uvicorn running on" message)
- Runs client application
- Displays metrics summary after completion
- Automatically cleans up (stops server) on exit

**Usage:**
```bash
chmod +x run_application.sh
./run_application.sh
```

**Environment Variables:**
- `PORT` - Server port (default: 8080)
- `MCP_URL` - Server URL for client (default: http://localhost:8080/mcp)

## Example Project Descriptions

You can use any of these example descriptions from `retail_project_descriptions.txt`:

1. **Sustainable Fashion Store:**
   ```
   Opening a new omnichannel retail store specializing in sustainable fashion and eco-friendly products in downtown Seattle, Washington. The store will feature both a physical retail location (2,500 sq ft) and a comprehensive e-commerce platform.
   ```

2. **Tech Accessories Store:**
   ```
   Launching a premium tech accessories and electronics retail store in Shibuya, Tokyo, Japan. The store will occupy 1,800 sq ft in a high-traffic shopping district and focus on Japanese and international tech brands.
   ```

3. **Artisanal Food Store:**
   ```
   Establishing a boutique artisanal food and specialty grocery store in Barcelona, Spain. The 3,000 sq ft store will focus on locally sourced organic produce, Spanish wines, artisanal cheeses, and specialty foods from Mediterranean regions.
   ```

## Metrics Tracking

The platform automatically tracks:

**Client Metrics:**
- Analysis sessions (duration, success status)
- Tool calls by agent and tool name
- MCP server communication metrics
- Agent activity patterns

**Server Metrics:**
- API calls to external services
- Response times
- Success/failure rates
- Error logs

**View Metrics:**
```bash
cd client
python view_metrics.py
```

## Additional Resources

- **Agent Documentation:** See `agents_documentation.md` for detailed agent information
- **Business Benefits:** See `retail_business_benefits_analysis.md` for business value analysis
- **Metrics Implementation:** See `METRICS_TRACKING_IMPLEMENTATION.md` for metrics details
- **Project Plan:** See `plan.md` for implementation details

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review log files in `client/logs/` and `server/logs/`
3. Check server output in `server.log` (if using the script)
4. Verify all environment variables are set correctly in `.env`

## Next Steps

After setup:
1. Run `./install_requirements.sh` to install dependencies
2. Configure your `.env` file with API keys
3. Run `./run_application.sh` to start the application
4. Enter a retail project description
5. Review the comprehensive analysis report
6. View metrics with `python client/view_metrics.py`

