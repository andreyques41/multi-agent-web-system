# GitHub Models vs GitHub Copilot

## 🔴 IMPORTANTE: Son servicios DIFERENTES

### GitHub Copilot (lo que usas en VS Code)
- **Qué es**: Asistente de IA integrado en tu IDE
- **Dónde**: VS Code, Visual Studio, JetBrains, etc.
- **Modelos disponibles**: GPT-4, Claude 3.5 Sonnet, y otros
- **Cómo funciona**: Autocompletado de código, chat, agente de codificación
- **Acceso**: A través de tu suscripción de GitHub Copilot
- **URL**: No usa API directa, integración nativa en el IDE

### GitHub Models (API que usa este proyecto)
- **Qué es**: Servicio de API para experimentar con modelos
- **Dónde**: API REST en `https://models.inference.ai.azure.com`
- **Modelos disponibles**: 
  - ✅ OpenAI (GPT-4o, GPT-5, GPT-4.1, o1, o3, o4-mini, etc.)
  - ✅ Microsoft Phi-4
  - ✅ Meta Llama 3.3, 3.2, 4
  - ✅ DeepSeek R1, V3
  - ✅ Mistral, Grok, Cohere, AI21 Jamba
  - ❌ **Claude/Anthropic NO está disponible**
- **Cómo funciona**: Llamadas API directas usando token de GitHub
- **Acceso**: Token de GitHub con permiso 'models'
- **Catálogo**: https://models.github.ai/catalog/models
- **Inferencia**: https://models.inference.ai.azure.com

## ❓ ¿Por qué Claude funciona en Copilot pero NO en GitHub Models?

**GitHub Copilot** tiene acuerdos especiales con Anthropic para ofrecer Claude a sus usuarios pagos. Esto es parte del producto Copilot.

**GitHub Models** es un servicio separado (playground + API) que solo ofrece modelos de OpenAI, Microsoft, Meta, DeepSeek y otros - pero NO incluye Claude.

Ver catálogo oficial: https://github.com/marketplace/models/catalog

## 📝 Nota sobre nomenclatura de modelos

**IMPORTANTE**: Hay una diferencia entre cómo se muestran los modelos y cómo se usan:

### Catálogo API (https://models.github.ai/catalog/models):
- Muestra modelos con prefijo de proveedor: `"openai/gpt-4o"`, `"microsoft/phi-4"`, etc.

### Inferencia API (https://models.inference.ai.azure.com):
- Usa solo el nombre del modelo: `"gpt-4o"`, `"Phi-4"`, etc.
- **NO incluir el prefijo del proveedor**

Ejemplo:
```python
# ❌ INCORRECTO (falla con error 400)
model = "openai/gpt-4o"

# ✅ CORRECTO (funciona)
model = "gpt-4o"
```

## ✅ Solución para este proyecto

Como este proyecto usa la **GitHub Models Inference API**, solo podemos usar modelos disponibles en ese servicio:

### Modelos recomendados por agente:

| Agente | Modelo | Razón |
|--------|--------|-------|
| Business Analyst | `gpt-4o` | Mejor modelo probado y estable |
| Project Manager | `gpt-4o` | Planificación y documentación |
| Backend Developer | `gpt-4o` | Excelente para código |
| Frontend Developer | `gpt-4o` | UI/UX y código |
| DevOps Engineer | `gpt-4o` | Infrastructure as Code |
| QA Engineer | `gpt-4o` | Tests y validación |

**Nota**: GPT-4o está verificado y funciona perfectamente. Los modelos más nuevos (GPT-5, GPT-4.1, o3) podrían funcionar pero no están testeados en este proyecto todavía.

### Modelos disponibles en GitHub Models:

```python
MODELOS_VERIFICADOS = {
    "gpt-4o": "✅ PROBADO - Funciona perfectamente",
    "gpt-4o-mini": "✅ Disponible - Versión más pequeña",
}

MODELOS_DISPONIBLES_NO_PROBADOS = {
    # OpenAI GPT-5 Series
    "gpt-5": "Última generación - NO probado",
    "gpt-5-chat": "Optimizado para chat - NO probado",
    "gpt-5-mini": "Versión pequeña - NO probado",
    "gpt-5-nano": "Versión ultra pequeña - NO probado",
    
    # OpenAI GPT-4.1 Series
    "gpt-4.1": "Nueva versión mejorada - NO probado",
    "gpt-4.1-mini": "Versión pequeña - NO probado",
    "gpt-4.1-nano": "Versión ultra pequeña - NO probado",
    
    # OpenAI o Series (Reasoning)
    "o1": "Razonamiento avanzado - NO probado",
    "o1-mini": "Versión pequeña - NO probado",
    "o3": "Última generación - NO probado",
    "o4-mini": "Versión pequeña - NO probado",
    
    # Microsoft Phi
    "Phi-4": "Modelo pequeño de Microsoft - NO probado",
    "Phi-4-reasoning": "Con razonamiento - NO probado",
}
```

### Alternativas si necesitas Claude:

1. **Usar Anthropic directamente**:
   - Crea una API key en https://console.anthropic.com
   - Configura `ANTHROPIC_API_KEY` en tu `.env`
   - Cambia `LLM_PROVIDER=anthropic`
   - ⚠️ Esto tiene costo ($)

2. **Usar OpenAI directamente**:
   - Crea una API key en https://platform.openai.com
   - Configura `OPENAI_API_KEY` en tu `.env`
   - Cambia `LLM_PROVIDER=openai`
   - ⚠️ Esto tiene costo ($)

3. **Mantener GitHub Models** (RECOMENDADO):
   - Gratis con tu suscripción de Copilot
   - Usa GPT-4o (verificado y funcionando)
   - Ya está configurado correctamente

## 🧪 Probar los modelos

```bash
# Ver qué modelos están disponibles
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py check-config

# Probar un modelo específico (VERIFICADO ✅)
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py test-llm --model gpt-4o

# Probar otros modelos disponibles (no verificados)
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py test-llm --model gpt-5
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py test-llm --model gpt-4.1
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py test-llm --model o3

# Intentar Claude (fallará - NO disponible en GitHub Models)
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py test-llm --model claude-4.5-sonnet
# ❌ Error: unknown_model (porque no está en GitHub Models API)
```

## 📚 Referencias

- GitHub Models Catalog: https://github.com/marketplace/models/catalog
- GitHub Models API Catalog: https://models.github.ai/catalog/models
- GitHub Models Inference Endpoint: https://models.inference.ai.azure.com
- GitHub Models Docs: https://docs.github.com/en/github-models
- GitHub Models API: https://docs.github.com/en/rest/models
- GitHub Copilot: https://docs.github.com/en/copilot

## 💡 Conclusión

Cuando dices "uso Claude con GitHub Copilot", es **correcto** - Copilot Chat en VS Code te da acceso a Claude.

Pero este proyecto usa la **GitHub Models API** (no Copilot), y esa API no incluye Claude.

La solución es usar GPT-4o, que es un excelente modelo, está disponible gratis en GitHub Models, y está **verificado funcionando** en este proyecto.

## 🎯 Estado actual del proyecto

✅ **CONFIGURACIÓN COMPLETADA Y VERIFICADA**

- Provider: GitHub Models
- Modelo principal: GPT-4o
- Token: Configurado y funcionando
- Test: ✅ `python main.py test-llm --model gpt-4o` exitoso
- Listo para crear el primer proyecto

```bash
# Crear tu primer proyecto de prueba
c:\Users\ANDY\repos\multi-agent-web-dev\venv\Scripts\python.exe main.py create \
  --project landing \
  --name "Mi Landing Page" \
  --description "Landing page de prueba para una PyME" \
  --verbose
```

