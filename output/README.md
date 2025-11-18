# Output Directory

Este directorio contendrá los proyectos generados por el sistema multi-agente.

## Estructura Típica

Cuando ejecutes `python main.py create --project <tipo> --name "<nombre>"`, se creará una carpeta aquí con la siguiente estructura:

```
output/
└── nombre-proyecto/
    ├── backend/
    │   ├── app/
    │   ├── config/
    │   ├── tests/
    │   └── requirements.txt
    ├── frontend/
    │   ├── src/
    │   ├── public/
    │   └── package.json
    └── docs/
        ├── requirements.md
        ├── architecture.md
        └── api-docs.md
```

## Archivos Ignorados

Esta carpeta está en `.gitignore` para evitar subir proyectos generados al repositorio.
