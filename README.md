# Multi-Agent Web Development System

> AI-powered automation for generating complete web projects using specialized agent teams

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Framework-purple.svg)](https://crewai.com)
[![GitHub Models](https://img.shields.io/badge/GitHub%20Models-API-black.svg)](https://github.com/marketplace/models)

## 📋 Overview

A **multi-agent AI system** that orchestrates specialized agents to collaboratively generate complete web development projects. Built with CrewAI, this system demonstrates agent-based workflow automation, prompt engineering, and AI-assisted software development.

### Problem Statement

Creating web projects involves coordinating multiple specialized roles:
- Business analysis and requirements gathering
- Backend API development
- Frontend implementation
- Quality assurance and testing
- DevOps and deployment configuration

Traditionally, this requires significant human coordination and time.

### Solution

An AI agent crew where each agent has specialized expertise:

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT MANAGER                           │
│               (Orchestration & Planning)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌──────────┐        ┌──────────┐          ┌──────────┐
│ Business │        │ Backend  │          │ Frontend │
│ Analyst  │        │Developer │          │Developer │
└──────────┘        └──────────┘          └──────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌──────────┐        ┌──────────┐          ┌──────────┐
│   QA     │        │  DevOps  │          │  Output  │
│Engineer  │        │ Engineer │          │ Project  │
└──────────┘        └──────────┘          └──────────┘
```

---

## 🏗️ Architecture

### Agent Roles

| Agent | Responsibility | Output |
|-------|---------------|--------|
| **Project Manager** | High-level planning, timeline, milestones | `docs/PROJECT_PLAN.md` |
| **Business Analyst** | Requirements analysis, user stories | `docs/REQUIREMENTS.md` |
| **Backend Developer** | API design, database models, auth | `backend/` directory |
| **Frontend Developer** | UI components, routing, styling | `frontend/` directory |
| **QA Engineer** | Test suites, coverage configuration | `tests/` directory |
| **DevOps Engineer** | Docker, CI/CD, deployment configs | `Dockerfile`, `docker-compose.yml` |

### Task Flow

```
Task 1: Planning (PM)
    │
    ▼
Task 2: Requirements (BA) ──────► context: Task 1
    │
    ├─────────────────────────┐
    ▼                         ▼
Task 3: Backend           Task 4: Frontend
(context: Task 2)         (context: Task 2)
    │                         │
    └─────────┬───────────────┘
              ▼
        Task 5: Testing (context: Task 3, 4)
              │
              ▼
        Task 6: DevOps (context: all)
```

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **CrewAI framework** | Mature agent orchestration with task dependencies |
| **GitHub Models API** | Free tier with GPT-4o access via Copilot subscription |
| **Token management** | Custom `TaskOutputManager` prevents 413 payload errors |
| **Modular agents** | Each agent defined separately for maintainability |
| **Project-scoped file tools** | Custom `ProjectFileWriter` ensures correct output paths |

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | CrewAI |
| **Language** | Python 3.10+ |
| **LLM Provider** | GitHub Models (OpenAI-compatible) |
| **CLI** | Rich (terminal UI) |
| **Configuration** | python-dotenv |

---

## 📦 Project Templates

| Template | Description | Generated Structure |
|----------|-------------|---------------------|
| `landing` | Corporate landing page | Frontend + basic backend |
| `ecommerce` | E-commerce platform | Full-stack with auth, cart, products |
| `dashboard` | Admin dashboard | Data visualization, CRUD operations |
| `api` | REST API only | Backend with documented endpoints |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- GitHub Copilot subscription (for GitHub Models API)
- OR OpenAI/Anthropic API key

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR-GITHUB/multi-agent-web-system
cd multi-agent-web-system

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API credentials
```

### Configuration

```env
# Option 1: GitHub Models (Recommended - Free with Copilot)
GITHUB_TOKEN=ghp_your_github_token

# Option 2: OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Option 3: Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
```

### Usage

```bash
# Create a landing page project
python main.py create "MyCompany" --project landing

# Create an e-commerce project
python main.py create "PetShop" --project ecommerce

# Enable verbose logging
python main.py create "Dashboard" --project dashboard --verbose

# List available templates
python main.py templates
```

### Generated Output

```
output/MyCompany/
├── docs/
│   ├── PROJECT_PLAN.md
│   └── REQUIREMENTS.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── auth.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   ├── index.html
│   └── package.json
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🧪 Example Output

The system has been tested to generate functional projects. See [output/TestRetry](output/TestRetry) for a complete example including:

- Flask backend with JWT authentication
- React/Vite frontend with Tailwind CSS
- Docker containerization
- GitHub Actions CI/CD workflow
- Comprehensive test suite

---

## 📊 Project Status

| Feature | Status |
|---------|--------|
| Agent definitions | ✅ Complete (6 agents) |
| Task orchestration | ✅ Complete |
| File generation | ✅ Complete |
| Token management | ✅ Complete |
| Landing template | ✅ Tested |
| E-commerce template | ✅ Tested |
| Dashboard template | 🔄 In Progress |
| API-only template | ⏳ Planned |

---

## 🎯 What This Demonstrates

### AI Engineering Skills
- **Agent Design**: Specialized agents with distinct personas and capabilities
- **Prompt Engineering**: Task descriptions optimized for consistent output
- **Token Management**: Preventing API errors with context size management
- **LLM Integration**: OpenAI-compatible endpoint configuration

### Software Engineering Skills
- **Modular Architecture**: Agents, tools, and utilities cleanly separated
- **CLI Design**: Rich terminal interface with progress indicators
- **Error Handling**: Graceful degradation with informative messages
- **Configuration Management**: Environment-based provider selection

### Innovation
- **Multi-model support**: Seamlessly switch between OpenAI, Anthropic, GitHub Models
- **Context optimization**: Only pass necessary context between dependent tasks
- **Custom tooling**: Project-scoped file writer ensures correct output structure

---

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Model Strategy](docs/MODEL_STRATEGY.md) - LLM provider selection
- [GitHub Models Setup](docs/SETUP_GITHUB_MODELS.md)
- [Project Structure](docs/STRUCTURE.md)
- [Debugging Guide](docs/DEBUGGING.md)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

*Built to explore AI-assisted development workflows and agent-based automation.*