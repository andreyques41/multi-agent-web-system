"""
Frontend Developer Agent

Responsible for:
- Creating responsive, modern user interfaces
- Implementing React/Vue components or vanilla JS
- Frontend state management
- API integration
- CSS styling with Tailwind or custom CSS
- Frontend testing
"""

from crewai import Agent
from typing import List, Optional


def create_frontend_developer_agent(tools: Optional[List] = None, verbose: bool = True, llm = None) -> Agent:
    """
    Create a Frontend Developer agent specialized in building
    modern, responsive user interfaces.
    
    Args:
        tools: List of tools available to the agent
        verbose: Whether to show detailed output
        llm: Language model to use (if None, will use default from environment)
        
    Returns:
        Agent: Configured Frontend Developer agent
    """
    agent_config = {
        'role': 'Senior Frontend Developer',
        'goal': 'Create beautiful, responsive, and user-friendly interfaces that work perfectly on all devices',
        'backstory': """You are a Senior Frontend Developer with 7+ years of experience 
        creating modern web applications. You're proficient in React, Vue, and vanilla 
        JavaScript, and you have a keen eye for design and user experience.
        
        Your expertise includes:
        - Responsive design (mobile-first approach)
        - Modern CSS (Flexbox, Grid, Tailwind CSS)
        - React with hooks and context API
        - Vue 3 with Composition API
        - State management (Redux, Vuex, or Context API)
        - REST API integration with fetch/axios
        - Form validation and user input handling
        - Loading states and error handling
        - Accessibility (WCAG compliance)
        - Cross-browser compatibility
        - Performance optimization (lazy loading, code splitting)
        
        You always consider:
        - Mobile users (responsive design)
        - User experience (intuitive navigation, clear CTAs)
        - Loading states (skeletons, spinners)
        - Error handling (user-friendly messages)
        - Accessibility (semantic HTML, ARIA labels)
        - Performance (optimized images, minimal bundle size)
        - SEO (meta tags, semantic structure)
        
        Your approach:
        - For simple sites: Clean HTML/CSS/JS with modern practices
        - For complex apps: React or Vue with proper state management
        - Always use Tailwind CSS or well-structured custom CSS
        - Mobile-first responsive design
        - Component-based architecture
        - Clean, maintainable code with proper comments""",
        'tools': tools or [],
        'verbose': verbose,
        'allow_delegation': False,
        'max_iter': 20,
        'memory': True,
    }
    
    if llm is not None:
        agent_config['llm'] = llm
    
    return Agent(**agent_config)


def create_ui_design_task_description(requirements: str, api_design: str) -> str:
    """
    Generate a task description for UI design and component planning.
    
    Args:
        requirements: Project requirements
        api_design: Backend API design
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Design the frontend architecture and UI components based on:
    
    REQUIREMENTS:
    {requirements}
    
    API DESIGN:
    {api_design}
    
    Your deliverable should include:
    
    1. TECHNOLOGY STACK DECISION
       - Framework choice (React/Vue/Vanilla JS) with justification
       - CSS approach (Tailwind/Custom CSS)
       - State management strategy
       - Build tools (Vite/Webpack)
    
    2. COMPONENT ARCHITECTURE
       List all components with:
       - Component name
       - Purpose
       - Props/inputs
       - State needed
       - Child components
    
    3. PAGE LAYOUTS
       For each page define:
       - Layout structure
       - Sections/components used
       - Responsive behavior
       - Navigation flow
    
    4. STYLING APPROACH
       - Color scheme
       - Typography (fonts, sizes)
       - Spacing system
       - Component styling strategy
       - Responsive breakpoints
    
    5. STATE MANAGEMENT
       - What data needs global state
       - API call handling
       - Loading and error states
       - Form state management
    
    6. ROUTING
       - All routes/pages
       - Protected routes (authentication)
       - Route parameters
       - Navigation structure
    
    7. API INTEGRATION PLAN
       - Which endpoints each component calls
       - Authentication token handling
       - Error handling strategy
       - Loading state patterns
    
    8. ACCESSIBILITY & UX
       - Keyboard navigation
       - Screen reader support
       - Focus management
       - Loading indicators
       - Error messages
    
    Format as a comprehensive frontend architecture document.
    """


def create_implementation_task_description(ui_design: str) -> str:
    """
    Generate a task description for frontend implementation.
    
    Args:
        ui_design: The UI design document
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Implement the frontend application based on this design:
    
    {ui_design}
    
    IMPLEMENTATION REQUIREMENTS:
    
    1. PROJECT SETUP
       - Initialize project with chosen framework
       - Configure build tools
       - Set up folder structure
       - Install and configure Tailwind CSS (or set up CSS structure)
    
    2. COMPONENT IMPLEMENTATION
       - Create all components following the design
       - Implement proper prop types/TypeScript interfaces
       - Add loading and error states
       - Ensure responsive design
       - Add accessibility attributes
    
    3. STATE MANAGEMENT
       - Set up state management (Context/Redux/Vuex)
       - Implement API integration
       - Handle authentication state
       - Manage form state
    
    4. ROUTING
       - Set up all routes
       - Implement protected routes
       - Add navigation components
       - Handle 404 pages
    
    5. STYLING
       - Implement responsive design
       - Add hover/active states
       - Ensure consistent spacing
       - Optimize for mobile
       - Add loading animations
    
    6. API INTEGRATION
       - Create API client/service layer
       - Implement all API calls
       - Add error handling
       - Implement token management
       - Add request interceptors
    
    7. FORMS & VALIDATION
       - Implement all forms
       - Add client-side validation
       - Show clear error messages
       - Handle submission states
    
    8. TESTING
       - Component unit tests
       - Integration tests for key flows
       - Accessibility tests
    
    9. OPTIMIZATION
       - Code splitting
       - Lazy loading
       - Image optimization
       - Bundle size optimization
    
    Provide complete, production-ready code with proper error handling and responsive design.
    """
