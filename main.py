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

# Configure CrewAI to use GitHub Models API
# CrewAI internally uses OpenAI client, so we configure it to point to GitHub's endpoint
github_token = os.getenv("GITHUB_TOKEN")
if github_token:
    # Use GitHub token as the API key
    os.environ["OPENAI_API_KEY"] = github_token
    # Point to GitHub Models endpoint (OpenAI-compatible)
    os.environ["OPENAI_API_BASE"] = "https://models.inference.ai.azure.com"

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
    # Check if ANY provider is configured
    github_token = os.getenv('GITHUB_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not any([github_token, openai_key, anthropic_key]):
        console.print("\n[bold red]⚠️  Configuración Incompleta[/bold red]\n")
        console.print("No se encontró ningún proveedor de IA configurado.")
        console.print("\n[bold]Configura UNO de los siguientes:[/bold]")
        console.print("  • GITHUB_TOKEN (Recomendado - GRATIS con GitHub Copilot)")
        console.print("  • OPENAI_API_KEY (Pay-per-use)")
        console.print("  • ANTHROPIC_API_KEY (Pay-per-use - Más económico)")
        console.print("\nPor favor, edita tu archivo .env basándote en .env.example")
        console.print("Más información: python main.py check-config\n")
        return False
    return True


def create_project(args):
    """Create a new web project using the multi-agent system."""
    console.print(f"\n[bold green]📦 Creando Proyecto: {args.name}[/bold green]")
    console.print(f"Tipo: {args.project}")
    console.print(f"Output: {args.output}")
    
    # Setup logging if requested
    if args.debug or args.verbose:
        import logging
        log_level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(args.log_file) if args.log_file else logging.NullHandler()
            ]
        )
        console.print(f"[yellow]🔍 Modo {'DEBUG' if args.debug else 'VERBOSE'} activado[/yellow]")
        if args.log_file:
            console.print(f"[yellow]📝 Logs guardándose en: {args.log_file}[/yellow]")
    
    console.print()
    
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
        import traceback
        traceback.print_exc()
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


def test_llm(args):
    """Test LLM connection with a simple prompt."""
    from utils.llm_config import get_llm_config
    from langchain_openai import ChatOpenAI
    
    print_banner()
    console.print("\n[bold cyan]🧪 Probando Conexión con LLM[/bold cyan]\n")
    
    try:
        provider = os.getenv("LLM_PROVIDER", "github")
        model = args.model if args.model else os.getenv("GITHUB_MODEL", "gpt-5.1")
        
        console.print(f"[cyan]Provider:[/cyan] {provider}")
        console.print(f"[cyan]Modelo:[/cyan] {model}")
        console.print(f"[cyan]Prompt:[/cyan] {args.prompt}\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Llamando al LLM...", total=None)
            
            # Get LLM config
            llm_config = get_llm_config(provider=provider, model=model)
            llm = ChatOpenAI(**llm_config)
            
            # Make a simple call
            from langchain_core.messages import HumanMessage
            response = llm.invoke([HumanMessage(content=args.prompt)])
            
            progress.update(task, description="✅ Respuesta recibida!")
        
        console.print("\n[bold green]✅ LLM funcionando correctamente![/bold green]\n")
        console.print(Panel(response.content, title="Respuesta del LLM", style="green"))
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error al conectar con LLM:[/bold red]")
        console.print(f"{str(e)}\n")
        
        # Show detailed error if it's an authentication issue
        if "authentication" in str(e).lower() or "api" in str(e).lower():
            console.print("[yellow]💡 Posibles soluciones:[/yellow]")
            console.print("  1. Verifica que tu GITHUB_TOKEN sea válido")
            console.print("  2. Verifica que el token tenga el scope 'models' o permisos de Copilot")
            console.print("  3. Intenta regenerar el token en https://github.com/settings/tokens")
            console.print()
        
        sys.exit(1)


def check_llm_config():
    """Check and display LLM provider configuration."""
    from utils.llm_config import get_provider_info, list_available_models, get_best_model_for_agent
    
    print_banner()
    console.print("\n[bold cyan]🔍 Verificando Configuración de IA[/bold cyan]\n")
    
    try:
        # Get provider info
        info = get_provider_info()
        console.print(Panel(info, title="Configuración Actual", style="green"))
        
        # Show agent-specific models
        console.print("\n[bold]Modelos por agente (optimizados automáticamente):[/bold]\n")
        agents = {
            "Business Analyst": "business_analyst",
            "Project Manager": "project_manager",
            "Backend Developer": "backend",
            "Frontend Developer": "frontend",
            "DevOps Engineer": "devops",
            "QA Engineer": "qa",
        }
        
        for agent_name, agent_role in agents.items():
            model = get_best_model_for_agent(agent_role)
            if model:
                console.print(f"  • [cyan]{agent_name:20}[/cyan] → {model}")
            else:
                console.print(f"  • [cyan]{agent_name:20}[/cyan] → (usando modelo por defecto)")
        
        # List available models
        models = list_available_models()
        console.print("\n[bold]Modelos disponibles por proveedor:[/bold]")
        for provider, model_list in models.items():
            console.print(f"\n[cyan]{provider.upper()}:[/cyan]")
            for model in model_list:
                console.print(f"  • {model}")
        
        console.print("\n[bold green]✅ Configuración válida[/bold green]\n")
        console.print("[dim]💡 Tip: Edita .env para override de modelo por agente (ver docs/MODEL_STRATEGY.md)[/dim]\n")
        
    except ValueError as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")
        console.print("[bold]Configura tu archivo .env con UNO de los siguientes:[/bold]")
        console.print("  • GITHUB_TOKEN=tu_token (Recomendado - GRATIS)")
        console.print("  • OPENAI_API_KEY=tu_key")
        console.print("  • ANTHROPIC_API_KEY=tu_key\n")
        sys.exit(1)


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
  python main.py check-config
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
    create_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar logs detallados de los agentes'
    )
    create_parser.add_argument(
        '--debug',
        action='store_true',
        help='Modo debug completo (incluye llamadas a LLM)'
    )
    create_parser.add_argument(
        '--log-file',
        type=str,
        help='Guardar logs en archivo (ej: logs/proyecto.log)'
    )
    
    # List templates command
    list_parser = subparsers.add_parser('list-templates', help='Listar templates disponibles')
    
    # Check config command
    check_parser = subparsers.add_parser('check-config', help='Verificar configuración del proveedor de IA')
    
    # Test LLM command (debugging)
    test_parser = subparsers.add_parser('test-llm', help='Probar conexión con el LLM')
    test_parser.add_argument(
        '--model',
        type=str,
        help='Modelo específico a probar (ej: claude-4.5-sonnet, gpt-5.1-codex)'
    )
    test_parser.add_argument(
        '--prompt',
        type=str,
        default='Hola, ¿funcionas correctamente?',
        help='Prompt de prueba'
    )
    
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
    elif args.command == 'check-config':
        check_llm_config()
    elif args.command == 'test-llm':
        test_llm(args)


if __name__ == '__main__':
    main()
