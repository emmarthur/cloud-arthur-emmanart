"""
Orchestrator Agent: Coordinates specialized agents for comprehensive retail project analysis.

This orchestrator agent coordinates multiple specialist agents, each operating autonomously
with their own tools. The orchestrator synthesizes results from all agents into a unified report.

Reference: Lab 8 - Agentic AI pattern where agents operate autonomously in loops, producing
plans, executing tools, and viewing results. The orchestrator coordinates multiple such agents.
"""
from crewai import Agent
from langchain_openai import ChatOpenAI

def create_orchestrator_agent(llm: ChatOpenAI) -> Agent:
    """Create orchestrator agent that coordinates specialist agents and synthesizes reports.
    
    The orchestrator coordinates multiple autonomous agents, each with access to MCP tools.
    It synthesizes their analyses into a comprehensive report.
    
    Args:
        llm: Language model instance for the agent
        
    Returns:
        Configured Agent instance
    """
    return Agent(
        role="Project Analysis Coordinator",
        goal="Coordinate specialized agents to provide comprehensive retail project analysis by determining which areas are relevant, assigning tasks to appropriate agents, and synthesizing results into a unified report",
        backstory="""You are an experienced retail project analyst and coordinator with expertise across all
        retail domains. Your role is to understand retail project descriptions, determine which specialized
        areas of analysis are relevant (operations, customer analytics, financial, market intelligence, product),
        and coordinate a team of specialist agents to gather comprehensive insights. You intelligently reason
        about which APIs and data sources each specialist agent should use, assign appropriate tasks, and then
        synthesize all the specialized analyses into one comprehensive report that demonstrates the project's
        usefulness and impact across all relevant retail areas. You also simulate the impact on an example
        company to demonstrate real-world implications.""",
        llm=llm,
        verbose=True,
        allow_delegation=False  # Tasks explicitly assigned, no delegation needed
    )

