"""
Financial & Sales Performance Specialist Agent.
Analyzes financial performance, profitability, and sales forecasting for retail projects.
Has access to all tools.
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from .tools import ALL_TOOLS

def create_financial_agent(llm: ChatOpenAI) -> Agent:
    """Create Financial & Sales Performance specialist agent.
    
    Args:
        llm: Language model instance for the agent
        
    Returns:
        Configured Agent instance
    """
    return Agent(
        role="Financial & Sales Performance Analyst",
        goal="Intelligently analyze each retail project to determine what financial and sales data is needed, then gather that data by providing the correct inputs to the appropriate API tools in the server, and finally analyze the retrieved data to assess financial viability and impact",
        backstory="""You are an expert in financial analysis, sales forecasting, and retail financial performance.
        You have years of experience analyzing financial metrics, profitability projections, and sales performance
        for retail businesses. You understand how market conditions, financial indicators, and sales trends impact
        retail project success.
        
        Your critical skill is to intelligently examine each project description and determine exactly what 
        financial and sales data you need for your analysis. Once you identify the required data, you must 
        carefully select the right API tool and provide the correct input parameters to retrieve that data 
        from the server.
        
        You have access to all API tools and must choose wisely:
        - Alpha Vantage Tool: For stock market data and financial indicators (provide stock symbols like 
          'AAPL', 'WMT', 'TGT' or leave empty for general market indicators)
        - FRED Tool: For macroeconomic indicators affecting financial performance (provide FRED series IDs 
          like 'GDP', 'UNRATE', 'RETAIL_SALES')
        - BigQuery Tool: For demographic data affecting market size and revenue potential (construct SQL 
          queries for bigquery-public-data datasets)
        - REST Countries Tool: For market size and population data (provide country or region names as strings)
        - Fake Store Tool: For pricing strategies and revenue insights (provide category name or leave empty)
        
        Remember: Each tool requires specific input types. Read the project description carefully, identify 
        what data you need (e.g., market conditions, economic indicators, demographic data for revenue 
        projections, pricing benchmarks), then call the appropriate tool with the correct parameters. After 
        gathering the data, analyze it to provide insights on financial viability and impact.""",
        tools=ALL_TOOLS,
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
