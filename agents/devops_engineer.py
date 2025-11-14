"""
DevOps Engineer Agent

Responsible for:
- Docker containerization
- CI/CD pipeline setup
- Deployment automation
- Server configuration
- Monitoring and logging
- Database deployment
- Security hardening
"""

from crewai import Agent
from typing import List, Optional


def create_devops_engineer_agent(tools: Optional[List] = None, verbose: bool = True, llm = None) -> Agent:
    """
    Create a DevOps Engineer agent specialized in deployment
    and infrastructure automation.
    
    Args:
        tools: List of tools available to the agent
        verbose: Whether to show detailed output
        llm: Language model to use (if None, will use default from environment)
        
    Returns:
        Agent: Configured DevOps Engineer agent
    """
    agent_config = {
        'role': 'Senior DevOps Engineer',
        'goal': 'Create automated, secure, and reliable deployment pipelines and infrastructure for web applications',
        'backstory': """You are a Senior DevOps Engineer with 6+ years of experience 
        in cloud infrastructure, containerization, and CI/CD automation. You specialize 
        in making deployment processes smooth, automated, and reliable for SMEs.
        
        Your expertise includes:
        - Docker and container orchestration
        - CI/CD pipelines (GitHub Actions, GitLab CI)
        - Cloud platforms (AWS, DigitalOcean, Heroku)
        - Nginx and reverse proxy configuration
        - SSL/TLS certificate management
        - Database deployment and backups
        - Environment configuration management
        - Monitoring and logging
        - Security best practices
        
        Your philosophy:
        - Automate everything possible
        - Infrastructure as Code
        - Security by default
        - Monitoring is essential
        - Simple solutions for SMEs
        - Cost-effective infrastructure
        - Easy rollback mechanisms
        
        You always consider:
        - Cost optimization (important for SMEs)
        - Scalability (room to grow)
        - Security (SSL, firewalls, secrets management)
        - Reliability (uptime, backups)
        - Simplicity (easy for small teams to maintain)
        - Documentation (clear deployment guides)
        
        Your approach for SMEs:
        - Docker for consistent environments
        - GitHub Actions for free CI/CD
        - DigitalOcean/Heroku for affordable hosting
        - Let's Encrypt for free SSL certificates
        - Simple but effective monitoring
        - Automated backups
        - Clear documentation for non-DevOps teams""",
        'tools': tools or [],
        'verbose': verbose,
        'allow_delegation': False,
        'max_iter': 20,
        'memory': True,
    }
    
    if llm is not None:
        agent_config['llm'] = llm
    
    return Agent(**agent_config)


def create_deployment_plan_task_description(
    requirements: str, 
    backend_implementation: str, 
    frontend_implementation: str
) -> str:
    """
    Generate a task description for creating a deployment plan.
    
    Args:
        requirements: Project requirements
        backend_implementation: Backend code summary
        frontend_implementation: Frontend code summary
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Create a comprehensive deployment plan based on:
    
    REQUIREMENTS:
    {requirements}
    
    BACKEND:
    {backend_implementation}
    
    FRONTEND:
    {frontend_implementation}
    
    Your deployment plan should include:
    
    1. INFRASTRUCTURE ARCHITECTURE
       - Hosting platform recommendation (with cost estimate)
       - Server specifications needed
       - Database hosting strategy
       - Static file hosting (for frontend)
       - Domain and DNS setup
    
    2. CONTAINERIZATION STRATEGY
       - Dockerfile for backend
       - Dockerfile for frontend (if needed)
       - Docker Compose for local development
       - Multi-stage builds for optimization
       - Environment variables management
    
    3. CI/CD PIPELINE
       - Trigger conditions (push to main, PR creation)
       - Build steps
       - Test execution
       - Deployment steps
       - Rollback mechanism
       - Notification setup
    
    4. ENVIRONMENT SETUP
       - Development environment
       - Staging environment (optional for budget)
       - Production environment
       - Environment variables needed
       - Secrets management
    
    5. DATABASE DEPLOYMENT
       - Database creation and migration
       - Backup strategy
       - Connection pooling
       - Migration rollback plan
    
    6. SSL/HTTPS CONFIGURATION
       - SSL certificate acquisition (Let's Encrypt)
       - Nginx configuration
       - HTTPS redirect
       - Security headers
    
    7. MONITORING & LOGGING
       - Application logs
       - Error tracking (optional: Sentry)
       - Uptime monitoring
       - Performance metrics
    
    8. SECURITY MEASURES
       - Firewall configuration
       - SSH key management
       - Rate limiting
       - Secrets rotation
       - Security headers
    
    9. BACKUP & DISASTER RECOVERY
       - Database backups (frequency, retention)
       - Code repository backups
       - Recovery procedures
       - Disaster recovery plan
    
    10. COST ESTIMATION
        - Monthly hosting costs
        - Domain costs
        - Third-party services
        - Total estimated monthly cost
    
    Format as a detailed deployment and infrastructure plan.
    """


def create_deployment_implementation_task_description(deployment_plan: str) -> str:
    """
    Generate a task description for implementing deployment.
    
    Args:
        deployment_plan: The deployment plan document
        
    Returns:
        str: Formatted task description
    """
    return f"""
    Implement the deployment infrastructure based on this plan:
    
    {deployment_plan}
    
    IMPLEMENTATION REQUIREMENTS:
    
    1. DOCKER CONFIGURATION
       
       A. Backend Dockerfile:
          - Multi-stage build
          - Python dependencies caching
          - Non-root user
          - Health check
          - Environment variables
       
       B. Frontend Dockerfile (if applicable):
          - Build stage
          - Production stage with Nginx
          - Optimized static files
       
       C. Docker Compose:
          - Backend service
          - Frontend service
          - Database service
          - Network configuration
          - Volume mounts
          - Environment files
    
    2. CI/CD PIPELINE (GitHub Actions)
       
       Create .github/workflows/main.yml with:
       
       A. Test Stage:
          - Checkout code
          - Set up Python/Node
          - Install dependencies
          - Run tests
          - Check coverage
       
       B. Build Stage:
          - Build Docker images
          - Tag with version
          - Push to registry (Docker Hub/GHCR)
       
       C. Deploy Stage:
          - SSH to server
          - Pull new images
          - Run database migrations
          - Restart containers
          - Health check
          - Rollback on failure
    
    3. SERVER CONFIGURATION
       
       A. Nginx Configuration:
          - Reverse proxy to backend
          - Serve frontend static files
          - SSL configuration
          - Gzip compression
          - Rate limiting
          - Security headers
       
       B. Environment Setup Script:
          - Install Docker
          - Install Docker Compose
          - Configure firewall
          - Set up SSL certificate
          - Create necessary directories
    
    4. DATABASE SETUP
       
       A. Migration Scripts:
          - Initial schema creation
          - Seed data (if needed)
          - Migration rollback scripts
       
       B. Backup Script:
          - Automated database backup
          - Backup rotation
          - Backup verification
    
    5. MONITORING SETUP
       
       A. Logging:
          - Application logs rotation
          - Error log aggregation
          - Log retention policy
       
       B. Health Checks:
          - Application health endpoint
          - Database connectivity check
          - Monitoring script
    
    6. DOCUMENTATION
       
       Create deployment documentation:
       - Initial server setup guide
       - Deployment process
       - Rollback procedure
       - Troubleshooting guide
       - Environment variables reference
       - Backup and restore guide
    
    7. SCRIPTS & AUTOMATION
       
       Provide scripts for:
       - One-command deployment
       - Database backup
       - Log rotation
       - SSL renewal
       - Health monitoring
    
    Provide complete, production-ready deployment configuration with clear 
    documentation and automation scripts. Include cost-effective solutions 
    suitable for small businesses.
    """
