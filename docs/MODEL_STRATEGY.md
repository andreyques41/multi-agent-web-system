# 🎯 Estrategia de Modelos por Agente

## 📋 Resumen

El sistema multi-agente usa **diferentes modelos de IA especializados** para cada tipo de agente, maximizando la calidad del output según la tarea:

| Agente | Modelo Recomendado | Razón |
|--------|-------------------|-------|
| **Backend Developer** | `gpt-5.1-codex` | Optimizado para generación de código Python/APIs |
| **Frontend Developer** | `gpt-5.1-codex` | Excelente para React/Vue/HTML/CSS/JavaScript |
| **DevOps Engineer** | `gpt-5.1-codex` | Perfecto para Docker/CI-CD/Infrastructure as Code |
| **Business Analyst** | `claude-4.5-sonnet` | Superior en razonamiento complejo y análisis |
| **Project Manager** | `claude-4.5-sonnet` | Mejor para planificación y documentación |
| **QA Engineer** | `gpt-5.1` | Equilibrado para generación de tests |

---

## 🤖 Por Qué Esta Estrategia

### **GPT-5.1 Codex** - Para Generación de Código

**Usado por:** Backend, Frontend, DevOps

**Fortalezas:**
- ✅ Entrenado específicamente en repositorios de código
- ✅ Entiende contexto de múltiples archivos
- ✅ Genera código idiomático y siguiendo best practices
- ✅ Excelente con frameworks modernos (Flask, FastAPI, React, Vue)
- ✅ Maneja configuraciones complejas (Docker, YAML, JSON)

**Por qué NO Claude:**
- Claude es mejor para razonamiento, pero Codex genera código más limpio y estructurado
- Codex tiene mejor comprensión de patrones de diseño en código

### **Claude 4.5 Sonnet** - Para Razonamiento Complejo

**Usado por:** Business Analyst, Project Manager

**Fortalezas:**
- ✅ Superior en análisis de requisitos complejos
- ✅ Mejor comprensión de necesidades de negocio
- ✅ Excelente para crear documentación detallada
- ✅ Razonamiento más profundo sobre trade-offs
- ✅ Mejor en planificación de largo plazo

**Por qué NO GPT-5:**
- GPT-5 tiende a ser más técnico, Claude entiende mejor el contexto de negocio
- Claude es más detallado en explicaciones y documentación

### **GPT-5.1** - Para Testing y Validación

**Usado por:** QA Engineer

**Fortalezas:**
- ✅ Balance entre generación de código de tests y razonamiento
- ✅ Bueno identificando edge cases
- ✅ Genera tests comprehensivos (unit, integration, e2e)
- ✅ Entiende tanto el código como los requisitos

---

## 🔧 Cómo Funciona

### **Configuración Automática**

Por defecto, **cada agente usa su modelo recomendado automáticamente**:

```python
# En crews/project_crew.py
self.backend_agent = create_backend_developer_agent()  # Usa gpt-5.1-codex
self.ba_agent = create_business_analyst_agent()       # Usa claude-4.5-sonnet
```

El sistema:
1. Detecta qué tipo de agente es (backend, frontend, etc.)
2. Consulta `get_best_model_for_agent(agent_role)`
3. Crea un LLM con ese modelo específico
4. Cada agente trabaja con su modelo óptimo

### **Override Manual (Opcional)**

Puedes forzar un modelo específico para un agente en `.env`:

```bash
# Forzar que el Backend use Claude en lugar de Codex
BACKEND_MODEL=claude-4.5-sonnet

# Forzar que el BA use GPT-5.1 en lugar de Claude
BUSINESS_ANALYST_MODEL=gpt-5.1
```

Variables disponibles:
- `BUSINESS_ANALYST_MODEL`
- `PROJECT_MANAGER_MODEL`
- `BACKEND_MODEL`
- `FRONTEND_MODEL`
- `DEVOPS_MODEL`
- `QA_MODEL`

---

## 📊 Comparación de Rendimiento

### **Generación de Código**

| Modelo | Backend API | Frontend UI | Docker Config | Score |
|--------|------------|-------------|---------------|-------|
| GPT-5.1 Codex | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 10/10 |
| GPT-5.1 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8/10 |
| Claude 4.5 Sonnet | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8/10 |

### **Análisis y Planificación**

| Modelo | Requisitos | User Stories | Docs | Score |
|--------|-----------|--------------|------|-------|
| Claude 4.5 Sonnet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 10/10 |
| GPT-5.1 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8/10 |
| GPT-5.1 Codex | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 6/10 |

### **Testing**

| Modelo | Unit Tests | Integration Tests | Test Coverage | Score |
|--------|-----------|------------------|---------------|-------|
| GPT-5.1 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 10/10 |
| GPT-5.1 Codex | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 9/10 |
| Claude 4.5 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 8/10 |

---

## 💡 Casos de Uso Especiales

### **Proyecto Simple (Landing Page)**

Para proyectos pequeños, puedes usar un solo modelo para todos:

```bash
# .env
LLM_PROVIDER=github
GITHUB_MODEL=gpt-5.1-codex

# No configurar overrides - todos usan gpt-5.1-codex
```

### **Proyecto Complejo (E-commerce)**

Usa la estrategia recomendada (default):
- Análisis de negocio → Claude 4.5 Sonnet
- Desarrollo → GPT-5.1 Codex
- Testing → GPT-5.1

### **Presupuesto Limitado**

Si pagas por uso (no usas GitHub Models gratis):

```bash
# Usar GPT-4o para todo (más barato que GPT-5)
GITHUB_MODEL=gpt-4o

# O usar modelos más económicos por agente
BACKEND_MODEL=gpt-4o
FRONTEND_MODEL=gpt-4o-mini  # Más rápido y barato
BUSINESS_ANALYST_MODEL=claude-3.5-sonnet  # Más barato que 4.5
```

---

## 🔍 Validar Configuración

Ver qué modelo usa cada agente:

```bash
python main.py check-config
```

Output esperado:
```
✅ Configuración válida

Provider: GITHUB
Default Model: gpt-5.1-codex
💰 Cost: FREE (using GitHub Copilot subscription)

Agent-specific models:
  • Business Analyst → claude-4.5-sonnet
  • Project Manager → claude-4.5-sonnet
  • Backend Developer → gpt-5.1-codex
  • Frontend Developer → gpt-5.1-codex
  • DevOps Engineer → gpt-5.1-codex
  • QA Engineer → gpt-5.1
```

---

## 🚀 Recomendaciones

### **Para Desarrollo de Software (Recomendado)**
```bash
# .env
LLM_PROVIDER=github
GITHUB_MODEL=gpt-5.1-codex  # Default
# Dejar que cada agente use su modelo óptimo
```

### **Para Prototipado Rápido**
```bash
# Usar GPT-5.1 Codex para todo
BUSINESS_ANALYST_MODEL=gpt-5.1-codex
PROJECT_MANAGER_MODEL=gpt-5.1-codex
# Rest usa default (gpt-5.1-codex)
```

### **Para Máxima Calidad**
```bash
# Usar modelos especializados (default)
# Business/PM → Claude 4.5 Sonnet
# Dev/DevOps → GPT-5.1 Codex
# QA → GPT-5.1
```

---

## 📚 Más Información

- [Lista de modelos disponibles](QUICKSTART.md#modelos-disponibles)
- [Configurar GitHub Models](SETUP_GITHUB_MODELS.md)
- [Variables de entorno](../.env.example)
