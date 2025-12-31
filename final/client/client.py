"""
Main client entry point for retail project analysis using CrewAI agents.

Agentic AI Implementation:
This system implements autonomous agents that operate in a loop: they produce plans,
execute them using tools, and view results. When they have sufficient information to
answer a query, they return it and terminate. Agents are configured with a set of tools
(MCP tools) that they can use to perform execution.

Reference: Lab 8 - "Another common application for LLMs is to construct autonomous agents.
Based on a user's query, such agents are able to operate in a loop in which they produce
their own plans, execute them, and view the results of execution. When they have sufficient
information to answer a particular query, they return it to the user and terminate. Agents
are typically configured with a set of tools that they can use to perform the execution."

Coordinates specialized agents to analyze retail projects via MCP server on Cloud Run.
"""
import os
import sys
import signal
import atexit

# Windows compatibility fix: Add missing Unix signal constants that crewai expects
# These signals don't exist on Windows, so we add dummy values to prevent AttributeError
if sys.platform == 'win32':
    # Common Unix signals that crewai might use
    unix_signals = {
        'SIGHUP': 1,
        'SIGINT': 2,
        'SIGQUIT': 3,
        'SIGILL': 4,
        'SIGTRAP': 5,
        'SIGABRT': 6,
        'SIGBUS': 7,
        'SIGFPE': 8,
        'SIGKILL': 9,
        'SIGUSR1': 10,
        'SIGSEGV': 11,
        'SIGUSR2': 12,
        'SIGPIPE': 13,
        'SIGALRM': 14,
        'SIGTERM': 15,
        'SIGSTKFLT': 16,
        'SIGCHLD': 17,
        'SIGCONT': 18,
        'SIGSTOP': 19,
        'SIGTSTP': 20,
        'SIGTTIN': 21,
        'SIGTTOU': 22,
        'SIGURG': 23,
        'SIGXCPU': 24,
        'SIGXFSZ': 25,
        'SIGVTALRM': 26,
        'SIGPROF': 27,
        'SIGWINCH': 28,
        'SIGIO': 29,
        'SIGPWR': 30,
        'SIGSYS': 31,
    }
    for sig_name, sig_value in unix_signals.items():
        if not hasattr(signal, sig_name):
            setattr(signal, sig_name, sig_value)

from dotenv import load_dotenv
from crewai import Crew, Task
from langchain_openai import ChatOpenAI

# Import agent factory functions
from orchestrator import create_orchestrator_agent
from agents.operations_agent import create_operations_agent
from agents.customer_analytics_agent import create_customer_analytics_agent
from agents.financial_agent import create_financial_agent
from agents.market_intelligence_agent import create_market_intelligence_agent
from agents.product_ecommerce_agent import create_product_ecommerce_agent
from metrics import start_analysis_session, end_analysis_session, save_metrics_to_file

load_dotenv()

# Initialize LLM (OpenAI by default, requires OPENAI_API_KEY in .env)
# Reference: Lab 8 - LLM setup with API key and model configuration
llm = ChatOpenAI(
    model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.7
)


def analyze_retail_project(project_description: str) -> str:
    """Analyze retail project using CrewAI agents and MCP server tools.
    
    Args:
        project_description: Description of the retail project to analyze
        
    Returns:
        Comprehensive analysis report combining insights from all specialist agents
    """
    # Start tracking analysis session
    session_id = start_analysis_session(project_description)
    
    # Set project name for logging (truncate to 100 chars)
    from agents.tools import set_project_name
    project_name = project_description[:100] + "..." if len(project_description) > 100 else project_description
    set_project_name(project_name)
    
    # Create all specialist agents
    orchestrator = create_orchestrator_agent(llm)
    operations_agent = create_operations_agent(llm)
    customer_agent = create_customer_analytics_agent(llm)
    financial_agent = create_financial_agent(llm)
    market_agent = create_market_intelligence_agent(llm)
    product_agent = create_product_ecommerce_agent(llm)
    
    # Create tasks for each specialist agent
    operations_task = Task(
        description=f"""Analyze the operations and supply chain aspects of this retail project:
        {project_description}
        
        IMPORTANT: 
        - You MUST use at least ONE tool to gather data before providing your analysis.
        - Call each tool SEPARATELY, one at a time. Do NOT try to call multiple tools in a single action.
        - Wait for each tool's response before calling the next tool.
        
        You have access to all tools. Use the appropriate tools to gather data:
        - REST Countries Tool: For geographic and logistics data (provide country or region names as strings)
        - BigQuery Tool: For demographic and population data (construct SQL queries for bigquery-public-data datasets)
        - FRED Tool: For economic indicators affecting supply chains (provide FRED series IDs like 'GDP', 'UNRATE')
        - Alpha Vantage Tool: For market conditions and retail sector performance. Intelligently determine relevant stock symbols based on the project type (e.g., 'WMT' for grocery, 'AMZN' for e-commerce, 'HD' for home improvement, 'TGT' for general retail) or call with stock_symbol="" for general indicators
        - Fake Store Tool: For product data if relevant to operations (provide category name or leave empty for all)
        
        Then provide a DETAILED, COMPREHENSIVE analysis report that includes:
        - Operational feasibility assessment with specific metrics and data points
        - Supply chain complexity analysis with regional breakdowns
        - Location-specific operational considerations with concrete examples
        - Impact on operations and supply chain with quantitative insights
        
        IMPORTANT: You must provide a FULL, DETAILED report (at least 300-500 words) with specific data points,
        metrics, and insights from the tool data you gather. Do NOT provide just a summary.
        Format your analysis as a clear, structured report with sections and subsections.""",
        agent=operations_agent,
        expected_output="A comprehensive, detailed operations and supply chain analysis report (300-500+ words) with specific data points and metrics"
    )
    
    customer_task = Task(
        description=f"""Analyze the customer analytics and marketing aspects of this retail project:
        {project_description}
        
        IMPORTANT: 
        - You MUST use at least ONE tool to gather data before providing your analysis.
        - Call each tool SEPARATELY, one at a time. Do NOT try to call multiple tools in a single action.
        - Wait for each tool's response before calling the next tool.
        
        You have access to all tools. Use the appropriate tools to gather data:
        - BigQuery Tool: For customer demographics and geographic distribution (construct SQL queries for bigquery-public-data datasets)
        - REST Countries Tool: For geographic and market size information (provide country or region names as strings)
        - FRED Tool: For economic indicators affecting customer spending (provide FRED series IDs like 'GDP', 'UNRATE', 'CPIAUCSL')
        - Alpha Vantage Tool: For market conditions and consumer confidence. Intelligently select relevant stock symbols based on project type (e.g., 'WMT', 'TGT', 'AMZN') or call with stock_symbol="" for general market indicators
        - Fake Store Tool: For product preferences and pricing insights (provide category name or leave empty for all)
        
        Then provide a DETAILED, COMPREHENSIVE analysis report that includes:
        - Customer segmentation and demographics with specific population data and percentages
        - Marketing potential and effectiveness with market size metrics
        - Customer impact and engagement opportunities with actionable strategies
        - Geographic customer distribution with regional breakdowns
        
        IMPORTANT: 
        - When calling tools, include your role name "Customer Analytics & Marketing Specialist" in the agent_name parameter
        - You must provide a FULL, DETAILED report (at least 300-500 words) with specific data points,
        metrics, and insights from the tool data you gather. Do NOT provide just a summary.
        Format your analysis as a clear, structured report with sections and subsections.""",
        agent=customer_agent,
        expected_output="A comprehensive, detailed customer analytics and marketing analysis report (300-500+ words) with specific data points and metrics"
    )
    
    financial_task = Task(
        description=f"""Analyze the financial and sales performance aspects of this retail project:
        {project_description}
        
        IMPORTANT: 
        - You MUST use at least ONE tool to gather data before providing your analysis.
        - Call each tool SEPARATELY, one at a time. Do NOT try to call multiple tools in a single action.
        - Wait for each tool's response before calling the next tool.
        
        You have access to all tools. Use the appropriate tools to gather data:
        - Alpha Vantage Tool: For market conditions and retail sector performance. Intelligently determine relevant stock symbols based on the project type (e.g., 'WMT' for grocery, 'TGT' for general retail, 'AMZN' for e-commerce) or call with stock_symbol="" for general indicators
        - FRED Tool: For macroeconomic indicators affecting financial performance (provide FRED series IDs like 'GDP', 'UNRATE', 'RETAIL_SALES')
        - BigQuery Tool: For demographic data affecting market size and revenue potential (construct SQL queries)
        - REST Countries Tool: For market size and population data (provide country or region names as strings)
        - Fake Store Tool: For pricing strategies and revenue insights (provide category name or leave empty)
        
        Then provide a DETAILED, COMPREHENSIVE analysis report that includes:
        - Financial viability and profitability with specific calculations and projections
        - Sales performance projections with revenue forecasts and growth estimates
        - Financial impact and ROI potential with quantitative analysis
        - Market conditions affecting financial performance with economic indicators
        
        IMPORTANT: 
        - When calling tools, include your role name "Financial & Sales Performance Analyst" in the agent_name parameter
        - You must provide a FULL, DETAILED report (at least 300-500 words) with specific data points,
        metrics, calculations, and insights from the tool data you gather. Do NOT provide just a summary.
        Format your analysis as a clear, structured report with sections and subsections.""",
        agent=financial_agent,
        expected_output="A comprehensive, detailed financial and sales performance analysis report (300-500+ words) with specific calculations and metrics"
    )
    
    market_task = Task(
        description=f"""Analyze the market intelligence and research aspects of this retail project:
        {project_description}
        
        IMPORTANT: 
        - You MUST use at least ONE tool to gather data before providing your analysis.
        - Call each tool SEPARATELY, one at a time. Do NOT try to call multiple tools in a single action.
        - Wait for each tool's response before calling the next tool.
        
        You have access to all tools. Use the appropriate tools to gather data:
        - FRED Tool: For macroeconomic indicators and market trends (provide FRED series IDs like 'GDP', 'UNRATE', 'CPIAUCSL', 'RETAIL_SALES')
        - Alpha Vantage Tool: For market conditions and industry performance. Intelligently select relevant stock symbols based on project type or call with stock_symbol="" for general market indicators
        - BigQuery Tool: For demographic and market size data (construct SQL queries)
        - REST Countries Tool: For geographic market information (provide country or region names as strings)
        - Fake Store Tool: For product trends and competitive insights (provide category name or leave empty)
        
        Then provide a DETAILED, COMPREHENSIVE analysis report that includes:
        - Market trends and industry dynamics with specific economic indicators and data
        - Competitive positioning with market share insights and differentiation strategies
        - Market viability and opportunities with quantitative market size analysis
        - Long-term macroeconomic factors with GDP, unemployment, and inflation data
        
        IMPORTANT: 
        - When calling tools, include your role name "Market Intelligence & Research Analyst" in the agent_name parameter
        - You must provide a FULL, DETAILED report (at least 300-500 words) with specific data points,
        metrics, and insights from the tool data you gather. Do NOT provide just a summary.
        Format your analysis as a clear, structured report with sections and subsections.""",
        agent=market_agent,
        expected_output="A comprehensive, detailed market intelligence and research analysis report (300-500+ words) with specific data points and metrics"
    )
    
    product_task = Task(
        description=f"""Analyze the product and e-commerce aspects of this retail project:
        {project_description}
        
        IMPORTANT: 
        - You MUST use at least ONE tool to gather data before providing your analysis.
        - Call each tool SEPARATELY, one at a time. Do NOT try to call multiple tools in a single action.
        - Wait for each tool's response before calling the next tool.
        
        You have access to all tools. Use the appropriate tools to gather data:
        - Fake Store Tool: For product portfolio data and pricing strategies (provide category name like 'electronics', 'jewelery', 'men's clothing', 'women's clothing' or leave empty for all)
        - BigQuery Tool: For demographic data affecting product preferences (construct SQL queries)
        - REST Countries Tool: For regional product preferences and market size (provide country or region names as strings)
        - FRED Tool: For economic conditions affecting product demand (provide FRED series IDs)
        - Alpha Vantage Tool: For market conditions affecting e-commerce performance. Intelligently select relevant stock symbols (e.g., 'AMZN' for e-commerce, 'WMT' for retail) or call with stock_symbol="" for general indicators
        
        Then provide a DETAILED, COMPREHENSIVE analysis report that includes:
        - Product strategy and assortment planning with specific product categories and pricing data
        - E-commerce performance potential with conversion metrics and online sales projections
        - Pricing strategies with price distribution analysis and competitive positioning
        - Omnichannel integration opportunities with specific implementation recommendations
        
        IMPORTANT: 
        - When calling tools, include your role name "Product & E-commerce Specialist" in the agent_name parameter
        - You must provide a FULL, DETAILED report (at least 300-500 words) with specific data points,
        metrics, and insights from the tool data you gather. Do NOT provide just a summary.
        Format your analysis as a clear, structured report with sections and subsections.""",
        agent=product_agent,
        expected_output="A comprehensive, detailed product and e-commerce analysis report (300-500+ words) with specific data points and metrics"
    )
    
    # Orchestrator task: synthesize all analyses
    orchestrator_task = Task(
        description=f"""You are coordinating the analysis of this retail project:
        {project_description}
        
        Review the analyses provided by the specialist agents. You will receive:
        - Operations & Supply Chain analysis from the Operations & Supply Chain Analyst
        - Customer Analytics & Marketing analysis from the Customer Analytics & Marketing Specialist
        - Financial & Sales Performance analysis from the Financial & Sales Performance Analyst
        - Market Intelligence & Research analysis from the Market Intelligence & Research Analyst
        - Product & E-commerce analysis from the Product & E-commerce Specialist
        
        Synthesize all these analyses into one comprehensive report that:
        1. Summarizes the project's usefulness and impact across all relevant areas
        2. Highlights key insights from each specialized area
        3. Identifies synergies and cross-area considerations
        4. Simulates the impact on an example retail company
        5. Provides actionable recommendations
        
        Format the final report clearly with sections for each area and an overall summary.""",
        agent=orchestrator,
        context=[
            operations_task,
            customer_task,
            financial_task,
            market_task,
            product_task
        ],
        expected_output="A comprehensive retail project analysis report combining all specialized areas"
    )
    
    # Create and execute crew with all agents and tasks
    # CrewAI orchestrates multiple agents working together on tasks
    # Each agent operates autonomously: produces plans, executes via tools, views results
    # Reference: Lab 8 - Agentic AI pattern where agents operate in loops with tool execution
    crew = Crew(
        agents=[
            orchestrator,
            operations_agent,
            customer_agent,
            financial_agent,
            market_agent,
            product_agent
        ],
        tasks=[
            operations_task,
            customer_task,
            financial_task,
            market_task,
            product_task,
            orchestrator_task
        ],
        verbose=True
    )
    
    # Execute crew: agents will autonomously plan, execute tools (MCP calls), and synthesize results
    try:
        result = crew.kickoff()
        analysis_success = True
    except Exception as e:
        analysis_success = False
        result = f"Error during analysis: {str(e)}"
    
    # End tracking analysis session
    end_analysis_session(session_id, analysis_success)
    
    # Save metrics to file
    save_metrics_to_file()
    
    # Extract comprehensive report from CrewOutput object
    # CrewAI returns CrewOutput with multiple ways to access results
    try:
        # Try orchestrator task output (last task = orchestrator)
        if hasattr(result, 'tasks_output') and result.tasks_output:
            orchestrator_output = result.tasks_output[-1]
            if hasattr(orchestrator_output, 'raw'):
                return orchestrator_output.raw
            elif hasattr(orchestrator_output, 'output'):
                return orchestrator_output.output
            else:
                return str(orchestrator_output)
        # Try direct raw attribute access
        elif hasattr(result, 'raw'):
            return result.raw
        # Fallback: convert to string, try to get more details if too short
        else:
            result_str = str(result)
            if len(result_str) < 200 and hasattr(result, 'tasks_output'):
                # Collect all task outputs if summary is too short
                all_outputs = []
                for task_output in result.tasks_output:
                    if hasattr(task_output, 'raw'):
                        all_outputs.append(task_output.raw)
                    elif hasattr(task_output, 'output'):
                        all_outputs.append(task_output.output)
                if all_outputs:
                    return "\n\n".join(all_outputs)
            return result_str
    except Exception as e:
        # Final fallback: return string representation
        return str(result)


def cleanup_and_exit(exit_code=0):
    """Clean up resources and exit cleanly."""
    import asyncio
    import threading
    
    # Close any remaining asyncio event loops
    try:
        # Try to get the current event loop
        try:
            loop = asyncio.get_running_loop()
            # Can't close a running loop, but we'll let it finish
        except RuntimeError:
            # No running loop, try to get and close any existing loop
            try:
                loop = asyncio.get_event_loop()
                if not loop.is_closed():
                    loop.close()
            except:
                pass
    except:
        pass
    
    # Force exit to bypass any hanging threads/processes
    # This is necessary because CrewAI may leave background threads running
    print("\n" + "=" * 70)
    print("Exiting...")
    print("=" * 70)
    
    # Use os._exit to force immediate termination, bypassing cleanup handlers
    # This prevents hanging on CrewAI's background threads
    os._exit(exit_code)


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\n" + "=" * 70)
    print("Interrupted by user (Ctrl+C)")
    print("=" * 70)
    cleanup_and_exit(0)


# Register signal handlers for clean exit
if sys.platform != 'win32':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

# Register cleanup function
atexit.register(lambda: print("\n[Cleanup] Exiting..."))


if __name__ == "__main__":
    try:
        print("=" * 70)
        print("Retail Project Analysis System")
        print("=" * 70)
        print("\nThis system uses CrewAI agents to analyze retail projects.")
        print("Specialist agents gather data from the MCP server on Cloud Run.")
        print("The orchestrator coordinates and synthesizes all analyses.")
        print("\nPress Ctrl+C at any time to exit.\n")
        
        # Example usage
        try:
            project_description = input("Enter your retail project description: ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nNo input provided. Exiting.")
            cleanup_and_exit(0)
        
        if project_description.strip():
            print("\n" + "=" * 70)
            print("Analyzing project...")
            print("=" * 70 + "\n")
            
            result = analyze_retail_project(project_description)
            
            print("\n" + "=" * 70)
            print("Analysis Complete")
            print("=" * 70)
            
            # Extract and print the full report
            if hasattr(result, 'raw'):
                print(result.raw)
            elif hasattr(result, 'tasks_output') and result.tasks_output:
                # Get the orchestrator task output (last task)
                orchestrator_output = result.tasks_output[-1]
                if hasattr(orchestrator_output, 'raw'):
                    print(orchestrator_output.raw)
                elif hasattr(orchestrator_output, 'output'):
                    print(orchestrator_output.output)
                else:
                    print(str(orchestrator_output))
            else:
                # Print the string representation
                result_str = str(result)
                print(result_str)
                
                # If it's too short, try to get more details
                if len(result_str) < 500:
                    print("\n[NOTE] Report seems truncated. Full details may be in verbose output above.")
            
            print("\n" + "=" * 70)
            print("Analysis finished. Exiting...")
            print("=" * 70)
        else:
            print("No project description provided. Exiting.")
        
        # Force immediate exit to prevent hanging on CrewAI threads
        # Use os._exit instead of cleanup_and_exit to bypass any hanging threads
        print("\n" + "=" * 70)
        print("Exiting...")
        print("=" * 70)
        os._exit(0)
        
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Interrupted by user (Ctrl+C)")
        print("=" * 70)
        os._exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        os._exit(1)
