"""
Code Generation Tools

Tools for generating boilerplate code, project structures,
and common patterns for web applications.
"""

from crewai_tools import tool
from typing import Dict, List, Optional
import os
from pathlib import Path


@tool("Flask App Generator")
def generate_flask_app(project_name: str, features: List[str]) -> str:
    """
    Generate Flask application structure with specified features.
    
    Args:
        project_name: Name of the project
        features: List of features (e.g., ['auth', 'database', 'api'])
        
    Returns:
        str: Description of generated structure
    """
    structure = {
        "app": {
            "__init__.py": _flask_init_content(features),
            "models": {
                "__init__.py": "",
            },
            "routes": {
                "__init__.py": "",
            },
            "services": {
                "__init__.py": "",
            },
            "utils": {
                "__init__.py": "",
            },
        },
        "config": {
            "__init__.py": "",
            "settings.py": _flask_config_content(),
        },
        "tests": {
            "__init__.py": "",
            "conftest.py": _pytest_conftest_content(),
        },
        "requirements.txt": _flask_requirements(features),
        "run.py": _flask_run_content(project_name),
        ".env.example": _flask_env_content(),
        "README.md": f"# {project_name}\n\nFlask application",
    }
    
    return f"""
    Generated Flask project structure for: {project_name}
    
    Features: {', '.join(features)}
    
    Structure:
    {project_name}/
    ├── app/
    │   ├── __init__.py
    │   ├── models/
    │   ├── routes/
    │   ├── services/
    │   └── utils/
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    ├── tests/
    │   ├── __init__.py
    │   └── conftest.py
    ├── requirements.txt
    ├── run.py
    ├── .env.example
    └── README.md
    
    Next steps:
    1. Create virtual environment: python -m venv venv
    2. Activate it: .\\venv\\Scripts\\Activate.ps1
    3. Install dependencies: pip install -r requirements.txt
    4. Copy .env.example to .env and configure
    5. Run: python run.py
    """


def _flask_init_content(features: List[str]) -> str:
    """Generate Flask app __init__.py content."""
    has_db = 'database' in features or 'db' in features
    has_jwt = 'auth' in features or 'jwt' in features
    
    content = '''"""
Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
'''
    
    if has_db:
        content += "from flask_sqlalchemy import SQLAlchemy\n"
    if has_jwt:
        content += "from flask_jwt_extended import JWTManager\n"
    
    content += '''
# Initialize extensions
'''
    
    if has_db:
        content += "db = SQLAlchemy()\n"
    if has_jwt:
        content += "jwt = JWTManager()\n"
    
    content += '''

def create_app(config_name='development'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'config.settings.{config_name.capitalize()}Config')
    
    # Initialize extensions
    CORS(app)
'''
    
    if has_db:
        content += "    db.init_app(app)\n"
    if has_jwt:
        content += "    jwt.init_app(app)\n"
    
    content += '''
    
    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    return app
'''
    
    return content


def _flask_config_content() -> str:
    """Generate Flask configuration content."""
    return '''"""
Configuration settings for Flask application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/dev_db'
    )


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/test_db'
'''


def _flask_requirements(features: List[str]) -> str:
    """Generate requirements.txt content."""
    base_requirements = [
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "python-dotenv>=1.0.0",
        "gunicorn>=21.2.0",
    ]
    
    if 'database' in features or 'db' in features:
        base_requirements.extend([
            "flask-sqlalchemy>=3.1.0",
            "psycopg2-binary>=2.9.9",
            "alembic>=1.13.0",
        ])
    
    if 'auth' in features or 'jwt' in features:
        base_requirements.extend([
            "flask-jwt-extended>=4.5.0",
            "passlib[bcrypt]>=1.7.4",
        ])
    
    if 'testing' in features or True:  # Always include testing
        base_requirements.extend([
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ])
    
    return "\n".join(sorted(base_requirements))


def _flask_run_content(project_name: str) -> str:
    """Generate run.py content."""
    return f'''"""
Run the Flask application
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''


def _flask_env_content() -> str:
    """Generate .env.example content."""
    return '''# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/your_db_name

# Environment
FLASK_ENV=development
'''


def _pytest_conftest_content() -> str:
    """Generate pytest conftest.py content."""
    return '''"""
Pytest configuration and fixtures
"""
import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
'''


@tool("React App Generator")
def generate_react_app(project_name: str, features: List[str]) -> str:
    """
    Generate React application structure with specified features.
    
    Args:
        project_name: Name of the project
        features: List of features (e.g., ['router', 'api', 'auth'])
        
    Returns:
        str: Description of generated structure
    """
    return f"""
    Generated React project structure for: {project_name}
    
    Features: {', '.join(features)}
    
    To create the project, run:
    
    ```bash
    # Using Vite (recommended)
    npm create vite@latest {project_name} -- --template react
    cd {project_name}
    npm install
    ```
    
    Additional packages to install based on features:
    
    {'npm install react-router-dom' if 'router' in features else ''}
    {'npm install axios' if 'api' in features else ''}
    {'npm install -D tailwindcss postcss autoprefixer' if 'tailwind' in features else ''}
    
    Recommended structure:
    {project_name}/
    ├── src/
    │   ├── components/
    │   │   ├── common/
    │   │   └── features/
    │   ├── pages/
    │   ├── services/
    │   │   └── api.js
    │   ├── hooks/
    │   ├── context/
    │   ├── utils/
    │   ├── App.jsx
    │   └── main.jsx
    ├── public/
    ├── package.json
    └── vite.config.js
    
    Next steps:
    1. npm install
    2. Configure Tailwind (if needed)
    3. Set up API service
    4. Create components
    5. npm run dev
    """


class CodeGeneratorTool:
    """Wrapper class for code generation tools."""
    
    @staticmethod
    def flask_app(project_name: str, features: List[str]) -> str:
        return generate_flask_app(project_name, features)
    
    @staticmethod
    def react_app(project_name: str, features: List[str]) -> str:
        return generate_react_app(project_name, features)


class FlaskAppGenerator:
    """Legacy wrapper for Flask app generation."""
    pass


class ReactAppGenerator:
    """Legacy wrapper for React app generation."""
    pass
