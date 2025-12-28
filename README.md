# Cloud Computing Course Repository

This repository contains coursework and projects for a cloud computing course, including homework assignments, labs, and a comprehensive final project implementing a **Retail Intelligence Platform** using multi-agent AI systems.

## 📋 Repository Structure

```
cloud-arthur-emmanart/
├── final/              # Final project: Retail Intelligence Platform
├── hw1/                # Homework 1: Docker Hub
├── hw2/                # Homework 2: Flask Guestbook Application
├── hw3/                # Homework 3: Docker Containerization
├── hw4/                # Homework 4: Cloud Run Deployment with Datastore
├── labs2/              # Lab 2 assignments
├── notebooks/          # Lab notebooks and documentation
└── README.md           # This file
```

---

## 🎯 Final Project: Retail Intelligence Platform

### Overview

The **Retail Intelligence Platform** is a sophisticated multi-agent AI system that provides comprehensive analysis of retail business projects. The platform uses **CrewAI** to coordinate specialized AI agents that leverage **Model Context Protocol (MCP)** servers deployed on **Google Cloud Run** to access multiple APIs for data gathering and analysis.

### Key Features

- **Multi-Agent Architecture**: Six specialized AI agents working collaboratively
- **MCP Server Integration**: Remote tool access via Model Context Protocol
- **Cloud-Native Deployment**: Server deployed on Google Cloud Run
- **Comprehensive Analysis**: Covers operations, customer analytics, financial performance, market intelligence, and product strategy
- **API Integration**: Accesses BigQuery, REST Countries, Alpha Vantage, FRED, and Fake Store APIs

### Architecture

#### Client-Side (Local)
- **CrewAI Framework**: Orchestrates multiple autonomous agents
- **Specialized Agents**: Each agent focuses on a specific domain of retail analysis
- **MCP Client**: Communicates with the remote MCP server on Cloud Run
- **LLM Integration**: Uses OpenAI's GPT models for agent reasoning

#### Server-Side (Cloud Run)
- **FastMCP Server**: Implements Model Context Protocol standard
- **API Tools**: Five integrated tools providing access to external data sources
- **Containerized Deployment**: Docker container running on Google Cloud Run

### Agent System

The platform consists of **6 specialized agents**:

1. **Project Analysis Coordinator (Orchestrator)**
   - Coordinates all specialist agents
   - Synthesizes comprehensive reports
   - Simulates real-world impact on example companies

2. **Operations & Supply Chain Analyst**
   - Analyzes operational feasibility
   - Assesses supply chain complexity
   - Evaluates location-specific considerations

3. **Customer Analytics & Marketing Specialist**
   - Analyzes customer demographics and segmentation
   - Evaluates marketing potential and effectiveness
   - Provides actionable marketing strategies

4. **Financial & Sales Performance Analyst**
   - Assesses financial viability and profitability
   - Projects sales performance and revenue forecasts
   - Analyzes ROI potential and market conditions

5. **Market Intelligence & Research Analyst**
   - Evaluates market trends and industry dynamics
   - Assesses competitive positioning
   - Analyzes long-term macroeconomic factors

6. **Product & E-commerce Specialist**
   - Develops product strategy and assortment planning
   - Assesses e-commerce performance potential
   - Analyzes pricing strategies and omnichannel opportunities

### MCP Tools Available

All agents have access to these 5 MCP tools via the Cloud Run server:

1. **BigQuery Tool**: Execute SQL queries against `bigquery-public-data` datasets for demographic and population data
2. **REST Countries Tool**: Retrieve country/region data for geographic and logistics analysis
3. **Alpha Vantage Tool**: Retrieve financial market data and stock information
4. **FRED Tool**: Retrieve macroeconomic indicators and economic data from the Federal Reserve
5. **Fake Store Tool**: Retrieve product data for product portfolio and pricing analysis

### Technology Stack

#### Client
- **Python 3.10+**
- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM integration and tooling
- **OpenAI API**: GPT models for agent reasoning
- **python-dotenv**: Environment variable management

#### Server
- **Python 3.10**
- **FastMCP**: Model Context Protocol server framework
- **Google Cloud BigQuery**: Data warehouse queries
- **REST APIs**: External data source integration
- **Docker**: Containerization
- **Google Cloud Run**: Serverless deployment platform

### Getting Started

#### Prerequisites

- Python 3.10 or higher
- Google Cloud Platform account with:
  - Cloud Run API enabled
  - BigQuery API enabled
  - Appropriate service account permissions
- OpenAI API key
- API keys for:
  - Alpha Vantage (optional, for financial data)
  - FRED API (free, no key required for basic usage)

#### Client Setup

1. **Navigate to the client directory:**
   ```bash
   cd final/client
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in `final/client/`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   MCP_SERVER_URL=https://your-cloud-run-url.run.app
   ```

5. **Run the client:**
   ```bash
   python client.py
   ```

#### Server Setup and Deployment

1. **Navigate to the server directory:**
   ```bash
   cd final/server
   ```

2. **Set up Google Cloud credentials:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Configure BigQuery permissions:**
   ```bash
   ./grant_bigquery_roles.sh
   ```

4. **Set up environment variables for Cloud Run:**
   Create a `.env` file or use Cloud Run environment variables:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   ALPHA_VANTAGE_API_KEY=your_key_here  # Optional
   ```

5. **Build and deploy to Cloud Run:**
   ```bash
   # Build the Docker image
   docker build -t gcr.io/YOUR_PROJECT_ID/retail-mcp-server .
   
   # Push to Google Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/retail-mcp-server
   
   # Deploy to Cloud Run
   gcloud run deploy retail-mcp-server \
     --image gcr.io/YOUR_PROJECT_ID/retail-mcp-server \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ALPHA_VANTAGE_API_KEY=your_key_here
   ```

   Or use the provided deployment script:
   ```bash
   ./rebuild_and_deploy.sh
   ```

### Usage Example

```python
from client import analyze_retail_project

project_description = """
Opening a new sustainable fashion retail store in downtown Seattle, Washington.
The store will feature both a physical retail location (2,500 sq ft) and an 
e-commerce platform, focusing on ethically sourced clothing and accessories.
Initial inventory investment of $150,000 with projected monthly sales of $75,000.
"""

result = analyze_retail_project(project_description)
print(result)  # Comprehensive analysis report
```

### Project Workflow

1. **User Input**: Provides a retail project description
2. **Orchestrator Coordination**: Determines relevant analysis areas
3. **Specialist Analysis**: Each relevant agent:
   - Examines the project description
   - Determines required data
   - Selects appropriate MCP tools
   - Calls tools with correct parameters
   - Analyzes retrieved data
   - Produces specialized analysis report
4. **Synthesis**: Orchestrator combines all analyses into a comprehensive report
5. **Output**: Final unified report with insights across all relevant areas

### Design Principles

- **Intelligent Tool Selection**: Agents autonomously determine which tools to use based on project needs
- **Flexible Access**: All agents can access all tools (not limited to one tool per agent)
- **Comprehensive Analysis**: Multiple perspectives ensure thorough project evaluation
- **Modular Architecture**: Each agent is a separate module for maintainability
- **Detailed Logging**: Tool calls and agent activities are logged for debugging

### File Structure

```
final/
├── client/
│   ├── client.py                    # Main entry point
│   ├── mcp_client.py                # MCP client implementation
│   ├── orchestrator.py              # Orchestrator agent
│   ├── requirements.txt             # Python dependencies
│   └── agents/
│       ├── operations_agent.py      # Operations & Supply Chain Analyst
│       ├── customer_analytics_agent.py  # Customer Analytics Specialist
│       ├── financial_agent.py       # Financial & Sales Performance Analyst
│       ├── market_intelligence_agent.py # Market Intelligence Analyst
│       ├── product_ecommerce_agent.py   # Product & E-commerce Specialist
│       └── tools.py                 # Shared tool wrappers
│
├── server/
│   ├── server.py                    # MCP server implementation
│   ├── Dockerfile                   # Container definition
│   ├── requirements.txt             # Python dependencies
│   ├── rebuild_and_deploy.sh        # Deployment script
│   └── tools/
│       ├── bigquery.py              # BigQuery tool implementation
│       ├── rest_countries.py        # REST Countries tool
│       ├── alpha_vantage.py         # Alpha Vantage tool
│       ├── fred.py                  # FRED tool
│       └── fake_store.py            # Fake Store tool
│
├── agents_documentation.md          # Detailed agent documentation
├── retail_project_descriptions.txt  # Example project descriptions
└── final_instructions.txt          # Project requirements
```

### Security Notes

- **API Keys**: Never commit API keys to the repository. Use environment variables or Google Cloud Secrets Manager
- **`.env` Files**: All `.env` files are gitignored. Create local `.env` files for development
- **Cloud Run**: Server can be configured with authentication if needed

### Documentation

- **Agent Documentation**: See `final/agents_documentation.md` for detailed agent specifications
- **Project Instructions**: See `final/final_instructions.txt` for original project requirements
- **Example Projects**: See `final/retail_project_descriptions.txt` for sample retail project descriptions

---

## 📚 Homework Assignments

### Homework 1: Docker Hub
Basic Docker containerization and Docker Hub integration.

### Homework 2: Flask Guestbook Application
A Flask-based guestbook web application with SQLite database backend.

### Homework 3: Docker Containerization
Containerizing applications using Docker with multi-stage builds.

### Homework 4: Cloud Run Deployment with Datastore
- Adapted Flask application to use Google Cloud Datastore
- Containerized with Docker
- Deployed to Google Cloud Run
- URL stored in `hw4/url.txt`

---

## 🧪 Labs

The repository includes lab assignments covering various cloud computing topics:
- **Lab 1**: Network simulation and subnetting
- **Lab 2**: Cloud infrastructure basics
- **Lab 3**: Python guestbook application
- **Labs 4-10**: Various cloud computing concepts and implementations

Lab notebooks and documentation are stored in the `notebooks/` directory.

---

## 🛠️ Development

### Git Workflow

This repository follows incremental development practices:
- Frequent commits with descriptive messages
- One commit per major feature or tool implementation
- Clear commit history showing development timeline

### Code Quality Standards

- **Documentation**: All functions include docstrings
- **Modularity**: Code organized into logical modules
- **Readability**: Clean, well-commented code
- **No Hard-coded Secrets**: All sensitive data in environment variables

---

## 📝 License

This repository contains coursework and is intended for educational purposes.

---

## 👤 Author

**Emmanuel Arthur** (`emmanart`)

---

## 🔗 Related Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google Cloud BigQuery](https://cloud.google.com/bigquery/docs)
- [FastMCP](https://github.com/jlowin/fastmcp)

---

## 📊 Project Status

✅ **Final Project**: Complete and deployed  
✅ **Homework Assignments**: All completed  
✅ **Labs**: Completed and documented  

---

*Last Updated: December 2024*
