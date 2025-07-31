"""
Code Analysis Tool for Development Team
"""

import ast
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from crewai.tools import BaseTool


class CodeAnalysisTool(BaseTool):
    name: str = "Code Analysis Tool"
    description: str = "Tool for analyzing code quality, complexity, and structure"

    def _run(self, operation: str, file_path: str, language: str = "python") -> str:
        """
        Analyze code files
        
        Args:
            operation: Analysis type (complexity, structure, quality, lint)
            file_path: Path to the code file
            language: Programming language (python, javascript, etc.)
        """
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                return f"File not found: {file_path}"
            
            if operation == "structure" and language == "python":
                return self._analyze_python_structure(path_obj)
            
            elif operation == "complexity" and language == "python":
                return self._analyze_python_complexity(path_obj)
            
            elif operation == "lint" and language == "python":
                return self._lint_python_code(path_obj)
            
            elif operation == "quality":
                return self._analyze_code_quality(path_obj, language)
            
            else:
                return f"Analysis operation '{operation}' not supported for {language}"
                
        except Exception as e:
            return f"Error analyzing code: {str(e)}"
    
    def _analyze_python_structure(self, file_path: Path) -> str:
        """Analyze Python file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    else:
                        imports.append(node.module or "")
            
            result = f"Python Structure Analysis for {file_path.name}:\n"
            result += f"Classes ({len(classes)}): {', '.join(classes)}\n"
            result += f"Functions ({len(functions)}): {', '.join(functions)}\n"
            result += f"Imports ({len(imports)}): {', '.join(imports)}"
            
            return result
            
        except Exception as e:
            return f"Error analyzing Python structure: {str(e)}"
    
    def _analyze_python_complexity(self, file_path: Path) -> str:
        """Analyze Python code complexity"""
        try:
            result = subprocess.run(
                ["python", "-m", "mccabe", "--min", "5", str(file_path)],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    return f"Complexity Analysis:\n{result.stdout}"
                else:
                    return "No complex functions found (complexity < 5)"
            else:
                return "McCabe complexity analysis not available (install mccabe: pip install mccabe)"
                
        except Exception as e:
            return f"Error analyzing complexity: {str(e)}"
    
    def _lint_python_code(self, file_path: Path) -> str:
        """Lint Python code"""
        try:
            result = subprocess.run(
                ["python", "-m", "flake8", str(file_path)],
                capture_output=True, text=True
            )
            
            if result.stdout.strip():
                return f"Linting Issues:\n{result.stdout}"
            else:
                return "No linting issues found"
                
        except Exception as e:
            return f"Error linting code: {str(e)}"
    
    def _analyze_code_quality(self, file_path: Path, language: str) -> str:
        """General code quality analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if not line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            
            result = f"Code Quality Analysis for {file_path.name}:\n"
            result += f"Total lines: {total_lines}\n"
            result += f"Blank lines: {blank_lines}\n"
            result += f"Comment lines: {comment_lines}\n"
            result += f"Code lines: {total_lines - blank_lines - comment_lines}\n"
            result += f"Comment ratio: {comment_lines / total_lines * 100:.1f}%"
            
            return result
            
        except Exception as e:
            return f"Error analyzing code quality: {str(e)}"
