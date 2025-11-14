# 📁 Estructura del Proyecto

Esta guía explica la organización de archivos y carpetas del sistema multi-agente.

## 🌳 Árbol de Directorios

```
multi-agent-web-dev/
├── .vscode/                  # Configuración de VS Code
│   └── settings.json         # Intérprete Python y formateo
│
├── agents/                   # Agentes especializados
│   ├── __init__.py
│   ├── business_analyst.py   # Análisis de requisitos
│   ├── project_manager.py    # Planificación y coordinación
│   ├── backend_developer.py  # Desarrollo backend
│   ├── frontend_developer.py # Desarrollo frontend
│   ├── devops_engineer.py    # Deployment y CI/CD
│   └── qa_engineer.py        # Testing y QA
│
├── crews/                    # Orquestación de agentes
│   ├── __init__.py
│   └── project_crew.py       # Crew principal del proyecto
│
├── docs/                     # 📚 Documentación
│   ├── MODEL_STRATEGY.md     # Estrategia de selección de modelos
│   ├── QUICKSTART.md         # Guía de inicio rápido
│   └── SETUP_GITHUB_MODELS.md # Configuración de GitHub Models
│
├── examples/                 # 💡 Ejemplos de proyectos
│   └── README.md             # Descripción de ejemplos
│
├── output/                   # 📦 Proyectos generados (gitignored)
│   └── README.md             # Explicación de la carpeta
│
├── tools/                    # 🛠️ Herramientas para agentes
│   ├── __init__.py
│   ├── code_generator.py     # Generación de código
│   ├── deployment_tools.py   # Herramientas de deployment
│   ├── file_operations.py    # Operaciones de archivos
│   ├── testing_tools.py      # Herramientas de testing
│   └── web_research.py       # Búsqueda web
│
├── utils/                    # 🔧 Utilidades
│   ├── __init__.py
│   └── llm_config.py         # Configuración de modelos LLM
│
├── .env                      # Variables de entorno (gitignored)
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos ignorados por Git
├── LICENSE                   # Licencia MIT
├── main.py                   # 🚀 CLI principal
├── README.md                 # Documentación principal
└── requirements.txt          # Dependencias Python
```

## 📂 Descripción de Carpetas

### `/agents`
Contiene los 6 agentes especializados del sistema. Cada agente tiene:
- Configuración de rol, objetivos y backstory
- Funciones para crear tareas específicas
- Soporte para selección de modelo LLM personalizado

**Modelos recomendados por agente:**
- Business Analyst & PM → `claude-4.5-sonnet`
- Backend, Frontend, DevOps → `gpt-5.1-codex`
- QA Engineer → `gpt-5.1`

### `/crews`
Define cómo los agentes trabajan en equipo. `project_crew.py` orquesta:
- Secuencia de ejecución de tareas
- Delegación entre agentes
- Flujo de información entre tareas

### `/docs`
Toda la documentación del proyecto:
- **MODEL_STRATEGY.md**: Cómo elegir el mejor modelo para cada agente
- **QUICKSTART.md**: Instalación y configuración paso a paso
- **SETUP_GITHUB_MODELS.md**: Configurar GitHub Models (gratis con Copilot)

### `/examples`
Proyectos de ejemplo generados con el sistema:
- E-commerce
- Dashboards
- Landing pages
- Sistemas de gestión

### `/output`
Carpeta donde se guardan los proyectos generados. **No se versiona en Git**.

Estructura típica de un proyecto generado:
```
output/mi-proyecto/
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── docs/
    └── architecture.md
```

### `/tools`
Herramientas que los agentes pueden usar:
- **code_generator**: Generación de código con templates
- **deployment_tools**: Docker, CI/CD, cloud deployment
- **file_operations**: Crear/editar archivos del proyecto
- **testing_tools**: Ejecución de tests, linting
- **web_research**: Búsqueda de documentación y mejores prácticas

### `/utils`
Utilidades compartidas:
- **llm_config.py**: Configuración centralizada de modelos LLM
  - Soporte para GitHub Models, OpenAI, Anthropic
  - Función `get_best_model_for_agent()` para optimización automática
  - Manejo de variables de entorno

## 🔧 Archivos de Configuración

### `.env` (no versionado)
Contiene tus credenciales reales:
```env
LLM_PROVIDER=github
GITHUB_TOKEN=ghp_tu_token_aqui
GITHUB_MODEL=gpt-5.1-codex
```

### `.env.example` (versionado)
Plantilla con todos los proveedores disponibles y ejemplos.

### `.vscode/settings.json`
Configuración de VS Code:
- Intérprete de Python del venv
- Formateo automático con Black
- Linting con flake8
- Type checking con Pylance

### `requirements.txt`
Todas las dependencias Python:
- `crewai==1.4.1` - Framework multi-agente
- `langchain-openai==1.0.2` - Cliente LLM
- `python-dotenv` - Variables de entorno
- Y más...

## 🚀 Flujo de Trabajo

1. **Usuario ejecuta:** `python main.py create --project ecommerce --name "Mi Tienda"`

2. **main.py** lee las variables de entorno y crea el ProjectCrew

3. **ProjectCrew** inicializa los 6 agentes con sus modelos óptimos

4. **Ejecución secuencial de tareas:**
   - BA analiza requisitos → genera user stories
   - PM crea plan de proyecto → define arquitectura
   - Backend Dev diseña API → implementa código
   - Frontend Dev diseña UI → implementa componentes
   - DevOps configura deployment → crea Dockerfiles
   - QA crea plan de testing → ejecuta tests

5. **Resultado:** Proyecto completo en `output/mi-tienda/`

## 📝 Convenciones de Código

- **Nombres de archivos**: `snake_case.py`
- **Nombres de clases**: `PascalCase`
- **Nombres de funciones**: `snake_case()`
- **Constantes**: `UPPER_CASE`
- **Formateo**: Black (line length 120)
- **Linting**: flake8
- **Type hints**: Obligatorios en funciones públicas
- **Docstrings**: Google style

## 🔄 Actualización de la Estructura

Si necesitas agregar:
- **Nuevo agente**: Crear en `/agents` y registrar en `project_crew.py`
- **Nueva herramienta**: Crear en `/tools` y asignar a agentes
- **Nueva documentación**: Agregar en `/docs`
- **Nuevo ejemplo**: Crear carpeta en `/examples`

## 📚 Más Información

- [README principal](../README.md)
- [Guía de inicio rápido](QUICKSTART.md)
- [Estrategia de modelos](MODEL_STRATEGY.md)
