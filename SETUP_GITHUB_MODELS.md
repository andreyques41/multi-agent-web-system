# 🚀 INSTRUCCIONES: Configurar GitHub Models (GRATIS)

## ✅ Beneficios de usar GitHub Models

Ya que tienes **GitHub Copilot Premium**, puedes usar modelos de IA premium **SIN COSTO ADICIONAL**:

### **Serie GPT-5 (Noviembre 2025 - Última Generación)**
- ✅ **GPT-5.1 Codex** ⭐ - Optimizado específicamente para desarrollo de software
- ✅ **GPT-5.1** - Versión más avanzada de OpenAI
- ✅ **GPT-5 Codex** - Especializado en generación de código
- ✅ **GPT-5** - Modelo general más potente

### **Serie Claude 4 (Noviembre 2025 - Última Generación)**
- ✅ **Claude 4.5 Sonnet** ⭐ - Modelo más avanzado de Anthropic
- ✅ **Claude 4 Sonnet** - Excelente para arquitectura de código

### **Modelos Legacy (Aún disponibles)**
- ✅ **GPT-4o**, **GPT-4o-mini**, **GPT-4** - Serie GPT-4
- ✅ **Claude 3.5 Sonnet** - Serie Claude 3
- ✅ **Llama 3.1 70B**, **Phi-3** - Open source

### **💰 Comparación de Precios:**
- **GitHub Models**: **GRATIS** (incluido en Copilot)
- OpenAI directo: ~$3-8 USD por proyecto (GPT-5 es más caro)
- Anthropic directo: ~$2-5 USD por proyecto

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

4. **OPCIONAL**: Elige el modelo que quieres usar:
   ```env
   # Modelos recomendados para desarrollo de software:
   GITHUB_MODEL=gpt-5.1-codex          # ⭐ RECOMENDADO - Optimizado para código
   # GITHUB_MODEL=claude-4.5-sonnet    # Excelente para arquitectura compleja
   # GITHUB_MODEL=gpt-5.1               # Más avanzado, uso general
   # GITHUB_MODEL=gpt-5-codex           # Especializado en código
   # GITHUB_MODEL=claude-4-sonnet       # Claude 4 base
   
   # Modelos legacy (aún disponibles):
   # GITHUB_MODEL=gpt-4o                # GPT-4 optimizado
   # GITHUB_MODEL=claude-3.5-sonnet     # Claude 3.5
   # GITHUB_MODEL=gpt-4o-mini           # Rápido y liviano
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
Model: openai/gpt-5.1-codex
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

**Para desarrollo de software (RECOMENDADO):**
- `gpt-5.1-codex` ⭐ - Mejor para generación de código completo
- `gpt-5-codex` - Especializado en código
- `claude-4.5-sonnet` - Excelente para arquitectura y diseño

**Para proyectos complejos:**
- `gpt-5.1` - Más inteligente, razonamiento avanzado
- `claude-4.5-sonnet` - Mejor comprensión de contexto

**Para iteraciones rápidas:**
- `gpt-4o-mini` - Más rápido, menos recursos
- `gpt-4o` - Balance velocidad/calidad

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
