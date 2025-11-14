"""
Backend Developer Agent

Responsible for:
- Designing and implementing REST APIs
- Database schema design and optimization
- Authentication and authorization
- Business logic implementation
- API documentation
- Backend testing
"""

from crewai import Agent
from typing import List, Optional


def create_backend_developer_agent(tools: Optional[List] = None, verbose: bool = True, llm = None) -> Agent:
    """
    Create a Backend Developer agent specialized in building
    robust, scalable backend systems.
    
    Args:
        tools: List of tools available to the agent
        verbose: Whether to show detailed output
        llm: Language model to use (if None, will use default from environment)
        
    Returns:
        Agent: Configured Backend Developer agent
    """
    agent_config = {
        'role': 'Senior Backend Developer',
        'goal': 'Design and implement robust, secure, and scalable backend systems using Python, Flask/FastAPI, and PostgreSQL',
        'backstory': """You are a Senior Backend Developer with 8+ years of experience building 
        web applications for small and medium-sized businesses. You specialize in Python 
        and have deep expertise in Flask, FastAPI, SQLAlchemy, and PostgreSQL.
        
        Your strengths include:
        - RESTful API design following industry best practices
        - Database schema design and optimization
        - JWT authentication and role-based access control (RBAC)
        - Input validation and error handling
        - Writing clean, maintainable code
        - Comprehensive testing (unit, integration)
        - API documentation with Swagger/OpenAPI
        - Performance optimization
        
        You always follow these principles:
        - Security first (SQL injection prevention, password hashing, CORS)
        - DRY (Don't Repeat Yourself)
        - SOLID principles
        - Proper error handling and logging
        - Database transactions for data integrity
        - Input validation at all entry points
        
        You prefer:
        - Flask for simpler projects
        - FastAPI for projects requiring high performance or async operations
        - PostgreSQL for relational data
        - SQLAlchemy ORM for database operations
        - pytest for testing
        - Pydantic for data validation""",
        'tools': tools or [],
        'verbose': verbose,
        'allow_delegation': False,
        'max_iter': 20,
        'memory': True,
    }
    
    if llm is not None:
        agent_config['llm'] = llm
    
    return Agent(**agent_config)


def create_api_design_task_description(requirements: str, user_stories: str) -> str:
    """
    Generate a task description for API design.
    
    Args:
        requirements: Project requirements
        user_stories: User stories from BA
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Design a comprehensive REST API based on these requirements and user stories:
    
    REQUIREMENTS:
    {requirements}
    
    USER STORIES:
    {user_stories}
    
    Your deliverable should include:
    
    1. API ARCHITECTURE
       - Framework choice (Flask/FastAPI) with justification
       - Project structure
       - Design patterns used
    
    2. API ENDPOINTS
       For each endpoint provide:
       - HTTP Method (GET, POST, PUT, DELETE)
       - Route path
       - Request body schema
       - Response schema
       - Status codes
       - Authentication requirements
    
    3. DATABASE SCHEMA
       - Tables/Models
       - Columns with data types
       - Relationships (One-to-Many, Many-to-Many)
       - Indexes for performance
       - Constraints (unique, foreign keys)
    
    4. AUTHENTICATION & AUTHORIZATION
       - JWT token structure
       - User roles and permissions
       - Protected endpoints
       - Token refresh strategy
    
    5. ERROR HANDLING
       - Standard error response format
       - Common error codes
       - Validation error messages
    
    6. SECURITY MEASURES
       - Password hashing strategy (bcrypt)
       - SQL injection prevention
       - CORS configuration
       - Rate limiting
       - Input validation
    
    Format as detailed API documentation in Markdown.
    """


def create_implementation_task_description(api_design: str) -> str:
    """
    Generate a task description for backend implementation.
    
    Args:
        api_design: The API design document
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Implement the backend system based on this API design:
    
    {api_design}
    
    IMPLEMENTATION REQUIREMENTS:
    
    1. PROJECT STRUCTURE
       Create a well-organized project structure:
       ```
       backend/
       ├── app/
       │   ├── __init__.py
       │   ├── models/
       │   ├── routes/
       │   ├── services/
       │   ├── schemas/
       │   └── utils/
       ├── config/
       ├── tests/
       ├── requirements.txt
       └── run.py
       ```
    
    2. DATABASE MODELS
       - Implement all models using SQLAlchemy
       - Add proper relationships
       - Include timestamps (created_at, updated_at)
       - Add __repr__ methods
    
    3. API ROUTES
       - Implement all endpoints
       - Add input validation
       - Implement error handling
       - Add logging
    
    4. BUSINESS LOGIC
       - Separate business logic into service layer
       - Implement all CRUD operations
       - Add transaction management
       - Handle edge cases
    
    5. AUTHENTICATION
       - Implement JWT token generation
       - Create login/register endpoints
       - Add token validation middleware
       - Implement password hashing
    
    6. TESTING
       - Unit tests for models
       - Integration tests for APIs
       - Test coverage > 80%
       - Mock external dependencies
    
    7. DOCUMENTATION
       - Add docstrings to all functions
       - Create API documentation
       - Add README with setup instructions
    
    Provide complete, production-ready code with proper error handling and security measures.
    """
