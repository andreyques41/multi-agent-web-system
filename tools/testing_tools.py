"""
Testing Tools

Tools for running tests, analyzing coverage, and quality assurance.
"""

from crewai_tools import tool
from typing import Optional, List
import subprocess
import os
from pathlib import Path


@tool("Run Python Tests Tool")
def run_python_tests(project_path: str, test_path: Optional[str] = None) -> str:
    """
    Run Python tests using pytest.
    
    Args:
        project_path: Path to the project root
        test_path: Optional specific test file or directory
        
    Returns:
        str: Test results
    """
    try:
        os.chdir(project_path)
        
        cmd = ['pytest', '-v']
        if test_path:
            cmd.append(test_path)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        status = "PASSED" if result.returncode == 0 else "FAILED"
        
        return f"""
Test Run Status: {status}
Exit Code: {result.returncode}

{output}
"""
    except subprocess.TimeoutExpired:
        return "Error: Test execution timed out (5 minutes)"
    except Exception as e:
        return f"Error running tests: {str(e)}"


@tool("Generate Coverage Report Tool")
def generate_coverage_report(project_path: str, html: bool = False) -> str:
    """
    Generate test coverage report using pytest-cov.
    
    Args:
        project_path: Path to the project root
        html: Whether to generate HTML report
        
    Returns:
        str: Coverage report
    """
    try:
        os.chdir(project_path)
        
        cmd = ['pytest', '--cov=app', '--cov-report=term']
        if html:
            cmd.append('--cov-report=html')
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return f"""
Coverage Report:

{result.stdout}

{result.stderr if result.stderr else ''}

{'HTML report generated in htmlcov/' if html else ''}
"""
    except Exception as e:
        return f"Error generating coverage report: {str(e)}"


@tool("Run JavaScript Tests Tool")
def run_javascript_tests(project_path: str) -> str:
    """
    Run JavaScript/React tests using npm test.
    
    Args:
        project_path: Path to the project root
        
    Returns:
        str: Test results
    """
    try:
        os.chdir(project_path)
        
        result = subprocess.run(
            ['npm', 'test', '--', '--watchAll=false'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        status = "PASSED" if result.returncode == 0 else "FAILED"
        
        return f"""
Test Run Status: {status}
Exit Code: {result.returncode}

{result.stdout}

{result.stderr if result.stderr else ''}
"""
    except Exception as e:
        return f"Error running JavaScript tests: {str(e)}"


@tool("Lint Python Code Tool")
def lint_python_code(project_path: str, files: Optional[List[str]] = None) -> str:
    """
    Lint Python code using flake8.
    
    Args:
        project_path: Path to the project root
        files: Optional list of specific files to lint
        
    Returns:
        str: Linting results
    """
    try:
        os.chdir(project_path)
        
        cmd = ['flake8']
        if files:
            cmd.extend(files)
        else:
            cmd.extend(['app/', 'tests/'])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return "✅ No linting errors found!"
        else:
            return f"""
Linting Issues Found:

{result.stdout}
"""
    except Exception as e:
        return f"Error linting code: {str(e)}"


@tool("Format Python Code Tool")
def format_python_code(project_path: str, check_only: bool = False) -> str:
    """
    Format Python code using black.
    
    Args:
        project_path: Path to the project root
        check_only: If True, only check without modifying
        
    Returns:
        str: Formatting results
    """
    try:
        os.chdir(project_path)
        
        cmd = ['black', 'app/', 'tests/']
        if check_only:
            cmd.append('--check')
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return f"""
Formatting Results:

{result.stdout}

{result.stderr if result.stderr else ''}
"""
    except Exception as e:
        return f"Error formatting code: {str(e)}"


@tool("Check Code Quality Tool")
def check_code_quality(project_path: str) -> str:
    """
    Comprehensive code quality check (tests + coverage + linting).
    
    Args:
        project_path: Path to the project root
        
    Returns:
        str: Combined quality report
    """
    report = []
    report.append("=" * 60)
    report.append("CODE QUALITY REPORT")
    report.append("=" * 60)
    
    # Run tests
    report.append("\n1. RUNNING TESTS...")
    test_result = run_python_tests(project_path)
    report.append(test_result)
    
    # Check coverage
    report.append("\n2. COVERAGE ANALYSIS...")
    coverage_result = generate_coverage_report(project_path)
    report.append(coverage_result)
    
    # Lint code
    report.append("\n3. CODE LINTING...")
    lint_result = lint_python_code(project_path)
    report.append(lint_result)
    
    # Format check
    report.append("\n4. CODE FORMATTING CHECK...")
    format_result = format_python_code(project_path, check_only=True)
    report.append(format_result)
    
    report.append("\n" + "=" * 60)
    report.append("QUALITY CHECK COMPLETE")
    report.append("=" * 60)
    
    return "\n".join(report)


class TestRunnerTool:
    """Wrapper class for test execution tools."""
    
    @staticmethod
    def run_python(project_path: str, test_path: Optional[str] = None) -> str:
        return run_python_tests(project_path, test_path)
    
    @staticmethod
    def run_javascript(project_path: str) -> str:
        return run_javascript_tests(project_path)
    
    @staticmethod
    def quality_check(project_path: str) -> str:
        return check_code_quality(project_path)


class CoverageAnalyzerTool:
    """Tool for test coverage analysis."""
    
    @staticmethod
    def generate_report(project_path: str, html: bool = False) -> str:
        return generate_coverage_report(project_path, html)
