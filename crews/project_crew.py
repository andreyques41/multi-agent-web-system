"""
Project Crew

Main crew that coordinates all agents to work together on a web development project.
"""

from crewai import Crew, Task, Process
from typing import List, Optional
from pathlib import Path
from crewai.tools import tool

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
        
        # Convert output_dir to absolute path relative to this file's location
        if Path(output_dir).is_absolute():
            self.output_dir = Path(output_dir)
        else:
            # Get the directory where this file (project_crew.py) is located
            current_file = Path(__file__).parent.parent  # Go up to multi-agent-web-dev root
            self.output_dir = current_file / output_dir
        
        self.description = description or f"A {project_type} project for small/medium business"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create project-specific directory
        self.project_dir = self.output_dir / self.project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize token manager to prevent 413 errors
        self.token_manager = TaskOutputManager(model="gpt-4o")
        
        # Create a custom file writer tool that ALWAYS saves in project directory
        @tool("ProjectFileWriter")
        def project_file_writer(filename: str, content: str) -> str:
            """
            Write content to a file in the project directory.
            
            Args:
                filename: Path to the file (relative to project root)
                content: Content to write to the file
            
            Returns:
                Success message with file path
            """
            file_path = self.project_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            return f"File successfully written to {file_path}"
        
        # Use custom tool instead of default FileWriterTool
        self.file_tools = [project_file_writer]
        
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
            YOU MUST CREATE ACTUAL FILES using the ProjectFileWriter tool.
            
            Create a professional business project plan for: {self.project_name}
            Project Type: {self.project_type}
            
            Save to: filename: "docs/PROJECT_PLAN.md"
            
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
            expected_output="Professional project plan in markdown format saved to docs/PROJECT_PLAN.md",
            context=[]  # Explicitly set to empty - no previous context
        )
        tasks.append(task_planning)
        
        # Task 2: Requirements Analysis (BA)
        # ONLY receives Task 1 context (project plan)
        task_requirements = Task(
            description=safety_prefix + f"""
            YOU MUST CREATE ACTUAL FILES using the ProjectFileWriter tool.
            
            Create technical requirements for a BUSINESS {self.project_type} application: {self.project_name}
            
            Save to: filename: "docs/REQUIREMENTS.md"
            
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
            expected_output="Technical requirements document in markdown format saved to docs/REQUIREMENTS.md",
            context=[task_planning]  # Only needs project plan
        )
        tasks.append(task_requirements)
        
        # Task 3: Backend Design & Implementation
        # ONLY receives Task 2 context (requirements) - skips Task 1
        if self.project_type in ['ecommerce', 'dashboard', 'api', 'landing']:
            task_backend = Task(
                description=safety_prefix + f"""
                Create a COMPLETE FUNCTIONAL backend for business {self.project_type}: {self.project_name}
                
                YOU MUST CREATE ACTUAL FILES using the ProjectFileWriter tool.
                
                Create these files (filename parameter is relative to project root):
                
                1. filename: "backend/app/main.py", content: Main Flask/FastAPI application with 3 REST endpoints
                2. filename: "backend/app/models.py", content: SQLAlchemy models (User, main business entity)
                3. filename: "backend/app/routes.py", content: API routes and controllers
                4. filename: "backend/app/auth.py", content: JWT authentication implementation
                5. filename: "backend/requirements.txt", content: Python dependencies list
                6. filename: "backend/.env.example", content: Environment variables template
                7. filename: "backend/README.md", content: Setup and API documentation
                
                Use Python with Flask OR FastAPI framework.
                Database: PostgreSQL with SQLAlchemy ORM.
                Include proper error handling, validation, and JWT auth.
                
                CREATE REAL, WORKING CODE - not documentation.
                Each file should be production-ready and functional.
                """,
                agent=self.backend_agent,
                expected_output="Complete backend application with all files created",
                context=[task_requirements]  # Only needs requirements, not project plan
            )
            tasks.append(task_backend)
        
        # Task 4: Frontend Implementation
        # ONLY receives Task 2 context (requirements) - skips Task 1 and 3
        if self.project_type in ['ecommerce', 'landing', 'dashboard']:
            task_frontend = Task(
                description=safety_prefix + f"""
                Create a COMPLETE FUNCTIONAL frontend for business {self.project_type}: {self.project_name}
                
                YOU MUST CREATE ACTUAL FILES using the ProjectFileWriter tool.
                
                Create these files (filename parameter is relative to project root):
                
                1. filename: "frontend/index.html", content: HTML entry point with <!DOCTYPE html>, <div id="root"></div>, and <script type="module" src="/src/main.jsx"></script>
                2. filename: "frontend/src/main.jsx", content: React entry point using ReactDOM.createRoot(document.getElementById('root')).render(<App />)
                3. filename: "frontend/src/App.jsx", content: Main React component with Header, main content, and Footer
                4. filename: "frontend/src/components/Header.jsx", content: Professional header with navigation
                5. filename: "frontend/src/components/Footer.jsx", content: Professional footer component
                6. filename: "frontend/src/pages/Home.jsx", content: Home page with hero section and features
                7. filename: "frontend/src/styles/main.css", content: Main styles with @tailwind directives
                8. filename: "frontend/vite.config.js", content: Vite configuration with React plugin and server port 3000
                9. filename: "frontend/tailwind.config.js", content: Tailwind config with content paths for HTML and JSX files
                10. filename: "frontend/postcss.config.js", content: PostCSS config with tailwindcss and autoprefixer plugins
                11. filename: "frontend/package.json", content: Complete package.json with "type": "module", scripts (dev, build, preview), dependencies (react, react-dom), devDependencies (vite, @vitejs/plugin-react, tailwindcss, postcss, autoprefixer)
                12. filename: "frontend/.env.example", content: Environment variables (VITE_API_URL, etc.)
                13. filename: "frontend/README.md", content: Setup instructions with npm install and npm run dev
                
                Use React 18+ with Vite 5+ as bundler.
                Styling: Tailwind CSS 3+ with PostCSS.
                Include responsive design, professional UI, and proper component structure.
                
                CREATE REAL, WORKING CODE - not documentation.
                Each file should be production-ready and functional.
                The project MUST run with: npm install && npm run dev
                """,
                agent=self.frontend_agent,
                expected_output="Complete frontend application with all files created",
                context=[task_requirements]  # Only needs requirements, not backend details
            )
            tasks.append(task_frontend)
        
        # Task 5: Testing & QA
        # Receives ONLY requirements (Task 2) - NO implementation details
        task_testing = Task(
            description=safety_prefix + f"""
            Create COMPLETE TEST SUITE for business application: {self.project_name}
            
            YOU MUST CREATE ACTUAL TEST FILES using the ProjectFileWriter tool.
            
            Create these files (filename parameter is relative to project root):
            
            1. filename: "tests/test_api.py", content: Unit tests for backend API endpoints (pytest)
            2. filename: "tests/test_auth.py", content: Unit tests for authentication logic
            3. filename: "tests/test_models.py", content: Unit tests for database models
            4. filename: "tests/test_integration.py", content: Integration test for main workflow
            5. filename: "tests/conftest.py", content: Pytest configuration and fixtures
            6. filename: "tests/requirements.txt", content: Testing dependencies
            7. filename: "tests/README.md", content: How to run tests and coverage
            
            Use pytest for Python backend tests.
            Include unit tests, integration tests, and fixtures.
            Focus on: Authentication, data validation, API responses, business logic.
            
            CREATE REAL, WORKING TEST CODE - not documentation.
            Each file should be production-ready and executable.
            """,
            agent=self.qa_agent,
            expected_output="Complete test suite with all test files created",
            context=[task_requirements]  # Only needs requirements to test against
        )
        tasks.append(task_testing)
        
        # Task 6: Deployment Setup
        # NO CONTEXT - deployment config is independent
        task_deployment = Task(
            description=safety_prefix + f"""
            Create COMPLETE DEPLOYMENT configuration for business {self.project_type}: {self.project_name}
            
            YOU MUST CREATE ACTUAL FILES using the ProjectFileWriter tool.
            
            Create these files (filename parameter is relative to project root):
            
            1. filename: "Dockerfile", content: Multi-stage Docker build: Stage 1 builds with 'npm run build' (outputs to /app/dist), Stage 2 copies from /app/dist to nginx /usr/share/nginx/html
            2. filename: "docker-compose.yml", content: Services: web app + PostgreSQL database
            3. filename: ".github/workflows/ci-cd.yml", content: GitHub Actions workflow for CI/CD
            4. filename: ".env.example", content: Environment variables template for deployment
            5. filename: "deployment/README.md", content: Deployment instructions and guide
            
            Include:
            - Production-ready Dockerfile with proper optimization
            - docker-compose with health checks and volumes
            - CI/CD pipeline with build, test, and deploy steps
            - Clear deployment instructions for AWS/GCP/Docker
            
            CREATE REAL, WORKING CONFIG FILES - not documentation.
            Each file should be production-ready and functional.
            """,
            agent=self.devops_agent,
            expected_output="Complete deployment configuration with all files created",
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
        
        # Add step callbacks to truncate outputs and save summary files
        def create_task_callback(task_name, summary_filename=None):
            """Create a callback for a specific task."""
            def callback(output):
                """Callback to truncate task output and optionally save summary."""
                if hasattr(output, 'raw'):
                    raw_output = str(output.raw)
                else:
                    raw_output = str(output)
                
                # Store output
                task_outputs[task_name] = raw_output
                
                # Save summary file if specified (for documentation tasks)
                # The actual project files are created by agents using FileWriterTool
                if summary_filename:
                    file_path = self.project_dir / summary_filename
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_text(raw_output, encoding='utf-8')
                    print(f"✅ Saved summary: {summary_filename}")
                
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
        
        # Apply callbacks to tasks
        # Note: Agents will create actual files using FileWriterTool
        # These callbacks only save summary/documentation files
        task_file_mapping = {
            0: ('planning', 'docs/PROJECT_PLAN.md'),
            1: ('requirements', 'docs/REQUIREMENTS.md'),
            2: ('backend', None),  # Backend creates its own files
            3: ('frontend', None),  # Frontend creates its own files
            4: ('testing', None),  # Testing creates its own files
            5: ('deployment', None),  # Deployment creates its own files
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
