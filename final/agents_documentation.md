# CrewAI Agents Documentation

## Program Name: **Retail Intelligence Platform**

A multi-agent system that uses CrewAI to coordinate specialized AI agents for comprehensive retail project analysis. The platform leverages MCP (Model Context Protocol) servers to provide agents with access to multiple APIs, enabling intelligent data gathering and analysis across operations, customer analytics, financial performance, market intelligence, and product strategy.

---

## Agent Overview

The system consists of **6 agents** working together:

1. **Project Analysis Coordinator** (Orchestrator)
2. **Operations & Supply Chain Analyst**
3. **Customer Analytics & Marketing Specialist**
4. **Financial & Sales Performance Analyst**
5. **Market Intelligence & Research Analyst**
6. **Product & E-commerce Specialist**

All agents have access to all MCP tools and intelligently select which tools to use based on the project requirements.

---

## 1. Project Analysis Coordinator (Orchestrator)

**Role:** Coordinates specialized agents and synthesizes comprehensive reports.

The orchestrator agent is the coordinator for the entire analysis team. It understands retail project descriptions and determines which specialized areas of analysis are relevant. The orchestrator coordinates specialist agents to gather comprehensive insights from their respective domains. After all specialist agents complete their analyses, it synthesizes their findings into one unified report that demonstrates the project's usefulness and impact across all relevant retail areas. It also simulates the impact on an example company to demonstrate real-world implications.

---

## 2. Operations & Supply Chain Analyst

**Role:** Analyzes operations, logistics, and supply chain factors for retail projects.

This agent specializes in operational feasibility and supply chain complexity analysis. It examines project descriptions to determine what operational data is needed, then uses tools like REST Countries for geographic logistics data, BigQuery for demographic and population data, and FRED for economic indicators. The agent assesses supply chain network complexity, regional distribution challenges, and location-specific operational considerations. It provides quantitative insights on operational feasibility and impact to help determine if a retail project is operationally viable.

---

## 3. Customer Analytics & Marketing Specialist

**Role:** Analyzes customer behavior, segmentation, and marketing effectiveness for retail projects.

This agent focuses on customer demographics, market segmentation, and marketing potential. It uses BigQuery to gather customer demographic data, REST Countries for market size information, FRED for economic indicators affecting customer spending, and Fake Store for product preferences. The agent provides detailed customer segmentation analysis and marketing potential assessments. It evaluates customer impact and geographic customer distribution to provide actionable marketing strategies for the retail project.

---

## 4. Financial & Sales Performance Analyst

**Role:** Analyzes financial performance, profitability, and sales forecasting for retail projects.

This agent specializes in financial viability and sales performance projections. It uses Alpha Vantage for market conditions and stock data, FRED for macroeconomic indicators, BigQuery for demographic data affecting market size and revenue potential, and Fake Store for pricing strategies. The agent provides financial viability assessments and sales performance projections with revenue forecasts. It analyzes ROI potential and provides quantitative financial impact evaluations to determine if a retail project is financially sound.

---

## 5. Market Intelligence & Research Analyst

**Role:** Analyzes market trends, consumer insights, and competitor positioning for retail projects.

This agent focuses on market viability and competitive intelligence. It uses FRED for macroeconomic indicators and market trends, Alpha Vantage for market conditions and industry performance, BigQuery for demographic and market size data, and Fake Store for product trends and competitive insights. The agent assesses market trends and industry dynamics to evaluate competitive positioning. It identifies market viability and opportunities, and analyzes long-term macroeconomic factors affecting retail success.

---

## 6. Product & E-commerce Specialist

**Role:** Analyzes product lifecycle, assortment planning, and e-commerce performance for retail projects.

This agent specializes in product strategy and e-commerce performance. It uses Fake Store for product portfolio data and pricing strategies, BigQuery for demographic data affecting product preferences, REST Countries for regional product preferences, and FRED for economic conditions affecting product demand. The agent provides product strategy and assortment planning recommendations. It assesses e-commerce performance potential, analyzes pricing strategies, and identifies omnichannel integration opportunities for the retail project.

---

## Agent Workflow

1. **Project Description Input:** User provides a retail project description
2. **Orchestrator Coordination:** Orchestrator determines relevant analysis areas
3. **Specialist Analysis:** Each relevant specialist agent:
   - Examines the project description
   - Determines what data is needed
   - Selects appropriate MCP tools
   - Calls tools with correct parameters
   - Analyzes retrieved data
   - Produces specialized analysis report
4. **Synthesis:** Orchestrator synthesizes all analyses into comprehensive report
5. **Output:** Final unified report with insights across all relevant areas

---

## MCP Tools Available to All Agents

All agents have access to these 5 MCP tools:

- **BigQuery Tool:** Execute SQL queries against bigquery-public-data datasets for demographic and population data
- **REST Countries Tool:** Retrieve country/region data for geographic and logistics analysis
- **Alpha Vantage Tool:** Retrieve financial market data and stock information
- **FRED Tool:** Retrieve macroeconomic indicators and economic data
- **Fake Store Tool:** Retrieve product data for product portfolio and pricing analysis

---

## Design Principles

- **Intelligent Tool Selection:** Agents determine which tools to use based on project needs
- **Flexible Access:** All agents can use all tools (not limited to one tool per agent)
- **Comprehensive Analysis:** Multiple perspectives ensure thorough project evaluation
- **Modular Architecture:** Each agent is a separate module for maintainability
- **Detailed Logging:** Tool calls and agent activities are logged for debugging

---

## File Structure

```
client/
├── client.py                    # Main entry point
├── mcp_client.py                # MCP client implementation
├── orchestrator.py              # Orchestrator agent
└── agents/
    ├── operations_agent.py      # Operations & Supply Chain Analyst
    ├── customer_analytics_agent.py  # Customer Analytics & Marketing Specialist
    ├── financial_agent.py       # Financial & Sales Performance Analyst
    ├── market_intelligence_agent.py # Market Intelligence & Research Analyst
    ├── product_ecommerce_agent.py   # Product & E-commerce Specialist
    └── tools.py                 # Shared tool wrappers for all agents
```

---

## Usage Example

```python
from client import analyze_retail_project

project_description = "A new grocery store chain in the Pacific Northwest focusing on organic products"

result = analyze_retail_project(project_description)
print(result)  # Comprehensive analysis report
```

The system will automatically:
1. Coordinate all relevant specialist agents
2. Have each agent gather necessary data using MCP tools
3. Synthesize all analyses into a comprehensive report

---

## Metrics Tracking System

The Retail Intelligence Platform includes a comprehensive metrics tracking system that monitors API calls, tool usage, agent activity, and performance metrics across both the client and server components.

### Overview

The metrics system tracks:
- **API Calls:** All external API calls made by server tools (Alpha Vantage, FRED, REST Countries, Fake Store, BigQuery)
- **Tool Usage:** Frequency and success rates of each MCP tool
- **Agent Activity:** Which agents use which tools and how often
- **Analysis Sessions:** Complete analysis sessions with duration and success tracking
- **Performance Metrics:** Response times, success rates, error rates
- **MCP Server Calls:** Client-to-server communication metrics

### Metrics Components

#### Server-Side Metrics (`server/metrics.py`)

Tracks metrics for the MCP server running on Cloud Run:

**Tracked Metrics:**
- Total API calls by external service
- Success/failure rates per API
- Response times (average, min, max) per API
- Tool call counts per MCP tool
- Error logs with timestamps and details
- API call parameters and results

**Metrics Storage:**
- Log file: `server/logs/server_metrics.log`
- JSON file: `server/logs/server_metrics.json` (auto-saved every 10 calls)

**Key Functions:**
- `track_api_call()`: Records each external API call with timing and success status
- `get_metrics_summary()`: Returns summary statistics
- `get_all_metrics()`: Returns complete metrics data
- `save_metrics_to_file()`: Persists metrics to JSON file

#### Client-Side Metrics (`client/metrics.py`)

Tracks metrics for the client application and agent activity:

**Tracked Metrics:**
- Analysis sessions (start time, duration, success status)
- Tool calls by agent and tool name
- Agent activity summaries
- MCP server call metrics (response times, success rates)
- Tool usage frequency
- Project descriptions and session details

**Metrics Storage:**
- Log file: `client/logs/client_metrics.log`
- JSON file: `client/logs/client_metrics.json` (auto-saved after each analysis)

**Key Functions:**
- `start_analysis_session()`: Begins tracking a new analysis session
- `end_analysis_session()`: Completes session tracking with duration
- `track_tool_call()`: Records tool usage by agents
- `track_mcp_call()`: Records MCP server communication metrics
- `get_metrics_summary()`: Returns summary statistics
- `get_all_metrics()`: Returns complete metrics data

### Integration Points

**Server Tools Integration:**
All server tools (`server/tools/*.py`) automatically track:
- API call start/end times
- Success/failure status
- Response times
- Error messages
- Parameters used

**Client Integration:**
- `client/client.py`: Tracks analysis sessions
- `client/mcp_client.py`: Tracks MCP server calls
- `client/agents/tools.py`: Tracks tool usage by agents

### Viewing Metrics

#### Command-Line View

Use the metrics viewer script:

```bash
cd client
python view_metrics.py
```

This displays:
- Summary statistics (total calls, success rates, etc.)
- Tool usage breakdown
- API usage statistics
- Average response times
- Agent activity summaries
- Recent analysis sessions
- Recent errors

#### Programmatic Access

Access metrics programmatically:

```python
# Client metrics
from client.metrics import get_metrics_summary, get_all_metrics

summary = get_metrics_summary()
all_metrics = get_all_metrics()

# Server metrics (if running locally)
from server.metrics import get_metrics_summary, get_all_metrics

server_summary = get_metrics_summary()
server_all = get_all_metrics()
```

### Metrics Data Structure

#### Client Metrics Summary

```json
{
  "summary": {
    "start_time": "2024-01-01T00:00:00",
    "current_time": "2024-01-01T12:00:00",
    "total_analyses": 10,
    "total_tool_calls": 50,
    "successful_tool_calls": 48,
    "failed_tool_calls": 2,
    "tool_call_success_rate_percent": 96.0,
    "total_mcp_calls": 50,
    "average_mcp_response_time_ms": 1250.5,
    "average_analysis_duration_seconds": 45.2
  },
  "tool_usage": {
    "BigQuery Tool": 15,
    "REST Countries Tool": 10,
    "Alpha Vantage Tool": 8,
    "FRED Tool": 12,
    "Fake Store Tool": 5
  },
  "agent_activity_summary": {
    "Operations & Supply Chain Analyst": 12,
    "Customer Analytics & Marketing Specialist": 10,
    "Financial & Sales Performance Analyst": 8,
    "Market Intelligence & Research Analyst": 10,
    "Product & E-commerce Specialist": 10
  }
}
```

#### Server Metrics Summary

```json
{
  "summary": {
    "start_time": "2024-01-01T00:00:00",
    "current_time": "2024-01-01T12:00:00",
    "total_api_calls": 50,
    "successful_calls": 48,
    "failed_calls": 2,
    "success_rate_percent": 96.0
  },
  "tool_usage": {
    "bigquery": 15,
    "rest_countries_api": 10,
    "alpha_vantage_api": 8,
    "fred_api": 12,
    "fake_store_api": 5
  },
  "api_usage": {
    "BigQuery": 15,
    "REST Countries": 10,
    "Alpha Vantage": 8,
    "FRED": 12,
    "Fake Store": 5
  },
  "average_response_times": {
    "BigQuery": {
      "avg_ms": 1250.5,
      "min_ms": 800.0,
      "max_ms": 2000.0,
      "count": 15
    }
  }
}
```

### Use Cases

**Performance Monitoring:**
- Track API response times to identify slow services
- Monitor success rates to detect API issues
- Analyze tool usage patterns

**Cost Management:**
- Count API calls to estimate costs
- Identify most-used APIs for optimization
- Track usage trends over time

**Debugging:**
- Review error logs with timestamps
- Trace tool call sequences
- Identify problematic API calls

**Analytics:**
- Understand agent behavior patterns
- Analyze tool selection by agents
- Measure analysis session durations

### Best Practices

1. **Regular Review:** Check metrics regularly to monitor system health
2. **Error Analysis:** Review error logs to identify and fix issues
3. **Performance Optimization:** Use response time data to optimize slow operations
4. **Cost Tracking:** Monitor API call counts to manage costs
5. **Session Analysis:** Review analysis sessions to understand usage patterns

### Metrics Retention

- Metrics are stored in JSON files for persistence
- Log files grow over time (consider rotation for production)
- Metrics are automatically saved:
  - Server: Every 10 API calls
  - Client: After each analysis session

### Cloud Run Considerations

On Cloud Run, server metrics are:
- Logged to stdout/stderr (captured by Cloud Logging)
- Saved to JSON file (if filesystem is writable)
- Accessible via Cloud Logging dashboard

Client metrics are always stored locally in the `client/logs/` directory.