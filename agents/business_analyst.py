"""
Business Analyst Agent

Responsible for:
- Analyzing client requirements
- Creating user stories and functional specifications
- Defining project scope and features
- Market research and competitive analysis
- Wireframing and UX considerations
"""

from crewai import Agent
from typing import List, Optional


def create_business_analyst_agent(tools: Optional[List] = None, verbose: bool = True, llm = None, model_name: Optional[str] = None) -> Agent:
    """
    Create a Business Analyst agent specialized in understanding
    client needs and translating them into technical requirements.
    
    Args:
        tools: List of tools available to the agent
        verbose: Whether to show detailed output
        llm: Language model to use (if provided, model_name is ignored)
        model_name: Specific model to use (e.g., 'claude-4.5-sonnet', 'gpt-5.1')
        
    Returns:
        Agent: Configured Business Analyst agent
    """
    # If no LLM provided, configure CrewAI LLM with GitHub Models endpoint
    if llm is None:
        from utils.llm_config import get_best_model_for_agent, GITHUB_MODELS, get_max_tokens_for_model
        from crewai import LLM
        import os
        
        # Get the recommended model for this agent
        model_key = model_name or get_best_model_for_agent('business_analyst')
        model_id = GITHUB_MODELS.get(model_key, model_key) if model_key else "gpt-4.1"
        
        # Create CrewAI LLM with GitHub Models endpoint
        llm_config = {
            "model": model_id,
            "base_url": "https://models.inference.ai.azure.com",
            "api_key": os.getenv("GITHUB_TOKEN"),
            "max_tokens": get_max_tokens_for_model(model_id),
        }
        
        # Only add temperature if not an o-series model
        if model_id not in ["o1", "o1-mini", "o1-preview", "o3", "o3-mini", "o4-mini"]:
            llm_config["temperature"] = 0.7
        
        llm = LLM(**llm_config)

    
    agent_config = {
        'role': 'Business Analyst',
        'goal': 'Understand client needs and translate them into clear, actionable technical requirements for small and medium-sized businesses',
        'backstory': """You are an experienced Business Analyst with over 10 years of experience 
        working with small and medium-sized enterprises (SMEs/PyMEs). You have a deep understanding 
        of common business needs in sectors like retail, services, and hospitality.
        
        You excel at:
        - Conducting stakeholder interviews
        - Identifying core business problems
        - Creating user stories and acceptance criteria
        - Prioritizing features based on business value
        - Understanding budget constraints of SMEs
        - Recommending cost-effective solutions
        
        You communicate in clear, non-technical language when talking to clients,
        but provide detailed technical specifications for the development team.
        
        You always consider:
        - Scalability for future growth
        - Budget constraints
        - Time to market
        - User experience
        - Competitive advantages""",
        'tools': tools or [],
        'verbose': verbose,
        'allow_delegation': False,
        'max_iter': 15,
        'memory': False,  # Disabled to reduce token usage - agent gets context via task description
        'llm': llm,  # Always set LLM (created above if not provided)
    }
    
    return Agent(**agent_config)


def create_requirements_task_description(project_name: str, project_type: str, client_description: str) -> str:
    """
    Generate a task description for requirements gathering.
    
    Args:
        project_name: Name of the project
        project_type: Type (ecommerce, landing, dashboard, api)
        client_description: Client's description of their needs
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Analyze the following project requirements and create a comprehensive requirements document:
    
    PROJECT NAME: {project_name}
    PROJECT TYPE: {project_type}
    
    CLIENT DESCRIPTION:
    {client_description}
    
    Your deliverable should include:
    
    1. EXECUTIVE SUMMARY
       - Business objective
       - Target audience
       - Success metrics
    
    2. FUNCTIONAL REQUIREMENTS
       - Must-have features (MVP)
       - Nice-to-have features (Phase 2)
       - User roles and permissions
    
    3. USER STORIES
       - At least 5-10 main user stories
       - Acceptance criteria for each
       - Priority level (High/Medium/Low)
    
    4. TECHNICAL CONSIDERATIONS
       - Recommended tech stack
       - Third-party integrations needed
       - Security requirements
       - Performance requirements
    
    5. PROJECT SCOPE
       - What's included in MVP
       - What's excluded
       - Timeline estimation
       - Budget considerations
    
    6. WIREFRAME RECOMMENDATIONS
       - Key pages/screens needed
       - Navigation flow
       - Important UI/UX considerations
    
    Format the output in clear Markdown with proper sections and bullet points.
    """


def create_user_stories_task_description(requirements: str) -> str:
    """
    Generate a task description for creating detailed user stories.
    
    Args:
        requirements: Previously gathered requirements
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Based on the following requirements, create detailed user stories:
    
    {requirements}
    
    For each user story, provide:
    
    1. USER STORY FORMAT:
       As a [user role]
       I want to [action]
       So that [benefit]
    
    2. ACCEPTANCE CRITERIA:
       - Given [context]
       - When [action]
       - Then [expected result]
    
    3. TECHNICAL NOTES:
       - API endpoints needed
       - Database tables/models
       - Frontend components
    
    4. PRIORITY:
       - Must Have (MVP)
       - Should Have (Phase 2)
       - Nice to Have (Future)
    
    5. ESTIMATION:
       - Story points or hours
       - Dependencies
    
    Create at least 10-15 comprehensive user stories covering all main features.
    """
