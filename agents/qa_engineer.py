"""
QA Engineer Agent

Responsible for:
- Creating comprehensive test suites
- Unit testing
- Integration testing
- End-to-end testing
- Test coverage analysis
- Bug reporting and verification
- Quality assurance standards
"""

from crewai import Agent
from typing import List, Optional


def create_qa_engineer_agent(tools: Optional[List] = None, verbose: bool = True, llm = None) -> Agent:
    """
    Create a QA Engineer agent specialized in ensuring
    code quality and comprehensive testing.
    
    Args:
        tools: List of tools available to the agent
        verbose: Whether to show detailed output
        llm: Language model to use (if None, will use default from environment)
        
    Returns:
        Agent: Configured QA Engineer agent
    """
    agent_config = {
        'role': 'Senior QA Engineer',
        'goal': 'Ensure the highest quality standards through comprehensive testing and quality assurance practices',
        'backstory': """You are a Senior QA Engineer with 6+ years of experience in 
        software quality assurance and test automation. You have a meticulous eye 
        for detail and a passion for ensuring software works flawlessly.
        
        Your expertise includes:
        - Test strategy and planning
        - Unit testing with pytest and Jest
        - Integration testing
        - End-to-end testing with Selenium/Playwright
        - API testing with Postman/pytest
        - Test coverage analysis
        - Performance testing basics
        - Security testing fundamentals
        - Bug tracking and reporting
        - Test automation
        
        Your testing philosophy:
        - Test early, test often
        - Aim for >80% code coverage
        - Focus on critical paths first
        - Test both happy paths and edge cases
        - Automate repetitive tests
        - Clear, reproducible bug reports
        - Testing is everyone's responsibility
        
        You always test for:
        - Functionality (does it work as expected?)
        - Usability (is it user-friendly?)
        - Security (is it safe from vulnerabilities?)
        - Performance (is it fast enough?)
        - Compatibility (works across browsers/devices?)
        - Accessibility (usable by everyone?)
        
        Your approach:
        - Create test plans before testing
        - Write automated tests alongside development
        - Test from user's perspective
        - Document bugs clearly with reproduction steps
        - Verify fixes before closing bugs
        - Maintain test suites as code evolves""",
        'tools': tools or [],
        'verbose': verbose,
        'allow_delegation': False,
        'max_iter': 20,
        'memory': True,
    }
    
    if llm is not None:
        agent_config['llm'] = llm
    
    return Agent(**agent_config)


def create_test_plan_task_description(requirements: str, backend_code: str, frontend_code: str) -> str:
    """
    Generate a task description for creating a test plan.
    
    Args:
        requirements: Project requirements
        backend_code: Backend implementation summary
        frontend_code: Frontend implementation summary
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Create a comprehensive test plan based on:
    
    REQUIREMENTS:
    {requirements}
    
    BACKEND IMPLEMENTATION:
    {backend_code}
    
    FRONTEND IMPLEMENTATION:
    {frontend_code}
    
    Your test plan should include:
    
    1. TEST STRATEGY
       - Testing levels (unit, integration, e2e)
       - Testing types (functional, security, performance)
       - Test environment setup
       - Testing tools and frameworks
    
    2. BACKEND TESTING PLAN
       
       A. Unit Tests:
          - Model tests (database models)
          - Service layer tests (business logic)
          - Utility function tests
          
       B. Integration Tests:
          - API endpoint tests
          - Database integration tests
          - Authentication flow tests
          
       C. Security Tests:
          - SQL injection prevention
          - XSS prevention
          - CSRF protection
          - Authentication/authorization
          - Password security
    
    3. FRONTEND TESTING PLAN
       
       A. Component Tests:
          - Individual component rendering
          - Component interactions
          - Props validation
          
       B. Integration Tests:
          - API integration
          - State management
          - Form submissions
          
       C. E2E Tests:
          - User registration flow
          - Login/logout flow
          - Critical user journeys
          - Error handling scenarios
    
    4. TEST CASES
       For each major feature, provide:
       - Test case ID
       - Description
       - Preconditions
       - Test steps
       - Expected result
       - Priority (Critical/High/Medium/Low)
    
    5. COVERAGE GOALS
       - Target coverage percentage per component
       - Critical paths requiring 100% coverage
       - Areas that can have lower coverage
    
    6. BUG REPORTING TEMPLATE
       - Bug severity levels
       - Bug report format
       - Bug lifecycle
    
    7. ACCEPTANCE CRITERIA
       - When is a feature considered "done"?
       - Quality gates for deployment
       - Performance benchmarks
    
    Format as a detailed test plan document.
    """


def create_test_implementation_task_description(test_plan: str) -> str:
    """
    Generate a task description for implementing tests.
    
    Args:
        test_plan: The test plan document
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Implement comprehensive automated tests based on this test plan:
    
    {test_plan}
    
    IMPLEMENTATION REQUIREMENTS:
    
    1. BACKEND TESTS (Python/pytest)
       
       A. Unit Tests Structure:
          ```
          tests/
          ├── unit/
          │   ├── test_models.py
          │   ├── test_services.py
          │   └── test_utils.py
          ├── integration/
          │   ├── test_api_endpoints.py
          │   ├── test_auth.py
          │   └── test_database.py
          └── conftest.py (fixtures)
          ```
       
       B. Implement:
          - All model tests with database fixtures
          - Service layer tests with mocking
          - API endpoint tests with test client
          - Authentication flow tests
          - Error handling tests
          - Input validation tests
       
       C. Use pytest features:
          - Fixtures for common setup
          - Parametrize for multiple test cases
          - Markers for test organization
          - Coverage reporting
    
    2. FRONTEND TESTS (Jest/React Testing Library or Vue Test Utils)
       
       A. Component Tests:
          - Render tests for all components
          - User interaction tests
          - Props validation tests
          - State change tests
       
       B. Integration Tests:
          - API mocking with MSW or similar
          - Navigation flow tests
          - Form submission tests
          - Error handling tests
       
       C. E2E Tests (Playwright/Cypress):
          - Full user registration flow
          - Login and authentication
          - Main feature workflows
          - Error scenarios
    
    3. TEST UTILITIES
       - Create test fixtures and factories
       - Set up test database
       - Create mock data generators
       - API mocking utilities
    
    4. CONTINUOUS INTEGRATION
       - GitHub Actions workflow for tests
       - Run tests on every PR
       - Coverage reporting
       - Fail build if coverage drops
    
    5. TEST DOCUMENTATION
       - README for running tests
       - Test naming conventions
       - How to add new tests
       - Debugging failed tests
    
    6. QUALITY METRICS
       - Code coverage report
       - Test execution time
       - Flaky test identification
       - Test maintenance guidelines
    
    Provide complete, working test suites with >80% coverage and clear documentation.
    Include sample commands to run tests and generate coverage reports.
    """
