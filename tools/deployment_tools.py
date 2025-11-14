"""
Deployment Tools

Tools for Docker containerization, CI/CD setup, and deployment automation.
"""

from crewai_tools import tool
from typing import Optional, Dict
from pathlib import Path


@tool("Generate Dockerfile Tool")
def generate_dockerfile(
    project_type: str,
    python_version: str = "3.11",
    port: int = 5000
) -> str:
    """
    Generate a Dockerfile for the project.
    
    Args:
        project_type: Type of project ('flask', 'fastapi', 'react')
        python_version: Python version to use
        port: Port to expose
        
    Returns:
        str: Dockerfile content
    """
    if project_type.lower() in ['flask', 'fastapi']:
        return f"""# Multi-stage Dockerfile for {project_type}

# Build stage
FROM python:{python_version}-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:{python_version}-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE {port}

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:{port}/health')" || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "--workers", "4", "run:app"]
"""
    elif project_type.lower() == 'react':
        return f"""# Multi-stage Dockerfile for React

# Build stage
FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Runtime stage with nginx
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
"""
    else:
        return f"Unknown project type: {project_type}"


@tool("Generate Docker Compose Tool")
def generate_docker_compose(
    has_backend: bool = True,
    has_frontend: bool = True,
    has_database: bool = True
) -> str:
    """
    Generate docker-compose.yml file.
    
    Args:
        has_backend: Include backend service
        has_frontend: Include frontend service
        has_database: Include database service
        
    Returns:
        str: docker-compose.yml content
    """
    services = {}
    
    if has_database:
        services['db'] = """  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-app_db}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
"""
    
    if has_backend:
        depends_on = "    depends_on:\n      - db\n" if has_database else ""
        services['backend'] = f"""  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://${{DB_USER:-postgres}}:${{DB_PASSWORD:-postgres}}@db:5432/${{DB_NAME:-app_db}}
      SECRET_KEY: ${{SECRET_KEY:-dev-secret-key}}
    volumes:
      - ./backend:/app
{depends_on}    networks:
      - app_network
"""
    
    if has_frontend:
        depends_on = "    depends_on:\n      - backend\n" if has_backend else ""
        services['frontend'] = f"""  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    environment:
      REACT_APP_API_URL: http://localhost:5000
{depends_on}    networks:
      - app_network
"""
    
    compose_content = f"""version: '3.8'

services:
{chr(10).join(services.values())}

networks:
  app_network:
    driver: bridge

{"volumes:" if has_database else ""}
{"  postgres_data:" if has_database else ""}
"""
    
    return compose_content


@tool("Generate GitHub Actions Workflow Tool")
def generate_github_actions(
    project_type: str,
    run_tests: bool = True,
    deploy: bool = False
) -> str:
    """
    Generate GitHub Actions CI/CD workflow.
    
    Args:
        project_type: 'python' or 'javascript' or 'full-stack'
        run_tests: Include test step
        deploy: Include deployment step
        
    Returns:
        str: GitHub Actions workflow YAML content
    """
    workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
"""
    
    if project_type in ['python', 'full-stack']:
        workflow += """
  test-backend:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
"""
        
        if run_tests:
            workflow += """    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
"""
    
    if project_type in ['javascript', 'full-stack']:
        workflow += """
  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
      working-directory: ./frontend
"""
        
        if run_tests:
            workflow += """    
    - name: Run tests
      run: npm test -- --coverage --watchAll=false
      working-directory: ./frontend
    
    - name: Build
      run: npm run build
      working-directory: ./frontend
"""
    
    if deploy:
        workflow += """
  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      env:
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        SERVER_HOST: ${{ secrets.SERVER_HOST }}
      run: |
        echo "Deploying to production..."
        # Add your deployment script here
"""
    
    return workflow


@tool("Generate Nginx Config Tool")
def generate_nginx_config(
    backend_port: int = 5000,
    frontend_port: int = 80,
    domain: str = "example.com"
) -> str:
    """
    Generate Nginx configuration for reverse proxy.
    
    Args:
        backend_port: Backend application port
        frontend_port: Frontend application port
        domain: Domain name
        
    Returns:
        str: Nginx configuration content
    """
    return f"""# Nginx configuration for {domain}

upstream backend {{
    server backend:{backend_port};
}}

server {{
    listen 80;
    server_name {domain} www.{domain};
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {domain} www.{domain};
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Frontend static files
    location / {{
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        
        # Caching for static assets
        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {{
            expires 1y;
            add_header Cache-Control "public, immutable";
        }}
    }}
    
    # API proxy
    location /api {{
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }}
    
    # Health check endpoint
    location /health {{
        access_log off;
        return 200 "healthy\\n";
        add_header Content-Type text/plain;
    }}
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
}}
"""


class DockerTool:
    """Wrapper class for Docker-related tools."""
    
    @staticmethod
    def dockerfile(project_type: str, python_version: str = "3.11", port: int = 5000) -> str:
        return generate_dockerfile(project_type, python_version, port)
    
    @staticmethod
    def compose(has_backend: bool = True, has_frontend: bool = True, has_database: bool = True) -> str:
        return generate_docker_compose(has_backend, has_frontend, has_database)


class CICDTool:
    """Tool for CI/CD configuration."""
    
    @staticmethod
    def github_actions(project_type: str, run_tests: bool = True, deploy: bool = False) -> str:
        return generate_github_actions(project_type, run_tests, deploy)
    
    @staticmethod
    def nginx_config(backend_port: int = 5000, frontend_port: int = 80, domain: str = "example.com") -> str:
        return generate_nginx_config(backend_port, frontend_port, domain)
