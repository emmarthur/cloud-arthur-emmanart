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
