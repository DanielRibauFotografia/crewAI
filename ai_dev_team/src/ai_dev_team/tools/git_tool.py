"""
Git Operations Tool for Development Team
"""

import subprocess
from typing import Optional
from crewai.tools import BaseTool
from pathlib import Path


class GitTool(BaseTool):
    name: str = "Git Tool"
    description: str = "Tool for Git version control operations including init, add, commit, push, pull, status, and branch operations"

    def _run(self, operation: str, path: str = ".", message: Optional[str] = None, 
             branch: Optional[str] = None, remote_url: Optional[str] = None) -> str:
        """
        Execute Git operations
        
        Args:
            operation: Git operation (init, add, commit, push, pull, status, branch, checkout, clone)
            path: Repository path (default: current directory)
            message: Commit message
            branch: Branch name
            remote_url: Remote repository URL
        """
        try:
            original_dir = Path.cwd()
            repo_path = Path(path).resolve()
            
            if operation == "clone" and remote_url:
                result = subprocess.run(
                    ["git", "clone", remote_url, str(repo_path)],
                    capture_output=True, text=True, cwd=original_dir
                )
            else:
                if not repo_path.exists():
                    return f"Path does not exist: {path}"
                
                if operation == "init":
                    result = subprocess.run(
                        ["git", "init"], capture_output=True, text=True, cwd=repo_path
                    )
                
                elif operation == "add":
                    result = subprocess.run(
                        ["git", "add", "."], capture_output=True, text=True, cwd=repo_path
                    )
                
                elif operation == "commit":
                    if not message:
                        return "Commit message is required"
                    result = subprocess.run(
                        ["git", "commit", "-m", message], 
                        capture_output=True, text=True, cwd=repo_path
                    )
                
                elif operation == "push":
                    result = subprocess.run(
                        ["git", "push"], capture_output=True, text=True, cwd=repo_path
                    )
                
                elif operation == "pull":
                    result = subprocess.run(
                        ["git", "pull"], capture_output=True, text=True, cwd=repo_path
                    )
                
                elif operation == "status":
                    result = subprocess.run(
                        ["git", "status"], capture_output=True, text=True, cwd=repo_path
                    )
                
                elif operation == "branch":
                    if branch:
                        result = subprocess.run(
                            ["git", "branch", branch], 
                            capture_output=True, text=True, cwd=repo_path
                        )
                    else:
                        result = subprocess.run(
                            ["git", "branch"], capture_output=True, text=True, cwd=repo_path
                        )
                
                elif operation == "checkout":
                    if not branch:
                        return "Branch name is required for checkout"
                    result = subprocess.run(
                        ["git", "checkout", branch], 
                        capture_output=True, text=True, cwd=repo_path
                    )
                
                else:
                    return f"Unknown Git operation: {operation}"
            
            if result.returncode == 0:
                return f"Git {operation} successful:\n{result.stdout}"
            else:
                return f"Git {operation} failed:\n{result.stderr}"
                
        except Exception as e:
            return f"Error executing Git {operation}: {str(e)}"
