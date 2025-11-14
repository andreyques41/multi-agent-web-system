"""
File Operations Tools

Tools for creating, reading, modifying files and project structures.
"""

from crewai_tools import tool
from typing import Dict, List, Optional
import os
from pathlib import Path
import json


@tool("Create File Tool")
def create_file(file_path: str, content: str) -> str:
    """
    Create a file with specified content.
    
    Args:
        file_path: Path where file should be created
        content: Content to write to the file
        
    Returns:
        str: Success message or error
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"Successfully created file: {file_path}"
    except Exception as e:
        return f"Error creating file {file_path}: {str(e)}"


@tool("Read File Tool")
def read_file(file_path: str) -> str:
    """
    Read contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        str: File contents or error message
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"File not found: {file_path}"
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"


@tool("Create Directory Tool")
def create_directory(dir_path: str) -> str:
    """
    Create a directory and all parent directories if needed.
    
    Args:
        dir_path: Path to the directory to create
        
    Returns:
        str: Success message or error
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return f"Successfully created directory: {dir_path}"
    except Exception as e:
        return f"Error creating directory {dir_path}: {str(e)}"


@tool("List Directory Tool")
def list_directory(dir_path: str) -> str:
    """
    List contents of a directory.
    
    Args:
        dir_path: Path to the directory
        
    Returns:
        str: List of files and directories
    """
    try:
        path = Path(dir_path)
        if not path.exists():
            return f"Directory not found: {dir_path}"
        
        items = []
        for item in sorted(path.iterdir()):
            item_type = "DIR" if item.is_dir() else "FILE"
            items.append(f"[{item_type}] {item.name}")
        
        return "\n".join(items) if items else "Directory is empty"
    except Exception as e:
        return f"Error listing directory {dir_path}: {str(e)}"


@tool("Create Project Structure Tool")
def create_project_structure(base_path: str, structure: Dict) -> str:
    """
    Create a complete project structure from a dictionary definition.
    
    Args:
        base_path: Base path where project should be created
        structure: Dictionary defining the structure
                  {
                      "dir_name": {
                          "file.py": "content",
                          "subdir": {...}
                      }
                  }
    
    Returns:
        str: Success message with created structure
    """
    try:
        base = Path(base_path)
        created_items = []
        
        def create_recursive(current_path: Path, struct: Dict):
            for name, value in struct.items():
                item_path = current_path / name
                
                if isinstance(value, dict):
                    # It's a directory
                    item_path.mkdir(parents=True, exist_ok=True)
                    created_items.append(f"[DIR]  {item_path.relative_to(base)}")
                    create_recursive(item_path, value)
                else:
                    # It's a file
                    item_path.parent.mkdir(parents=True, exist_ok=True)
                    item_path.write_text(str(value), encoding='utf-8')
                    created_items.append(f"[FILE] {item_path.relative_to(base)}")
        
        create_recursive(base, structure)
        
        return f"""
Successfully created project structure at: {base_path}

Created {len(created_items)} items:
{chr(10).join(created_items[:50])}
{'... and more' if len(created_items) > 50 else ''}
"""
    except Exception as e:
        return f"Error creating project structure: {str(e)}"


@tool("File Exists Tool")
def file_exists(file_path: str) -> str:
    """
    Check if a file or directory exists.
    
    Args:
        file_path: Path to check
        
    Returns:
        str: Exists status and type
    """
    path = Path(file_path)
    if not path.exists():
        return f"Does not exist: {file_path}"
    elif path.is_file():
        size = path.stat().st_size
        return f"File exists: {file_path} ({size} bytes)"
    elif path.is_dir():
        items = len(list(path.iterdir()))
        return f"Directory exists: {file_path} ({items} items)"
    else:
        return f"Exists but type unknown: {file_path}"


@tool("Write JSON File Tool")
def write_json_file(file_path: str, data: Dict) -> str:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path to JSON file
        data: Dictionary to write
        
    Returns:
        str: Success message or error
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return f"Successfully wrote JSON to: {file_path}"
    except Exception as e:
        return f"Error writing JSON file {file_path}: {str(e)}"


@tool("Read JSON File Tool")
def read_json_file(file_path: str) -> str:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        str: JSON content as string or error
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"File not found: {file_path}"
        data = json.loads(path.read_text(encoding='utf-8'))
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error reading JSON file {file_path}: {str(e)}"


class FileOperationsTool:
    """Wrapper class for file operation tools."""
    
    @staticmethod
    def create_file(file_path: str, content: str) -> str:
        return create_file(file_path, content)
    
    @staticmethod
    def read_file(file_path: str) -> str:
        return read_file(file_path)
    
    @staticmethod
    def create_directory(dir_path: str) -> str:
        return create_directory(dir_path)
    
    @staticmethod
    def list_directory(dir_path: str) -> str:
        return list_directory(dir_path)
    
    @staticmethod
    def file_exists(file_path: str) -> str:
        return file_exists(file_path)


class ProjectStructureTool:
    """Tool for creating complete project structures."""
    
    @staticmethod
    def create(base_path: str, structure: Dict) -> str:
        return create_project_structure(base_path, structure)
