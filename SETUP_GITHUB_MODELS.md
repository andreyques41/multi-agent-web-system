# 🚀 INSTRUCCIONES: Configurar GitHub Models (GRATIS)

## ✅ Beneficios de usar GitHub Models

Ya que tienes **GitHub Copilot Premium**, puedes usar modelos de IA premium **SIN COSTO ADICIONAL**:

- ✅ **GPT-4o** - Modelo más avanzado de OpenAI
- ✅ **Claude 3.5 Sonnet** - Excelente para código complejo  
- ✅ **GPT-4o-mini** - Rápido para tareas simples
- ✅ **Llama 3.1 70B** - Modelo open source potente
- ✅ **SIN COSTOS** - Incluido en tu suscripción de Copilot

Vs. pagar:
- OpenAI: ~$2-5 USD por proyecto
- Anthropic: ~$1-3 USD por proyecto

---

## 📋 Pasos para Configurar

### 1️⃣ Crear un Personal Access Token (PAT)

1. Ve a: **https://github.com/settings/tokens**
2. Haz clic en **"Generate new token"** → **"Generate new token (classic)"**
3. Configuración del token:
   - **Name**: `multi-agent-web-dev` (o cualquier nombre descriptivo)
   - **Expiration**: `90 days` (o el tiempo que prefieras)
   - **Scopes**: Selecciona SOLO **`models`** (GitHub Models API)
     - ⚠️ **IMPORTANTE**: Solo necesitas el scope `models`, no más
4. Haz clic en **"Generate token"** al final de la página
5. **COPIA EL TOKEN INMEDIATAMENTE** 
   - ⚠️ Solo se muestra UNA VEZ
   - Formato: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2️⃣ Configurar el archivo .env

1. Abre el archivo `.env` en este directorio con un editor de texto:
   ```powershell
   notepad .env
   ```

2. Busca la línea que dice:
   ```env
   GITHUB_TOKEN=your-github-personal-access-token-here
   ```

3. Reemplázala con tu token real:
   ```env
   GITHUB_TOKEN=ghp_tu_token_real_aqui_xxxxxxxxxx
   ```

4. **OPCIONAL**: Elige el modelo que quieres usar (por defecto es gpt-4o):
   ```env
   GITHUB_MODEL=gpt-4o          # Recomendado para desarrollo completo
   # GITHUB_MODEL=claude-3.5-sonnet  # Excelente para código complejo
   # GITHUB_MODEL=gpt-4o-mini        # Más rápido y liviano
   ```

5. **Guarda** el archivo `.env`

### 3️⃣ Verificar la Configuración

Ejecuta el comando de verificación:

```powershell
python main.py check-config
```

Deberías ver:
```
✅ Configuración válida

Provider: GITHUB
Model: openai/gpt-4o
💰 Cost: FREE (using GitHub Copilot subscription)
```

---

## 🎯 Próximos Pasos

Una vez configurado, puedes:

### 1. Crear tu primer proyecto de prueba:

```powershell
python main.py create --project landing --name "Test Landing" --description "Página de prueba para validar el sistema"
```

### 2. Ver templates disponibles:

```powershell
python main.py list-templates
```

### 3. Crear un proyecto real:

```powershell
python main.py create --project ecommerce --name "Mi Tienda" --description "Tienda online de productos artesanales con catálogo, carrito y checkout"
```

---

## 🔒 Seguridad del Token

- ⚠️ **NUNCA** compartas tu token con nadie
- ⚠️ **NUNCA** lo subas a Git (`.env` ya está en `.gitignore`)
- 🔄 Puedes revocarlo en cualquier momento en: https://github.com/settings/tokens
- 🔄 Si lo pierdes, simplemente genera uno nuevo

---

## ❓ Preguntas Frecuentes

### ¿Tengo límite de uso?

Sí, GitHub Copilot tiene límites mensuales, pero son generosos:
- Suficientes para varios proyectos al mes
- El sistema te avisará si te acercas al límite

### ¿Puedo cambiar de modelo después?

Sí, solo edita `GITHUB_MODEL` en `.env`:
- `gpt-4o` - Más inteligente, mejor para proyectos complejos
- `claude-3.5-sonnet` - Excelente para arquitectura de código
- `gpt-4o-mini` - Más rápido para cambios pequeños

### ¿Y si quiero usar OpenAI o Claude directamente?

Puedes cambiar el proveedor en `.env`:

```env
# Opción 2: OpenAI (pago)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-tu-key-aqui

# Opción 3: Anthropic (pago, más barato)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
```

Pero para empezar, **GitHub Models es la mejor opción** porque es gratis.

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas:

1. Verifica que el token tenga el scope `models`
2. Asegúrate de que no haya espacios extra en el `.env`
3. Ejecuta `python main.py check-config` para diagnosticar
4. Revisa que tu suscripción de GitHub Copilot esté activa

---

**¡Listo para crear proyectos web automáticamente con IA! 🚀**
