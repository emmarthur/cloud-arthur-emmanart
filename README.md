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
├── labs2/              # Lab 2 assignments (PDFs)
├── notebooks/          # Lab notebooks and documentation (Labs 1-10)
└── README.md           # This file
```

---

## 📚 Homework Assignments

### Homework 1: Docker Hub
**Location:** `hw1/`

Basic Docker containerization and Docker Hub integration. This assignment focused on:
- Creating Docker images
- Pushing images to Docker Hub
- Understanding container registries

**Contents:**
- `dockerhub.txt` - Docker Hub username

---

### Homework 2: Flask Guestbook Application
**Location:** `hw2/`

A Flask-based guestbook web application implementing the Model-View-Presenter (MVP) pattern with a SQLite database backend. Users can view and add songs to a collection.

**Key Features:**
- Flask web framework
- SQLite database for data persistence
- MVP architectural pattern
- Routes for landing page, viewing entries, and adding entries

**File Structure:**
```
hw2/
├── app.py              # Main Flask application
├── index.py            # Landing page presenter
├── sign.py             # Add entry presenter
├── view.py             # View entries presenter
├── Model/
│   ├── Model.py        # Base model interface
│   └── model_sqlite3.py # SQLite implementation
├── templates/          # HTML templates
│   ├── layout.html
│   ├── index.html
│   ├── sign.html
│   └── view.html
├── static/
│   └── style.css       # Styling
└── requirements.txt    # Python dependencies
```

**Technologies:**
- Python 3
- Flask
- SQLite3
- HTML/CSS

---

### Homework 3: Docker Containerization
**Location:** `hw3/`

Containerizing applications using Docker with multi-stage builds. This assignment focused on creating optimized Docker images for the Flask application.

**Contents:**
- `Dockerfile.large` - Full Ubuntu-based image with all dependencies
- `Dockerfile.small` - Optimized smaller image
- `screenshots.pdf` - Documentation of the containerization process

**Key Concepts:**
- Multi-stage Docker builds
- Image optimization
- Layer caching strategies
- Container port configuration

---

### Homework 4: Cloud Run Deployment with Datastore
**Location:** `hw4/`

Advanced deployment assignment adapting the Flask guestbook application to use Google Cloud Datastore and deploying it to Google Cloud Run.

**Key Features:**
- Migrated from SQLite to Google Cloud Datastore
- Containerized with Docker
- Deployed to Google Cloud Run (serverless platform)
- Production-ready configuration

**File Structure:**
```
hw4/
├── app.py              # Main Flask application (Cloud Run compatible)
├── Dockerfile          # Container definition for Cloud Run
├── Model/
│   ├── Model.py        # Base model interface
│   ├── model_sqlite3.py # SQLite implementation (for local dev)
│   └── model_datastore.py # Cloud Datastore implementation
├── templates/          # HTML templates
├── static/             # CSS styling
├── url.txt             # Cloud Run deployment URL
└── requirements.txt    # Python dependencies
```

**Deployment:**
- **Live URL:** https://hw4-325950842705.us-west1.run.app (stored in `hw4/url.txt`)
- Configured for Cloud Run's port environment variable
- Uses Cloud Datastore as the production database

**Technologies:**
- Google Cloud Datastore
- Google Cloud Run
- Docker
- Flask

---

## 🧪 Labs

Lab assignments and documentation are stored in the `notebooks/` directory. Each lab folder contains PDFs, documentation, screenshots, and implementation details.

### Lab 1: Network Simulation and Subnetting
**Location:** `notebooks/Labs1/`

Network infrastructure and subnetting exercises using network simulation tools.

**What I Did:**
Configured Google Cloud VPC networks with subnetting across multiple regions. Analyzed ARP tables to understand network addressing, examined default VPC subnetworks (43 regions with /20 CIDR prefixes), and created VM instances in different regions (europe-north1-a and asia-east1-a) to verify network connectivity. Used network tools like netstat and nmap to monitor services and scan network security. Verified that instances in the same VPC network can communicate via virtual switches.

**Contents:**
- `Labs1.pdf` - Lab instructions and documentation
- `Lab1_including_images.pdf` - Complete lab with embedded images
- Multiple screenshots demonstrating:
  - Network subnet configuration
  - Instance connectivity testing
  - Network topology visualization
  - Subnet allocation across regions
  - Network security scanning results

**Tools & Technologies:**
- **Google Cloud Console**: Web-based interface for cloud resource management
- **Google Cloud VPC**: Virtual Private Cloud for network isolation and subnetting
- **Google Compute Engine**: VM instances across multiple regions
- **ARP (Address Resolution Protocol)**: Network address resolution commands (`arp -an`)
- **netstat**: Network statistics and connection monitoring tool
- **nmap**: Network security scanning and port discovery tool
- **CIDR Notation**: Subnet design and IP address allocation (/20, /24 prefixes)
- **Cloud Shell**: Command-line interface for Google Cloud operations
- **awk**: Text processing for network data extraction
- **Virtual Switch**: Network connectivity within VPC

**Key Topics:**
- VPC (Virtual Private Cloud) configuration
- Subnet design and CIDR notation
- Network security groups
- Instance networking and connectivity
- Network monitoring and security scanning

---

### Lab 2: Cloud Infrastructure Basics
**Location:** `labs2/` and `notebooks/Labs2/`

Introduction to cloud infrastructure concepts and services.

**What I Did:**
Set up Google Cloud Compute Engine VMs and used SSH for remote access. Monitored network services using netstat to identify services accessible from external interfaces (like sshd) versus local-only services (like cupsd). Measured network bandwidth between VMs using iperf3. Analyzed HTTP requests using curl and browser developer tools, examining HTTP/2 and HTTP/3 protocols, redirects (307 status codes), and cookie handling. Used ChatGPT to generate network diagnostic commands and explored DNS lookups and geographic IP resolution.

**Contents:**
- `Lab_2.1.pdf` - First part of Lab 2
- `Lab_2.2.pdf` - Second part of Lab 2

**Tools & Technologies:**
- **Google Cloud Compute Engine**: VM instance creation and management
- **SSH (Secure Shell)**: Remote access to VMs
- **netstat / ss**: Network service and port monitoring (`sudo netstat -tulpn`)
- **systemd-resolved**: DNS resolution service
- **iperf3**: Network bandwidth measurement tool
- **curl**: HTTP client for testing web requests
- **Browser Developer Tools**: Network inspection (HTTP/2, HTTP/3, cookies, redirects)
- **ChatGPT / LLM Tools**: AI-assisted command generation
- **Google Cloud Console**: Web-based resource management

---

### Lab 3: Python Guestbook Application
**Location:** `notebooks/Labs3/`

Implementation of a Python/Flask guestbook application deployed to cloud infrastructure.

**What I Did:**
Developed and deployed a Flask-based guestbook web application to Google Cloud. Created database tables (Recommendation, Rating, Accommodation) with proper primary keys and schemas. Performed SQL queries to filter accommodations by location (Dublin), price ranges, and types. Deployed the application to cloud infrastructure and verified successful connections. Examined database schemas and performed data dumps to understand the database structure.

**Contents:**
- `Lab_3.pdf` - Lab instructions
- `labs3.md` - Lab documentation and notes
- `images/Emmanuel-emmanart(python-guestbook-result).png` - Screenshot of deployed application

**Tools & Technologies:**
- **Python 3**: Programming language
- **Flask**: Web application framework
- **Google Cloud Platform**: Cloud deployment platform
- **Google App Engine / Cloud Run**: Serverless deployment services
- **Google Cloud SQL / Cloud Datastore**: Database services
- **SQL**: Database query language for table operations
- **Git**: Version control for code management
- **Cloud Shell / Local Terminal**: Development and deployment interface
- **Web Browser**: Application testing and verification

**Key Topics:**
- Flask web application development
- Cloud deployment and configuration
- Web application architecture

---

### Lab 4: Cloud Services and APIs
**Location:** `notebooks/Labs4/`

**Contents:**
- `Lab_4.pdf` - Lab documentation

**What I Did:**
Worked with Docker containerization, creating container images from Ubuntu and Alpine Linux base images. Analyzed Docker image layers to identify which layers add the most size (apt-get install layer was 102.79 MB). Optimized images by switching to Alpine Linux, reducing image size by 12.1 MB. Explored SSL/TLS certificates with Let's Encrypt and configured HTTPS for secure web connections. Examined container image sizes and layer composition.

**Tools & Technologies:**
- **Docker**: Containerization platform
- **Docker Hub**: Container image registry
- **Dockerfile**: Container image definition
- **Ubuntu**: Base Linux distribution for containers
- **Alpine Linux**: Lightweight Linux distribution for smaller containers
- **apt-get**: Package management in Ubuntu containers
- **Let's Encrypt**: SSL/TLS certificate authority
- **HTTPS**: Secure web protocol
- **Container Layer Analysis**: Docker image inspection tools

---

### Lab 6: Advanced Cloud Concepts
**Location:** `notebooks/Labs6/`

**Contents:**
- `Lab_6.pdf` - Lab documentation

**What I Did:**
Deployed applications to Google Cloud Run with containerized services listening on port 8080. Configured Cloud Run proxy services with environment variables for secure secret management. Set up Google Cloud Load Balancers for traffic distribution. Created Cloud Functions that process images using ImageMagick (blurring operations) triggered by Cloud Storage bucket events. Implemented Google Cloud Pub/Sub messaging for asynchronous communication, publishing and subscribing to messages. Explored SSRF (Server-Side Request Forgery) vulnerabilities and Google's metadata service protection mechanisms.

**Tools & Technologies:**
- **Google Cloud Run**: Serverless container platform
- **Google Cloud Load Balancer**: Traffic distribution and management
- **Docker**: Containerization
- **Google Container Registry**: Container image storage
- **Cloud Run Proxy**: Secure proxy service with environment variables
- **Google Cloud Functions**: Serverless function execution
- **Google Cloud Storage**: Object storage and file buckets
- **ImageMagick**: Image processing library (blur, transform operations)
- **Google Cloud Pub/Sub**: Message queuing and event streaming
- **Python**: Programming language for cloud functions
- **Metadata Service Security**: SSRF protection mechanisms

---

### Lab 7: Cloud Deployment Strategies
**Location:** `notebooks/Labs7/`

**Contents:**
- `Lab_7.pdf` - Lab documentation

**What I Did:**
Used Terraform for Infrastructure as Code, creating and managing VM instances with startup scripts. Deployed applications to Google Kubernetes Engine (GKE), creating instance templates, instance groups, and managing containerized services with Kubernetes. Set up load balancers with external IPs for service exposure. Integrated multiple Google Cloud APIs: Knowledge Graph API for entity search, Vision API for image analysis (label detection, logo detection, face detection), Speech-to-Text API for audio transcription, Translation API for text translation, and Video Intelligence API for video content analysis. Built a photo upload application using Cloud Storage and Cloud Datastore, storing face detection results with joy scores.

**Tools & Technologies:**
- **Terraform**: Infrastructure as Code (IaC) tool
- **Google Kubernetes Engine (GKE)**: Managed Kubernetes service
- **Kubernetes**: Container orchestration platform
- **kubectl**: Kubernetes command-line tool
- **Docker**: Containerization
- **Google Cloud Load Balancer**: External IP and traffic distribution
- **Google Knowledge Graph API**: Entity search and information retrieval
- **Google Cloud Vision API**: Image analysis (label detection, logo detection, face detection)
- **Google Cloud Speech-to-Text API**: Audio transcription
- **Google Cloud Translation API**: Text translation
- **Google Cloud Video Intelligence API**: Video content analysis
- **Google Cloud Datastore**: NoSQL database
- **Google Cloud Storage**: Object storage
- **Slack API**: Messaging platform integration
- **Python**: Programming language with Google Cloud client libraries

---

### Lab 8: Model Context Protocol (MCP)
**Location:** `notebooks/Labs8/`

**Contents:**
- `Lab8.pdf` - Lab documentation covering MCP server implementation

**What I Did:**
Built Model Context Protocol (MCP) servers using FastMCP to provide tools for LLM agents. Implemented RAG (Retrieval Augmented Generation) systems using LangChain with vector stores (Chroma/FAISS), chunking documents into 10,000-character segments with 1,000-character overlap. Created autonomous agents that use OpenAPI toolkits to interact with REST APIs (like xkcd API). Deployed MCP servers and integrated them with Google Cloud API Gateway. Explored SQL injection vulnerabilities and security practices. Built agents capable of querying databases and composing multiple API calls to answer complex questions.

**Tools & Technologies:**
- **Model Context Protocol (MCP)**: Protocol for LLM-agent tool communication
- **FastMCP**: Python framework for building MCP servers
- **OpenAPI Toolkit**: Tool for interacting with REST APIs via OpenAPI specifications
- **LangChain**: Framework for building LLM applications and agents
- **LangChain Vector Stores**: Document embedding and retrieval (Chroma, FAISS)
- **RecursiveCharacterTextSplitter**: Text chunking for RAG (Retrieval Augmented Generation)
- **Google Cloud APIs**: Integration with various Google Cloud services
- **SQLite**: Local database for MCP server tools
- **xkcd API**: Example REST API integration
- **Google Cloud API Gateway**: API management and routing
- **Python 3**: Server implementation language
- **HTTP/JSON**: Communication protocols for MCP
- **SQL Injection Security**: Database security practices

**Key Topics:**
- MCP server architecture and implementation
- Agentic AI and autonomous agents
- Tool integration for LLM agents
- OpenAPI specification usage

This lab provided the foundation for the final project's MCP server architecture.

---

### Lab 9: Advanced Cloud Topics
**Location:** `notebooks/Labs9/`

**Contents:**
- `Lab_9.pdf` - Lab documentation

**What I Did:**
Implemented Google OAuth 2.0 authentication for web applications, handling OAuth callbacks and user authorization flows. Built a Firebase-based chat application with authentication, Firestore database for messages, Cloud Storage for images, and Cloud Messaging for push notifications. Analyzed large datasets in Google Cloud BigQuery, including COVID-19 data, mobility reports, and health statistics. Created SQL queries to analyze twin births, mask usage, airport traffic impacts, and excess deaths. Generated data visualizations using Python and Jupyter Notebooks to plot trends and relationships in the data.

**Tools & Technologies:**
- **Google OAuth 2.0**: User authentication and authorization
- **Firebase Authentication**: User sign-in services
- **Firebase Firestore**: NoSQL document database
- **Firebase Storage**: File and image storage
- **Firebase Cloud Messaging (FCM)**: Push notifications
- **Google Cloud BigQuery**: Data warehouse and analytics
- **BigQuery SQL**: SQL queries on large datasets
- **Jupyter Notebooks**: Interactive data analysis environment
- **Python**: Data analysis and visualization
- **Matplotlib / Plotting Libraries**: Data visualization
- **Public Datasets**: COVID-19, mobility, and health data analysis
- **JavaScript**: Frontend Firebase integration
- **HTML/CSS**: Web application interface

---

### Lab 10: Final Lab Assignment
**Location:** `notebooks/Labs10/`

**Contents:**
- `Lab_10.pdf` - Lab documentation

**What I Did:**
Built Apache Beam data processing pipelines for distributed computing, implementing MapReduce operations to analyze Java package imports and word frequency in literary texts (King Lear). Deployed pipelines to Google Cloud Dataflow, processing data in parallel and analyzing job performance metrics. Used Terraform to provision multi-region VPC networks with 5 subnets and 5 VM instances across different availability zones. Configured load balancers for traffic distribution and measured network latency between regions using iperf3. Performed deep network protocol analysis using Wireshark, capturing and analyzing ARP, DNS, TCP handshake, and HTTP packet flows. Used dig for DNS queries and explored IP geolocation services to map IP addresses to geographic locations.

**Tools & Technologies:**
- **Apache Beam**: Unified programming model for batch and streaming data processing
- **Google Cloud Dataflow**: Managed Beam execution service
- **Python**: Beam pipeline programming
- **MapReduce Operations**: Map, Shuffle-Reduce, Reduce transformations
- **Google Cloud Storage**: Input/output data storage
- **Unix Command-Line Tools**: `wc`, `sort`, `head` for text processing
- **Google Cloud Load Balancer**: Traffic distribution across regions
- **Terraform**: Infrastructure as Code for network provisioning
- **Google Cloud VPC**: Multi-region network configuration
- **Google Compute Engine**: VM instances across multiple availability zones
- **iperf3**: Network latency measurement
- **Wireshark**: Network packet capture and analysis
- **dig**: DNS query tool
- **ipinfo.io / DB-IP**: IP geolocation services
- **ARP Protocol**: Address resolution analysis
- **TCP/IP Protocol Stack**: Network protocol analysis (DNS, TCP, HTTP)

---

## 🎯 Final Project: Retail Intelligence Platform

**Location:** `final/`

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
**Location:** `final/client/`

- **CrewAI Framework**: Orchestrates multiple autonomous agents
- **Specialized Agents**: Each agent focuses on a specific domain of retail analysis
- **MCP Client**: Communicates with the remote MCP server on Cloud Run
- **LLM Integration**: Uses OpenAI's GPT models for agent reasoning

#### Server-Side (Cloud Run)
**Location:** `final/server/`

- **FastMCP Server**: Implements Model Context Protocol standard
- **API Tools**: Five integrated tools providing access to external data sources
- **Containerized Deployment**: Docker container running on Google Cloud Run

### Agent System

The platform consists of **6 specialized agents**:

1. **Project Analysis Coordinator (Orchestrator)** - Coordinates all specialist agents and synthesizes reports
2. **Operations & Supply Chain Analyst** - Analyzes operational feasibility and supply chain complexity
3. **Customer Analytics & Marketing Specialist** - Analyzes customer demographics and marketing potential
4. **Financial & Sales Performance Analyst** - Assesses financial viability and sales projections
5. **Market Intelligence & Research Analyst** - Evaluates market trends and competitive positioning
6. **Product & E-commerce Specialist** - Develops product strategy and e-commerce performance analysis

### MCP Tools Available

All agents have access to these 5 MCP tools via the Cloud Run server:

1. **BigQuery Tool**: Execute SQL queries against `bigquery-public-data` datasets
2. **REST Countries Tool**: Retrieve country/region data for geographic analysis
3. **Alpha Vantage Tool**: Retrieve financial market data and stock information
4. **FRED Tool**: Retrieve macroeconomic indicators from the Federal Reserve
5. **Fake Store Tool**: Retrieve product data for portfolio and pricing analysis

### Technology Stack

**Client** (`final/client/`):
- Python 3.10+
- CrewAI, LangChain, OpenAI API
- python-dotenv

**Server** (`final/server/`):
- Python 3.10
- FastMCP, Google Cloud BigQuery
- Docker, Google Cloud Run

### Quick Start

**Client Setup:**
```bash
cd final/client
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Create .env file with OPENAI_API_KEY and MCP_SERVER_URL
python client.py
```

**Server Deployment:**
```bash
cd final/server
# Configure Google Cloud credentials
./rebuild_and_deploy.sh
```

### Documentation

- **Agent Documentation**: `final/agents_documentation.md` - Detailed agent specifications
- **Project Instructions**: `final/final_instructions.txt` - Original project requirements
- **Example Projects**: `final/retail_project_descriptions.txt` - Sample retail project descriptions

### File Structure

```
final/
├── client/                    # Client-side agent system
│   ├── client.py              # Main entry point
│   ├── mcp_client.py          # MCP client implementation
│   ├── orchestrator.py       # Orchestrator agent
│   └── agents/                # Specialist agents
│       ├── operations_agent.py
│       ├── customer_analytics_agent.py
│       ├── financial_agent.py
│       ├── market_intelligence_agent.py
│       ├── product_ecommerce_agent.py
│       └── tools.py
│
├── server/                     # MCP server (Cloud Run)
│   ├── server.py              # MCP server implementation
│   ├── Dockerfile             # Container definition
│   ├── rebuild_and_deploy.sh  # Deployment script
│   └── tools/                 # API tool implementations
│       ├── bigquery.py
│       ├── rest_countries.py
│       ├── alpha_vantage.py
│       ├── fred.py
│       └── fake_store.py
│
└── [documentation files]
```

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

### Security Notes

- **API Keys**: Never commit API keys to the repository. Use environment variables or Google Cloud Secrets Manager
- **`.env` Files**: All `.env` files are gitignored. Create local `.env` files for development
- **Cloud Run**: Server can be configured with authentication if needed

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
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📊 Project Status

✅ **Final Project**: Complete and deployed  
✅ **Homework Assignments**: All completed (hw1-hw4)  
✅ **Labs**: Completed and documented (Labs 1-10)  

---

*Last Updated: December 2024*
