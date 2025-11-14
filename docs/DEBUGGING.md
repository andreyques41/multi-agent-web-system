# 🐛 Guía de Debugging

Esta guía te muestra cómo hacer debugging del sistema multi-agente.

## 🧪 Comandos de Debugging

### 1. **Probar Conexión con el LLM**

Antes de crear un proyecto, prueba que tu configuración funciona:

```bash
# Probar con el modelo por defecto
python main.py test-llm

# Probar con un modelo específico
python main.py test-llm --model claude-4.5-sonnet
python main.py test-llm --model gpt-5.1-codex

# Probar con un prompt personalizado
python main.py test-llm --prompt "Dame un ejemplo de código Python"
```

**Qué hace:**
- Conecta con el LLM configurado
- Envía un prompt simple
- Muestra la respuesta
- Si falla, te da pistas de qué está mal

**Ejemplo de salida exitosa:**
```
✅ LLM funcionando correctamente!

╭─ Respuesta del LLM ─╮
│ ¡Hola! Sí, funciono │
│ correctamente.      │
╰─────────────────────╯
```

---

### 2. **Verificar Configuración**

```bash
python main.py check-config
```

**Qué muestra:**
- Provider actual (GitHub/OpenAI/Anthropic)
- Modelo por defecto
- Modelos asignados a cada agente
- Todos los modelos disponibles
- Si hay algún error de configuración

---

### 3. **Modo Verbose**

Ver logs detallados durante la creación del proyecto:

```bash
python main.py create --project landing --name "Test" --verbose
```

**Qué muestra:**
- Qué agente está trabajando
- Qué tarea está ejecutando
- Progreso de cada paso
- Logs de CrewAI

---

### 4. **Modo Debug**

Ver TODO incluyendo llamadas al LLM:

```bash
python main.py create --project landing --name "Test" --debug
```

**Qué muestra:**
- Todo lo del modo verbose
- Prompts enviados al LLM
- Respuestas del LLM
- Errores detallados
- Stack traces completos

---

### 5. **Guardar Logs en Archivo**

```bash
# Crear directorio de logs
mkdir logs

# Ejecutar con logs
python main.py create --project landing --name "Test" --debug --log-file logs/proyecto.log
```

**Ventajas:**
- Puedes revisar los logs después
- Útil para reportar errores
- No pierdas información si falla

---

## 🔍 Estrategia de Debugging

### Paso 1: Verificar Configuración Básica

```bash
python main.py check-config
```

**Verifica:**
- ✅ Aparece tu provider (GITHUB)
- ✅ Aparecen los modelos
- ✅ No hay errores rojos

---

### Paso 2: Probar Conexión con LLM

```bash
# Probar GPT
python main.py test-llm --model gpt-5.1

# Probar Claude
python main.py test-llm --model claude-4.5-sonnet
```

**Si falla:**
- ❌ `authentication error` → Token inválido o sin permisos
- ❌ `model not found` → El modelo no existe en GitHub Models
- ❌ `rate limit` → Demasiadas peticiones

---

### Paso 3: Crear Proyecto con Logs

```bash
python main.py create --project landing --name "Test Debug" --verbose --log-file logs/test.log
```

**Observa:**
- ¿En qué agente falla?
- ¿Qué error muestra?
- Revisa `logs/test.log` para detalles

---

## 🚨 Errores Comunes y Soluciones

### Error: `AnthropicException - invalid x-api-key`

**Causa:** El sistema está intentando usar Anthropic directamente en lugar de GitHub Models.

**Solución:**
```bash
# Verifica que estés usando GitHub
echo $env:LLM_PROVIDER  # Windows
# Debe decir "github"

# Si no, edita .env
LLM_PROVIDER=github
```

---

### Error: `GITHUB_TOKEN not found`

**Causa:** No configuraste el token de GitHub.

**Solución:**
```bash
# Genera token en https://github.com/settings/tokens
# Edita .env y agrega:
GITHUB_TOKEN=ghp_tu_token_aqui
```

---

### Error: `Model not found`

**Causa:** El modelo que especificaste no existe.

**Solución:**
```bash
# Ver modelos disponibles
python main.py check-config

# Usa uno de los listados, ej:
python main.py test-llm --model gpt-5.1
```

---

### Error: `Rate limit exceeded`

**Causa:** Demasiadas peticiones al LLM.

**Solución:**
- Espera 1 minuto
- GitHub Models tiene límites por minuto
- Considera usar modelos más pequeños (gpt-4o en lugar de gpt-5.1)

---

## 📊 Interpretando los Logs

### Modo Verbose

```
2025-11-14 10:30:15 - crew - INFO - Starting Task: business_analyst_task
2025-11-14 10:30:20 - agent - INFO - Business Analyst is analyzing requirements
2025-11-14 10:30:45 - crew - INFO - Task completed successfully
```

**Indica:**
- Qué tarea está ejecutándose
- Qué agente está trabajando
- Si completó exitosamente

---

### Modo Debug

```
2025-11-14 10:30:15 - llm - DEBUG - Sending prompt to claude-4.5-sonnet
2025-11-14 10:30:16 - llm - DEBUG - Prompt: Analyze these requirements...
2025-11-14 10:30:45 - llm - DEBUG - Response received: Based on the requirements...
```

**Indica:**
- Qué se está enviando al LLM
- Qué responde el LLM
- Útil para ver si el prompt es correcto

---

## 🎯 Casos de Uso

### Caso 1: Claude no funciona

```bash
# 1. Prueba si Claude funciona
python main.py test-llm --model claude-4.5-sonnet

# 2. Si falla, usa GPT temporalmente
# Edita .env:
BUSINESS_ANALYST_MODEL=gpt-5.1
PROJECT_MANAGER_MODEL=gpt-5.1

# 3. Vuelve a probar
python main.py create --project landing --name "Test" --verbose
```

---

### Caso 2: Proyecto falla a mitad

```bash
# 1. Ejecuta con logs
python main.py create --project landing --name "Test" --debug --log-file logs/debug.log

# 2. Cuando falle, revisa el log
notepad logs/debug.log

# 3. Busca la última línea antes del error
# Identifica qué agente falló
# Reporta el error con el log
```

---

### Caso 3: Quiero ver qué está pensando el LLM

```bash
# Ejecuta en modo debug
python main.py create --project landing --name "Test" --debug

# Verás:
# - El prompt completo que se envía
# - La respuesta completa del LLM
# - Útil para entender decisiones del agente
```

---

## 📝 Reportar Errores

Si encuentras un error, incluye:

1. **Comando ejecutado:**
   ```bash
   python main.py create --project landing --name "Test"
   ```

2. **Configuración:**
   ```bash
   python main.py check-config
   ```
   (Copia la salida)

3. **Error exacto:**
   ```
   Error durante la creación del proyecto:
   litellm.AuthenticationError: ...
   ```

4. **Logs (si los tienes):**
   ```bash
   # Adjunta el archivo logs/debug.log
   ```

5. **Entorno:**
   - OS: Windows/Mac/Linux
   - Python: 3.13.7
   - CrewAI: 1.4.1

---

## 🔗 Recursos Adicionales

- [Configuración de GitHub Models](SETUP_GITHUB_MODELS.md)
- [Estrategia de Modelos](MODEL_STRATEGY.md)
- [Estructura del Proyecto](STRUCTURE.md)
