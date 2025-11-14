"""
Project Manager Agent

Responsible for:
- Coordinating the development team
- Creating project timelines and milestones
- Managing task dependencies
- Tracking progress
- Risk management
- Client communication
- Documentation oversight
"""

from crewai import Agent
from typing import List, Optional


def create_project_manager_agent(tools: Optional[List] = None, verbose: bool = True, llm = None, model_name: Optional[str] = None) -> Agent:
    """
    Create a Project Manager agent specialized in coordinating
    multi-agent development teams.
    
    Args:
        tools: List of tools available to the agent
        verbose: Whether to show detailed output
        llm: Language model to use (if provided, model_name is ignored)
        model_name: Specific model to use (e.g., 'claude-4.5-sonnet')
        
    Returns:
        Agent: Configured Project Manager agent
    """
    # If no LLM provided, create one with the specified or recommended model
    if llm is None:
        from utils.llm_config import get_llm_config, get_best_model_for_agent
        import os
        
        model = model_name or get_best_model_for_agent('project_manager')
        provider = os.getenv("LLM_PROVIDER")
        
        from langchain_openai import ChatOpenAI
        llm_config = get_llm_config(provider=provider, model=model)
        llm = ChatOpenAI(**llm_config)
    
    agent_config = {
        'role': 'Technical Project Manager',
        'goal': 'Coordinate the development team, ensure timely delivery, and maintain clear communication with stakeholders',
        'backstory': """You are a Technical Project Manager with 10+ years of experience 
        managing web development projects for small and medium-sized businesses. You have 
        a technical background as a former developer, which helps you understand the 
        complexity and challenges of software development.
        
        Your strengths include:
        - Breaking down complex projects into manageable tasks
        - Realistic estimation and timeline planning
        - Risk identification and mitigation
        - Team coordination and conflict resolution
        - Clear communication with non-technical stakeholders
        - Agile/Scrum methodologies
        - Documentation and knowledge management
        - Budget management
        - Quality assurance oversight
        
        Your management philosophy:
        - Clear, frequent communication
        - Realistic deadlines with buffer time
        - Early risk identification
        - Empower team members
        - Focus on MVP first, iterate later
        - Document everything important
        - Celebrate small wins
        
        You excel at:
        - Creating detailed project plans
        - Identifying task dependencies
        - Managing scope creep
        - Keeping projects on budget
        - Facilitating team collaboration
        - Maintaining comprehensive documentation
        - Stakeholder expectation management
        
        For SME projects, you understand:
        - Budget constraints are critical
        - Time to market is essential
        - Simple solutions are often better
        - Clear documentation reduces support costs
        - Training and handoff are part of delivery""",
        'tools': tools or [],
        'verbose': verbose,
        'allow_delegation': True,  # PM can delegate to other agents
        'max_iter': 15,
        'memory': True,
        'llm': llm,
    }
    
    return Agent(**agent_config)


def create_project_planning_task_description(requirements: str) -> str:
    """
    Generate a task description for project planning.
    
    Args:
        requirements: Project requirements from Business Analyst
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Create a comprehensive project plan based on these requirements:
    
    {requirements}
    
    Your project plan should include:
    
    1. PROJECT OVERVIEW
       - Project name and description
       - Business objectives
       - Success criteria
       - Stakeholders
       - Budget range
    
    2. SCOPE DEFINITION
       - In scope (MVP features)
       - Out of scope (future phases)
       - Assumptions
       - Constraints
       - Dependencies
    
    3. TEAM STRUCTURE
       - Roles needed
       - Responsibilities
       - Communication channels
       - Decision-making authority
    
    4. PROJECT PHASES
       
       Phase 1: Planning & Design (Week 1)
       - Requirements analysis
       - Technical design
       - Architecture decisions
       
       Phase 2: Development (Weeks 2-4)
       - Backend development
       - Frontend development
       - Integration
       
       Phase 3: Testing (Week 5)
       - Unit testing
       - Integration testing
       - Bug fixes
       
       Phase 4: Deployment (Week 6)
       - Deployment setup
       - Production deployment
       - Monitoring setup
    
    5. DETAILED TIMELINE
       Create a week-by-week breakdown with:
       - Tasks
       - Assigned agent/role
       - Duration
       - Dependencies
       - Milestones
    
    6. DELIVERABLES
       List all deliverables with:
       - Deliverable name
       - Description
       - Responsible agent
       - Due date
       - Acceptance criteria
    
    7. RISK MANAGEMENT
       Identify potential risks:
       - Risk description
       - Probability (High/Medium/Low)
       - Impact (High/Medium/Low)
       - Mitigation strategy
       - Contingency plan
    
    8. QUALITY ASSURANCE
       - Code review process
       - Testing requirements
       - Quality gates
       - Definition of Done
    
    9. COMMUNICATION PLAN
       - Team meetings schedule
       - Progress reporting
       - Stakeholder updates
       - Issue escalation process
    
    10. DOCUMENTATION REQUIREMENTS
        - Technical documentation
        - User documentation
        - API documentation
        - Deployment guides
    
    Format as a comprehensive project management document with clear sections.
    """


def create_progress_tracking_task_description(project_plan: str, current_progress: str) -> str:
    """
    Generate a task description for progress tracking and reporting.
    
    Args:
        project_plan: The project plan
        current_progress: Current development progress
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Create a progress report based on:
    
    PROJECT PLAN:
    {project_plan}
    
    CURRENT PROGRESS:
    {current_progress}
    
    Your progress report should include:
    
    1. EXECUTIVE SUMMARY
       - Overall project status (On Track / At Risk / Delayed)
       - Percentage complete
       - Key accomplishments this period
       - Upcoming milestones
    
    2. COMPLETED TASKS
       - Task name
       - Completed by (agent)
       - Completion date
       - Quality notes
    
    3. IN-PROGRESS TASKS
       - Task name
       - Assigned to (agent)
       - Progress percentage
       - Expected completion
       - Blockers (if any)
    
    4. UPCOMING TASKS (Next 2 Weeks)
       - Task name
       - Assigned to (agent)
       - Planned start date
       - Dependencies
    
    5. ISSUES & BLOCKERS
       - Issue description
       - Impact on timeline
       - Resolution plan
       - Owner
    
    6. RISKS & CONCERNS
       - New risks identified
       - Risk status updates
       - Mitigation actions taken
    
    7. TIMELINE STATUS
       - Original end date
       - Current projected end date
       - Variance explanation
       - Recovery plan (if delayed)
    
    8. QUALITY METRICS
       - Code coverage percentage
       - Bugs found vs fixed
       - Code review status
       - Test pass rate
    
    9. NEXT STEPS
       - Immediate priorities
       - Decisions needed
       - Resources needed
    
    10. RECOMMENDATIONS
        - Process improvements
        - Risk mitigation actions
        - Resource adjustments
    
    Format as a clear, actionable progress report suitable for both 
    technical team members and non-technical stakeholders.
    """
