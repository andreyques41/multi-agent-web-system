"""
Project Crew

Main crew that coordinates all agents to work together on a web development project.
"""

from crewai import Crew, Task, Process
from typing import List, Optional
from pathlib import Path

from agents import (
    create_business_analyst_agent,
    create_backend_developer_agent,
    create_frontend_developer_agent,
    create_qa_engineer_agent,
    create_devops_engineer_agent,
    create_project_manager_agent,
)
from utils.token_manager import TaskOutputManager, count_tokens
from crewai_tools import FileWriterTool, DirectoryReadTool, FileReadTool


class ProjectCrew:
    """
    Main crew that orchestrates all agents for a complete web development project.
    """
    
    def __init__(
        self,
        project_name: str,
        project_type: str,
        output_dir: str = "./output",
        description: str = ""
    ):
        """
        Initialize the Project Crew.
        
        Args:
            project_name: Name of the project
            project_type: Type of project (ecommerce, landing, dashboard, api)
            output_dir: Directory where project will be created
            description: Additional project description from client
        """
        self.project_name = project_name
        self.project_type = project_type
        self.output_dir = Path(output_dir)
        self.description = description or f"A {project_type} project for small/medium business"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create project-specific directory
        self.project_dir = self.output_dir / self.project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize token manager to prevent 413 errors
        self.token_manager = TaskOutputManager(model="gpt-4o")
        
        # File operation tools for agents to create actual files
        # FileWriterTool allows agents to write files to the project directory
        self.file_tools = [
            FileWriterTool(directory=str(self.project_dir))
        ]
        
        # Create agents with file tools - all use gpt-4o for stability
        self.pm_agent = create_project_manager_agent(tools=self.file_tools)
        self.ba_agent = create_business_analyst_agent(tools=self.file_tools)
        self.backend_agent = create_backend_developer_agent(tools=self.file_tools)
        self.frontend_agent = create_frontend_developer_agent(tools=self.file_tools)
        self.qa_agent = create_qa_engineer_agent(tools=self.file_tools)
        self.devops_agent = create_devops_engineer_agent(tools=self.file_tools)
    
    def create_tasks(self) -> List[Task]:
        """Create tasks for the crew based on project type."""
        tasks = []
        
        # Safety prefix for all tasks to avoid content policy violations
        safety_prefix = """
        IMPORTANT CONTENT POLICY:
        - This is a PROFESSIONAL BUSINESS application
        - Focus ONLY on corporate/enterprise software features
        - NO personal, social, dating, adult, or inappropriate content
        - Use professional examples: companies, products, services, data
        - Stick to standard business domains: e-commerce, CRM, dashboards, analytics
        """
        
        # Task 1: Project Planning (PM)
        # NO CONTEXT - first task starts fresh
        task_planning = Task(
            description=safety_prefix + f"""
            Create a professional business project plan for: {self.project_name}
            Project Type: {self.project_type}
            
            This is a BUSINESS/CORPORATE project. Focus on:
            - Professional project scope and business objectives
            - Development timeline with 3-4 milestones
            - Team coordination and resource allocation
            - Technical risk assessment
            - Measurable success criteria
            
            Format as markdown with clear sections.
            Keep it professional and business-focused. Maximum 300 words.
            """,
            agent=self.pm_agent,
            expected_output="Professional project plan in markdown format",
            context=[]  # Explicitly set to empty - no previous context
        )
        tasks.append(task_planning)
        
        # Task 2: Requirements Analysis (BA)
        # ONLY receives Task 1 context (project plan)
        task_requirements = Task(
            description=safety_prefix + f"""
            Create technical requirements for a BUSINESS {self.project_type} application: {self.project_name}
            
            This is a PROFESSIONAL/CORPORATE project. Specify:
            - 5 core business features (e.g., user authentication, data display, forms)
            - 3 user stories for business users
            - Technical stack recommendations (React/Vue, Node/Python, PostgreSQL)
            - Professional UI/UX guidelines
            
            Format as markdown with clear sections.
            Keep it technical and business-focused. Maximum 200 words.
            NO personal, social, or inappropriate content.
            """,
            agent=self.ba_agent,
            expected_output="Technical requirements document in markdown format",
            context=[task_planning]  # Only needs project plan
        )
        tasks.append(task_requirements)
        
        # Task 3: Backend Design & Implementation
        # ONLY receives Task 2 context (requirements) - skips Task 1
        if self.project_type in ['ecommerce', 'dashboard', 'api']:
            task_backend = Task(
                description=safety_prefix + f"""
                Design PROFESSIONAL backend API for business {self.project_type}: {self.project_name}
                
                Create BUSINESS-FOCUSED backend documentation:
                - 3 main REST API endpoints (essential business operations)
                - Database schema (2-3 tables: users, main business entity)
                - JWT authentication approach
                - Basic CRUD operations
                - API code examples in Python/Flask OR Node.js/Express
                
                Database: PostgreSQL
                
                Format as markdown with code blocks.
                Keep it professional and concise. Maximum 300 words total.
                NO inappropriate or personal content.
                """,
                agent=self.backend_agent,
                expected_output="Backend API documentation in markdown with code examples",
                context=[task_requirements]  # Only needs requirements, not project plan
            )
            tasks.append(task_backend)
        
        # Task 4: Frontend Implementation
        # ONLY receives Task 2 context (requirements) - skips Task 1 and 3
        if self.project_type in ['ecommerce', 'landing', 'dashboard']:
            task_frontend = Task(
                description=safety_prefix + f"""
                Create PROFESSIONAL frontend for business {self.project_type}: {self.project_name}
                
                Build BUSINESS-FOCUSED UI documentation:
                - 2 main pages (Home, Dashboard - essential pages)
                - Responsive design approach (desktop/mobile)
                - Professional color scheme (blue/gray corporate colors)
                - Basic business form (login or contact)
                - HTML/CSS/JS code examples
                
                Use: React OR Vue.js OR vanilla HTML/CSS/JS
                Styling: Tailwind CSS OR Bootstrap
                
                Format as markdown with code blocks.
                Keep it professional and concise. Maximum 300 words total.
                NO personal, social, or inappropriate content - BUSINESS ONLY.
                """,
                agent=self.frontend_agent,
                expected_output="Frontend documentation in markdown with code examples",
                context=[task_requirements]  # Only needs requirements, not backend details
            )
            tasks.append(task_frontend)
        
        # Task 5: Testing & QA
        # Receives ONLY requirements (Task 2) - NO implementation details
        task_testing = Task(
            description=safety_prefix + f"""
            Create PROFESSIONAL test plan for business application: {self.project_name}
            
            Provide BUSINESS-FOCUSED test documentation:
            - Brief test plan (focus on business functionality)
            - 3 unit test examples (test key business logic)
            - 1 integration test example (test main user workflow)
            - Brief test coverage summary
            
            Focus on: Authentication, data validation, API responses
            
            Format as markdown with code examples.
            Keep it concise and professional. Maximum 200 words.
            """,
            agent=self.qa_agent,
            expected_output="Test plan in markdown with code examples",
            context=[task_requirements]  # Only needs requirements to test against
        )
        tasks.append(task_testing)
        
        # Task 6: Deployment Setup
        # NO CONTEXT - deployment config is independent
        task_deployment = Task(
            description=safety_prefix + f"""
            Create PROFESSIONAL deployment config for business {self.project_type}: {self.project_name}
            
            Provide STANDARD deployment documentation:
            - Dockerfile example (Node.js OR Python base image)
            - docker-compose.yml example (web service + database)
            - Brief GitHub Actions CI/CD workflow
            - Brief deployment instructions
            
            Use standard practices for {self.project_type} applications.
            
            Format as markdown with code blocks (YAML, Dockerfile).
            Keep it professional and concise. Maximum 200 words total.
            """,
            agent=self.devops_agent,
            expected_output="Deployment documentation in markdown with config examples",
            context=[]  # Deployment is generic, doesn't need previous outputs
        )
        tasks.append(task_deployment)
        
        # Task 7: Final Documentation & Handoff (PM)
        # ONLY receives Task 1 (project plan) + Task 2 (requirements) - minimal context
        task_handoff = Task(
            description=safety_prefix + f"""
            Create PROFESSIONAL README documentation for: {self.project_name}
            
            Provide BUSINESS-FOCUSED documentation:
            - Project overview and business value
            - Quick start guide (how to run)
            - Setup instructions (dependencies, environment)
            - Usage guide (main features)
            - Brief deployment guide
            - 3 future enhancements
            
            Format as proper README.md with clear sections and structure.
            Keep it professional and client-ready. Maximum 250 words total.
            Focus on BUSINESS value and technical accuracy.
            """,
            agent=self.pm_agent,
            expected_output="Professional README.md documentation",
            context=[task_planning, task_requirements]  # Only high-level info, not implementation details
        )
        tasks.append(task_handoff)
        
        return tasks
    
    def run(self) -> str:
        """
        Execute the crew and create the project.
        
        Returns:
            str: Summary of the project creation process
        """
        tasks = self.create_tasks()
        
        # Storage for task outputs to save as files
        task_outputs = {}
        
        # Add step callbacks to truncate outputs and save files
        def create_task_callback(task_name, filename=None):
            """Create a callback for a specific task."""
            def callback(output):
                """Callback to truncate task output and save to file."""
                if hasattr(output, 'raw'):
                    raw_output = str(output.raw)
                else:
                    raw_output = str(output)
                
                # Store output
                task_outputs[task_name] = raw_output
                
                # Save to file if filename specified
                if filename:
                    file_path = self.project_dir / filename
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_text(raw_output, encoding='utf-8')
                    print(f"✅ Saved: {filename}")
                
                # Count tokens
                token_count = count_tokens(raw_output, "gpt-4o")
                
                # If output is too large, truncate it for next task
                if token_count > 1500:
                    truncated = self.token_manager.store_output(
                        task_id=id(output),
                        output=raw_output
                    )
                    print(f"⚠️  Output truncated: {token_count} → ~1500 tokens")
                    
                    if hasattr(output, 'raw'):
                        output.raw = truncated
                    return output
                
                return output
            return callback
        
        # Apply callbacks to tasks with file names
        task_file_mapping = {
            0: ('planning', 'PROJECT_PLAN.md'),
            1: ('requirements', 'REQUIREMENTS.md'),
            2: ('backend', 'BACKEND.md'),  # Backend task if exists
            3: ('frontend', 'FRONTEND.md'),  # Frontend task if exists  
            4: ('testing', 'TESTING.md'),
            5: ('deployment', 'DEPLOYMENT.md'),
            6: ('docs', 'README.md')
        }
        
        for idx, task in enumerate(tasks):
            if idx in task_file_mapping:
                task_name, filename = task_file_mapping[idx]
                task.callback = create_task_callback(task_name, filename)
            else:
                task.callback = create_task_callback(f'task_{idx}', None)
        
        crew = Crew(
            agents=[
                self.pm_agent,
                self.ba_agent,
                self.backend_agent,
                self.frontend_agent,
                self.qa_agent,
                self.devops_agent,
            ],
            tasks=tasks,
            process=Process.sequential,  # Tasks execute in order
            verbose=True,
        )
        
        result = crew.kickoff()
        
        return f"""
Proyecto: {self.project_name}
Tipo: {self.project_type}
Ubicación: {self.output_dir / self.project_name}

{result}

✅ El proyecto ha sido creado exitosamente!

Próximos pasos:
1. Revisa la documentación en: {self.output_dir / self.project_name / 'README.md'}
2. Sigue la guía de instalación
3. Configura las variables de entorno
4. Ejecuta el proyecto localmente
5. Revisa la guía de deployment

¡Tu proyecto está listo para usar!
"""
