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
        
        # Create agents - each will use their recommended model automatically
        # Business Analyst & PM: Best with Claude 4.5 Sonnet (complex reasoning)
        # Backend/Frontend/DevOps: Best with GPT-5.1 Codex (code generation)
        # QA: Best with GPT-5.1 (general testing)
        self.pm_agent = create_project_manager_agent()  # -> claude-4.5-sonnet
        self.ba_agent = create_business_analyst_agent()  # -> claude-4.5-sonnet
        self.backend_agent = create_backend_developer_agent()  # -> gpt-5.1-codex
        self.frontend_agent = create_frontend_developer_agent()  # -> gpt-5.1-codex
        self.qa_agent = create_qa_engineer_agent()  # -> gpt-5.1
        self.devops_agent = create_devops_engineer_agent()  # -> gpt-5.1-codex
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_tasks(self) -> List[Task]:
        """Create tasks for the crew based on project type."""
        tasks = []
        
        # Task 1: Project Planning (PM)
        task_planning = Task(
            description=f"""
            Create a comprehensive project plan for: {self.project_name}
            Project Type: {self.project_type}
            Client Description: {self.description}
            
            Define:
            - Project scope and objectives
            - Timeline and milestones
            - Team coordination strategy
            - Risk assessment
            - Success criteria
            """,
            agent=self.pm_agent,
            expected_output="Detailed project plan with timeline, milestones, and risk assessment"
        )
        tasks.append(task_planning)
        
        # Task 2: Requirements Analysis (BA)
        task_requirements = Task(
            description=f"""
            Analyze requirements and create detailed specifications for: {self.project_name}
            Project Type: {self.project_type}
            Client Needs: {self.description}
            
            Deliver:
            - Functional requirements
            - User stories with acceptance criteria
            - Technical recommendations
            - Wireframe suggestions
            """,
            agent=self.ba_agent,
            expected_output="Complete requirements document with user stories and technical specifications",
            context=[task_planning]
        )
        tasks.append(task_requirements)
        
        # Task 3: Backend Design & Implementation
        if self.project_type in ['ecommerce', 'dashboard', 'api']:
            task_backend = Task(
                description=f"""
                Design and implement the backend system for: {self.project_name}
                
                Based on the requirements, create:
                - API architecture and endpoints
                - Database schema
                - Authentication system
                - Business logic implementation
                - API documentation
                
                Output directory: {self.output_dir / self.project_name / 'backend'}
                """,
                agent=self.backend_agent,
                expected_output="Complete backend implementation with API, database, and documentation",
                context=[task_requirements]
            )
            tasks.append(task_backend)
        
        # Task 4: Frontend Implementation
        if self.project_type in ['ecommerce', 'landing', 'dashboard']:
            backend_context = [task_backend] if self.project_type in ['ecommerce', 'dashboard'] else []
            
            task_frontend = Task(
                description=f"""
                Create the frontend application for: {self.project_name}
                Project Type: {self.project_type}
                
                Implement:
                - Responsive user interface
                - Component architecture
                - API integration (if backend exists)
                - Forms and validation
                - Navigation
                
                Output directory: {self.output_dir / self.project_name / 'frontend'}
                """,
                agent=self.frontend_agent,
                expected_output="Complete frontend application with responsive design and all features",
                context=[task_requirements] + backend_context
            )
            tasks.append(task_frontend)
        
        # Task 5: Testing & QA
        task_testing = Task(
            description=f"""
            Create and execute comprehensive tests for: {self.project_name}
            
            Provide:
            - Test plan
            - Unit tests
            - Integration tests
            - Test coverage report
            - Bug report (if any)
            - Quality assurance sign-off
            """,
            agent=self.qa_agent,
            expected_output="Complete test suite with coverage report and quality assessment",
            context=tasks[2:]  # All development tasks
        )
        tasks.append(task_testing)
        
        # Task 6: Deployment Setup
        task_deployment = Task(
            description=f"""
            Set up deployment infrastructure for: {self.project_name}
            
            Create:
            - Dockerfile(s)
            - docker-compose.yml
            - CI/CD pipeline (GitHub Actions)
            - Nginx configuration
            - Deployment documentation
            - Environment setup guide
            
            Output directory: {self.output_dir / self.project_name}
            """,
            agent=self.devops_agent,
            expected_output="Complete deployment configuration with Docker, CI/CD, and documentation",
            context=[task_testing]
        )
        tasks.append(task_deployment)
        
        # Task 7: Final Documentation & Handoff (PM)
        task_handoff = Task(
            description=f"""
            Create final project documentation and handoff package for: {self.project_name}
            
            Compile:
            - Complete project documentation
            - Setup and installation guide
            - User manual
            - Deployment guide
            - Maintenance recommendations
            - Future enhancement suggestions
            
            Output directory: {self.output_dir / self.project_name}
            """,
            agent=self.pm_agent,
            expected_output="Complete project documentation package ready for client handoff",
            context=tasks  # All previous tasks
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
