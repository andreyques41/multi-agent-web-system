# 🤖 Multi-Agent Web Development System

Sistema multi-agente especializado en desarrollo de proyectos web para pequeñas y medianas empresas (PyMEs).

## 📋 Descripción

Este sistema utiliza agentes de IA especializados que trabajan en equipo para desarrollar proyectos web completos, desde el análisis de requisitos hasta el deployment. Ideal para:

- 🏪 E-commerce para pequeños negocios
- 📱 Landing pages corporativas
- 📊 Dashboards y sistemas de gestión
- 🔌 APIs y backends
- 🎨 Sitios web responsive

## 🎯 Agentes Especializados

### 1. **Business Analyst Agent**
- Análisis de requisitos del cliente
- Definición de funcionalidades
- Creación de user stories
- Estimación de proyectos

### 2. **Backend Developer Agent**
- Desarrollo de APIs REST
- Bases de datos (PostgreSQL, MySQL)
- Autenticación y seguridad
- Lógica de negocio

### 3. **Frontend Developer Agent**
- Interfaces de usuario modernas
- React, Vue, o HTML/CSS/JS vanilla
- Responsive design
- Integración con APIs

### 4. **QA Engineer Agent**
- Testing automatizado
- Pruebas de integración
- Validación de requisitos
- Reportes de bugs

### 5. **DevOps Agent**
- Configuración de servidores
- CI/CD pipelines
- Docker containers
- Deployment automation

### 6. **Project Manager Agent**
- Coordinación del equipo
- Timelines y milestones
- Documentación del proyecto
- Comunicación con stakeholders

## 🚀 Instalación

### Prerrequisitos
- Python 3.10+
- Git
- Node.js (opcional, para proyectos frontend)
- Docker (opcional, para deployment)

### 🚀 Inicio Rápido

**📘 Guía completa de instalación:** [docs/QUICKSTART.md](docs/QUICKSTART.md)

```bash
# Clonar el repositorio
git clone https://github.com/andreyques41/multi-agent-web-dev.git
cd multi-agent-web-dev

# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

### Configuración de API Keys

Tienes **3 opciones** de proveedores de IA:

#### **Opción 1: GitHub Models (RECOMENDADO - GRATIS)** ⭐

Si tienes GitHub Copilot, usa modelos premium sin costo:

```env
LLM_PROVIDER=github
GITHUB_TOKEN=tu-github-token-aqui
GITHUB_MODEL=gpt-5.1-codex  # Recomendado para desarrollo
```

**Modelos disponibles (Noviembre 2025):**
- `gpt-5.1-codex`, `gpt-5.1`, `gpt-5-codex`, `gpt-5` - Serie GPT-5
- `claude-4.5-sonnet`, `claude-4-sonnet` - Serie Claude 4
- `gpt-4o`, `gpt-4o-mini`, `gpt-4` - Serie GPT-4 (legacy)
- `claude-3.5-sonnet` - Claude 3.5 (legacy)

**Ver instrucciones completas:** [docs/SETUP_GITHUB_MODELS.md](docs/SETUP_GITHUB_MODELS.md)

#### **Opción 2: OpenAI**

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=tu-api-key-aqui
OPENAI_MODEL=gpt-5.1-codex
```

#### **Opción 3: Anthropic Claude**

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=tu-api-key-aqui
ANTHROPIC_MODEL=claude-4.5-sonnet
```

**Configuración opcional:**
```env
SERPER_API_KEY=tu-api-key-aqui  # Para búsquedas web
```

## 💻 Uso Básico

### Ejemplo 1: Crear un E-commerce

```bash
python main.py --project ecommerce --name "Tienda de Ropa Online"
```

### Ejemplo 2: Landing Page Corporativa

```bash
python main.py --project landing --name "Consultora XYZ"
```

### Ejemplo 3: Dashboard de Gestión

```bash
python main.py --project dashboard --name "Panel Admin Inventario"
```

## 📁 Estructura del Proyecto

```
multi-agent-web-dev/
├── agents/              # Definición de agentes especializados
│   ├── business_analyst.py
│   ├── backend_dev.py
│   ├── frontend_dev.py
│   ├── qa_engineer.py
│   ├── devops.py
│   └── project_manager.py
├── crews/               # Equipos de trabajo por tipo de proyecto
│   ├── ecommerce_crew.py
│   ├── landing_crew.py
│   ├── dashboard_crew.py
│   └── api_crew.py
├── tools/               # Herramientas disponibles para los agentes
│   ├── code_generator.py
│   ├── file_operations.py
│   ├── web_research.py
│   ├── testing_tools.py
│   └── deployment_tools.py
├── templates/           # Templates base para proyectos
│   ├── ecommerce/
│   ├── landing/
│   ├── dashboard/
│   └── api/
├── examples/            # Ejemplos de uso
├── output/              # Proyectos generados
└── main.py             # Punto de entrada principal
```

## 🛠️ Tecnologías Stack

### Backend
- Python/Flask
- FastAPI
- PostgreSQL
- JWT Authentication

### Frontend
- React.js
- Tailwind CSS
- HTML/CSS/JavaScript vanilla

### DevOps
- Docker
- GitHub Actions
- Nginx

## 📖 Documentación

### 🚀 Guías de Inicio
- **[Inicio Rápido](docs/QUICKSTART.md)** - Instalación y configuración paso a paso
- **[Configurar GitHub Models](docs/SETUP_GITHUB_MODELS.md)** - Usar modelos gratis con Copilot
- **[Estructura del Proyecto](docs/STRUCTURE.md)** - Organización de archivos y carpetas

### 🧠 Guías Técnicas
- **[Estrategia de Modelos](docs/MODEL_STRATEGY.md)** - Cómo elegir el mejor modelo para cada agente
- [Guía de Agentes](docs/agents.md) *(próximamente)*
- [Configuración de Crews](docs/crews.md) *(próximamente)*
- [Tools Disponibles](docs/tools.md) *(próximamente)*

### 💡 Recursos Adicionales
- [Ejemplos de Proyectos](examples/README.md)
- [Templates de Proyectos](docs/templates.md) *(próximamente)*

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Andrey Ques**
- GitHub: [@andreyques41](https://github.com/andreyques41)

## 🙏 Agradecimientos

- CrewAI por el framework de agentes
- OpenAI por los modelos GPT
- La comunidad de desarrollo de software con IA

---

⭐ Si este proyecto te fue útil, dale una estrella en GitHub!
