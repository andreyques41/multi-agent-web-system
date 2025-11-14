# Guía de Inicio Rápido

## 🚀 Configuración Inicial

### 1. Clonar el Repositorio

```bash
git clone https://github.com/andreyques41/multi-agent-web-dev.git
cd multi-agent-web-dev
```

### 2. Crear Ambiente Virtual

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Edita el archivo `.env` y agrega tu API key de OpenAI:

```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**¿Cómo obtener tu API Key?**
1. Ve a [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Inicia sesión o crea una cuenta
3. Haz clic en "Create new secret key"
4. Copia la key y pégala en tu archivo `.env`

## 💻 Uso Básico

### Listar Templates Disponibles

```bash
python main.py list-templates
```

### Crear un Proyecto

**E-commerce:**
```bash
python main.py create --project ecommerce --name "Mi Tienda Online" --description "Tienda de ropa y accesorios"
```

**Landing Page:**
```bash
python main.py create --project landing --name "Consultora ABC" --description "Página de servicios de consultoría"
```

**Dashboard:**
```bash
python main.py create --project dashboard --name "Panel Admin" --description "Sistema de gestión de inventario"
```

**API Backend:**
```bash
python main.py create --project api --name "API Productos" --description "API REST para gestión de productos"
```

### Opciones Adicionales

```bash
# Especificar directorio de salida personalizado
python main.py create --project ecommerce --name "Tienda" --output ./mis-proyectos

# Ver ayuda
python main.py --help
python main.py create --help
```

## 📂 Estructura del Proyecto Generado

Después de ejecutar el comando, encontrarás tu proyecto en:

```
output/
└── nombre-del-proyecto/
    ├── backend/           # Código del backend (si aplica)
    │   ├── app/
    │   ├── tests/
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── frontend/          # Código del frontend (si aplica)
    │   ├── src/
    │   ├── public/
    │   ├── package.json
    │   └── Dockerfile
    ├── docker-compose.yml # Configuración Docker
    ├── .github/           # CI/CD workflows
    └── README.md          # Documentación del proyecto
```

## 🔧 Ejecutar el Proyecto Generado

### Opción 1: Con Docker (Recomendado)

```bash
cd output/nombre-del-proyecto
docker-compose up -d
```

Accede a:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Opción 2: Manualmente

**Backend:**
```bash
cd output/nombre-del-proyecto/backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python run.py
```

**Frontend:**
```bash
cd output/nombre-del-proyecto/frontend
npm install
npm run dev
```

## 🐛 Solución de Problemas

### Error: "OPENAI_API_KEY no configurada"

Asegúrate de haber creado el archivo `.env` y agregado tu API key:
```bash
OPENAI_API_KEY=sk-tu-key-aqui
```

### Error: "ModuleNotFoundError: No module named 'crewai'"

Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Cannot find module 'react'"

Para proyectos frontend, necesitas Node.js instalado:
```bash
# Verifica que Node.js esté instalado
node --version
npm --version
```

Descarga Node.js de: https://nodejs.org/

## 📖 Próximos Pasos

1. **Revisa la documentación** del proyecto generado
2. **Personaliza el código** según tus necesidades
3. **Ejecuta los tests** con `pytest` (backend) o `npm test` (frontend)
4. **Despliega** usando Docker Compose o siguiendo la guía de deployment

## 🤝 Obtener Ayuda

- **Documentación**: Ver carpeta `docs/`
- **Ejemplos**: Ver carpeta `examples/`
- **Issues**: [GitHub Issues](https://github.com/andreyques41/multi-agent-web-dev/issues)

¡Estás listo para crear proyectos web con agentes de IA! 🚀
