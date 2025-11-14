"""
Web Research Tools

Tools for searching the web, finding best practices,
analyzing competitors, and gathering information.
"""

from crewai_tools import tool
from typing import Optional
import requests
from bs4 import BeautifulSoup
import os


@tool("Web Search Tool")
def search_web(query: str) -> str:
    """
    Search the web for information using Serper API or fallback to basic search.
    
    Args:
        query: Search query string
        
    Returns:
        str: Search results formatted as text
    """
    serper_api_key = os.getenv('SERPER_API_KEY')
    
    if serper_api_key:
        return _search_with_serper(query, serper_api_key)
    else:
        return _basic_web_search(query)


def _search_with_serper(query: str, api_key: str) -> str:
    """Search using Serper API (Google Search)."""
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    payload = {'q': query, 'num': 5}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json()
        
        # Format results
        formatted_results = []
        if 'organic' in results:
            for i, result in enumerate(results['organic'][:5], 1):
                formatted_results.append(
                    f"{i}. {result.get('title', 'No title')}\n"
                    f"   {result.get('snippet', 'No description')}\n"
                    f"   URL: {result.get('link', '')}\n"
                )
        
        return "\n".join(formatted_results) if formatted_results else "No results found."
    
    except Exception as e:
        return f"Error searching with Serper: {str(e)}"


def _basic_web_search(query: str) -> str:
    """Basic fallback search without API."""
    return f"""
    Web search for: {query}
    
    Note: Serper API key not configured. Please set SERPER_API_KEY in .env for actual web search.
    
    For now, here are general recommendations based on common best practices:
    
    1. Check official documentation for the technology stack
    2. Review GitHub repositories with similar implementations
    3. Consult Stack Overflow for specific problems
    4. Review Medium articles for tutorials
    5. Check dev.to for community insights
    
    To enable real web search, add your Serper API key to .env:
    SERPER_API_KEY=your-api-key
    Get free API key at: https://serper.dev
    """


@tool("Best Practices Research Tool")
def research_best_practices(topic: str, technology: str) -> str:
    """
    Research best practices for a specific technology or topic.
    
    Args:
        topic: The topic to research (e.g., "API authentication", "React state management")
        technology: The technology stack (e.g., "Flask", "React", "PostgreSQL")
        
    Returns:
        str: Best practices and recommendations
    """
    # Common best practices database (can be enhanced with real search)
    best_practices = {
        "flask": """
        Flask Best Practices:
        1. Use Blueprints for organizing routes
        2. Implement proper error handling with try-except
        3. Use Flask-SQLAlchemy for database operations
        4. Implement JWT authentication for APIs
        5. Use environment variables for configuration
        6. Add request validation using marshmallow or pydantic
        7. Implement CORS properly for frontend integration
        8. Use application factory pattern
        9. Add comprehensive logging
        10. Write tests with pytest
        """,
        "fastapi": """
        FastAPI Best Practices:
        1. Use Pydantic models for request/response validation
        2. Implement dependency injection for database sessions
        3. Use async/await for I/O operations
        4. Auto-generate API documentation (built-in)
        5. Implement OAuth2 with Password flow for authentication
        6. Use SQLAlchemy with async support
        7. Add proper exception handlers
        8. Use background tasks for long-running operations
        9. Implement rate limiting
        10. Write tests with pytest and TestClient
        """,
        "react": """
        React Best Practices:
        1. Use functional components with hooks
        2. Implement proper state management (Context API or Redux)
        3. Use React Query for API calls and caching
        4. Implement code splitting and lazy loading
        5. Use TypeScript for type safety
        6. Follow component composition patterns
        7. Implement proper error boundaries
        8. Use memo and useCallback for optimization
        9. Implement proper form validation
        10. Write tests with React Testing Library
        """,
        "postgresql": """
        PostgreSQL Best Practices:
        1. Use proper indexes for frequently queried columns
        2. Implement foreign key constraints
        3. Use transactions for related operations
        4. Add proper validation constraints
        5. Use connection pooling
        6. Implement regular backups
        7. Use prepared statements to prevent SQL injection
        8. Optimize queries with EXPLAIN ANALYZE
        9. Use appropriate data types
        10. Implement proper migration strategy
        """,
        "authentication": """
        Authentication Best Practices:
        1. Use JWT tokens for stateless authentication
        2. Hash passwords with bcrypt (cost factor 12+)
        3. Implement refresh tokens
        4. Use HTTPS for all authentication endpoints
        5. Implement rate limiting on login endpoints
        6. Add account lockout after failed attempts
        7. Require strong passwords
        8. Implement password reset functionality
        9. Use secure session management
        10. Add two-factor authentication (optional)
        """,
    }
    
    tech_lower = technology.lower()
    topic_lower = topic.lower()
    
    # Search for relevant best practices
    results = []
    for key, practices in best_practices.items():
        if key in tech_lower or key in topic_lower:
            results.append(practices)
    
    if results:
        return "\n\n".join(results)
    else:
        return f"""
        Best practices for {technology} - {topic}:
        
        General Recommendations:
        1. Follow official documentation
        2. Use latest stable version
        3. Implement proper error handling
        4. Add comprehensive tests
        5. Use linting and formatting tools
        6. Follow security best practices
        7. Optimize for performance
        8. Add proper documentation
        9. Use version control
        10. Regular dependency updates
        
        For more specific guidance, use the Web Search Tool.
        """


@tool("Library Finder Tool")
def find_libraries(purpose: str, language: str) -> str:
    """
    Find recommended libraries for a specific purpose.
    
    Args:
        purpose: What the library should do (e.g., "authentication", "PDF generation")
        language: Programming language (python, javascript)
        
    Returns:
        str: Recommended libraries with descriptions
    """
    libraries = {
        "python": {
            "authentication": """
            Recommended Python Authentication Libraries:
            
            1. PyJWT (python-jwt)
               - Purpose: JWT token creation and validation
               - Install: pip install PyJWT
               - Use case: Stateless API authentication
            
            2. Flask-JWT-Extended
               - Purpose: JWT extension for Flask
               - Install: pip install flask-jwt-extended
               - Use case: Full-featured JWT auth for Flask
            
            3. Passlib
               - Purpose: Password hashing
               - Install: pip install passlib[bcrypt]
               - Use case: Secure password storage
            
            4. python-jose
               - Purpose: JWT and JWS implementation
               - Install: pip install python-jose[cryptography]
               - Use case: OAuth2 and OpenID Connect
            """,
            "database": """
            Recommended Python Database Libraries:
            
            1. SQLAlchemy
               - Purpose: SQL toolkit and ORM
               - Install: pip install sqlalchemy
               - Use case: Database operations with any SQL database
            
            2. psycopg2-binary
               - Purpose: PostgreSQL adapter
               - Install: pip install psycopg2-binary
               - Use case: Direct PostgreSQL connection
            
            3. Alembic
               - Purpose: Database migrations
               - Install: pip install alembic
               - Use case: Version control for database schema
            
            4. SQLModel
               - Purpose: SQLAlchemy + Pydantic
               - Install: pip install sqlmodel
               - Use case: Modern ORM with type hints
            """,
            "testing": """
            Recommended Python Testing Libraries:
            
            1. pytest
               - Purpose: Testing framework
               - Install: pip install pytest
               - Use case: Unit and integration tests
            
            2. pytest-cov
               - Purpose: Coverage reporting
               - Install: pip install pytest-cov
               - Use case: Test coverage analysis
            
            3. Faker
               - Purpose: Fake data generation
               - Install: pip install faker
               - Use case: Test data creation
            
            4. factory-boy
               - Purpose: Test fixtures
               - Install: pip install factory-boy
               - Use case: Model instance creation for tests
            """,
        },
        "javascript": {
            "frontend": """
            Recommended JavaScript Frontend Libraries:
            
            1. React
               - Purpose: UI framework
               - Install: npx create-react-app my-app
               - Use case: Building interactive UIs
            
            2. Axios
               - Purpose: HTTP client
               - Install: npm install axios
               - Use case: API calls from frontend
            
            3. React Router
               - Purpose: Routing
               - Install: npm install react-router-dom
               - Use case: Single-page application routing
            
            4. Tailwind CSS
               - Purpose: Utility-first CSS framework
               - Install: npm install -D tailwindcss
               - Use case: Rapid UI development
            """,
            "validation": """
            Recommended JavaScript Validation Libraries:
            
            1. Yup
               - Purpose: Schema validation
               - Install: npm install yup
               - Use case: Form validation
            
            2. Joi
               - Purpose: Data validation
               - Install: npm install joi
               - Use case: Input validation
            
            3. Validator.js
               - Purpose: String validators
               - Install: npm install validator
               - Use case: Email, URL validation
            """,
        }
    }
    
    lang_lower = language.lower()
    purpose_lower = purpose.lower()
    
    if lang_lower in libraries:
        for key, libs in libraries[lang_lower].items():
            if key in purpose_lower or purpose_lower in key:
                return libs
    
    return f"""
    Library recommendations for: {purpose} ({language})
    
    Please use Web Search Tool for more specific library recommendations.
    Consider factors like:
    - Active maintenance
    - Community support
    - Documentation quality
    - Security track record
    - Performance
    - License compatibility
    """


class WebResearchTool:
    """Wrapper class for web research tools."""
    
    @staticmethod
    def search(query: str) -> str:
        return search_web(query)
    
    @staticmethod
    def best_practices(topic: str, technology: str) -> str:
        return research_best_practices(topic, technology)
    
    @staticmethod
    def find_library(purpose: str, language: str) -> str:
        return find_libraries(purpose, language)


class SearchTool:
    """Legacy wrapper for backward compatibility."""
    
    def __init__(self):
        self.research = WebResearchTool()
