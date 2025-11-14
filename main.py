"""
Multi-Agent Web Development System
Main Entry Point

This is the main orchestrator for the multi-agent web development system.
It coordinates different agents to work together on web development projects.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()


def print_banner():
    """Print the application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     🤖  MULTI-AGENT WEB DEVELOPMENT SYSTEM  🤖      ║
    ║                                                       ║
    ║         Desarrollo Web Automatizado para PyMEs       ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue"))


def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        console.print("\n[bold red]⚠️  Configuración Incompleta[/bold red]\n")
        console.print("Las siguientes variables de entorno no están configuradas:")
        for var in missing_vars:
            console.print(f"  • {var}")
        console.print("\nPor favor, configura tu archivo .env basándote en .env.example")
        console.print("Mínimo requerido: OPENAI_API_KEY\n")
        return False
    return True


def create_project(args):
    """Create a new web project using the multi-agent system."""
    console.print(f"\n[bold green]📦 Creando Proyecto: {args.name}[/bold green]")
    console.print(f"Tipo: {args.project}")
    console.print(f"Output: {args.output}\n")
    
    # Import here to avoid errors if dependencies aren't installed yet
    try:
        from crews.project_crew import ProjectCrew
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Inicializando agentes...", total=None)
            
            # Create the crew based on project type
            crew = ProjectCrew(
                project_name=args.name,
                project_type=args.project,
                output_dir=args.output,
                description=args.description
            )
            
            progress.update(task, description="Agentes trabajando en tu proyecto...")
            
            # Execute the crew
            result = crew.run()
            
            progress.update(task, description="✅ Proyecto completado!")
        
        console.print("\n[bold green]🎉 ¡Proyecto Creado Exitosamente![/bold green]\n")
        console.print(result)
        
    except ImportError as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        console.print("\n[yellow]Asegúrate de haber instalado las dependencias:[/yellow]")
        console.print("  pip install -r requirements.txt\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error durante la creación del proyecto:[/bold red]")
        console.print(f"{str(e)}\n")
        sys.exit(1)


def list_templates():
    """List available project templates."""
    console.print("\n[bold cyan]📋 Templates Disponibles:[/bold cyan]\n")
    
    templates = {
        "ecommerce": {
            "name": "E-commerce",
            "description": "Tienda online completa con catálogo, carrito y checkout",
            "features": ["Catálogo de productos", "Carrito de compras", "Sistema de pagos", "Panel admin"],
            "time": "2-3 semanas"
        },
        "landing": {
            "name": "Landing Page",
            "description": "Página de aterrizaje moderna y responsive",
            "features": ["Hero section", "Servicios", "Testimonios", "Formulario de contacto"],
            "time": "3-5 días"
        },
        "dashboard": {
            "name": "Dashboard",
            "description": "Panel de administración con gestión de datos",
            "features": ["Autenticación", "CRUD completo", "Gráficos", "Reportes"],
            "time": "1-2 semanas"
        },
        "api": {
            "name": "REST API",
            "description": "API backend robusta y escalable",
            "features": ["Endpoints REST", "Autenticación JWT", "Documentación", "Rate limiting"],
            "time": "1 semana"
        }
    }
    
    for key, template in templates.items():
        console.print(f"[bold]{template['name']}[/bold] ({key})")
        console.print(f"  {template['description']}")
        console.print(f"  Tiempo estimado: {template['time']}")
        console.print(f"  Features:")
        for feature in template['features']:
            console.print(f"    • {feature}")
        console.print()


def main():
    """Main entry point."""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Sistema Multi-Agente para Desarrollo Web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py create --project ecommerce --name "Tienda de Ropa"
  python main.py create --project landing --name "Consultora ABC" --description "Landing page para consultora"
  python main.py create --project dashboard --name "Panel Admin"
  python main.py list-templates
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Create project command
    create_parser = subparsers.add_parser('create', help='Crear un nuevo proyecto')
    create_parser.add_argument(
        '--project',
        type=str,
        required=True,
        choices=['ecommerce', 'landing', 'dashboard', 'api'],
        help='Tipo de proyecto a crear'
    )
    create_parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='Nombre del proyecto'
    )
    create_parser.add_argument(
        '--description',
        type=str,
        default='',
        help='Descripción detallada del proyecto'
    )
    create_parser.add_argument(
        '--output',
        type=str,
        default='./output',
        help='Directorio de salida (default: ./output)'
    )
    
    # List templates command
    list_parser = subparsers.add_parser('list-templates', help='Listar templates disponibles')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    if args.command == 'create':
        if not check_environment():
            sys.exit(1)
        create_project(args)
    elif args.command == 'list-templates':
        list_templates()


if __name__ == '__main__':
    main()
