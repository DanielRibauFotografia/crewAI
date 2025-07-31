"""
File System Operations Tool for Development Team
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class FileSystemTool(BaseTool):
    name: str = "File System Tool"
    description: str = "Tool for file and directory operations including create, read, write, delete, and list operations"

    def _run(self, operation: str, path: str, content: Optional[str] = None, 
             destination: Optional[str] = None) -> str:
        """
        Execute file system operations
        
        Args:
            operation: Operation type (create_file, read_file, write_file, delete_file, 
                      create_dir, delete_dir, list_dir, copy_file, move_file)
            path: File or directory path
            content: Content for write operations
            destination: Destination path for copy/move operations
        """
        try:
            path_obj = Path(path)
            
            if operation == "create_file":
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                path_obj.touch()
                return f"File created: {path}"
            
            elif operation == "read_file":
                if not path_obj.exists():
                    return f"File not found: {path}"
                return path_obj.read_text(encoding='utf-8')
            
            elif operation == "write_file":
                if content is None:
                    return "Content is required for write operation"
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                path_obj.write_text(content, encoding='utf-8')
                return f"Content written to: {path}"
            
            elif operation == "delete_file":
                if path_obj.exists():
                    path_obj.unlink()
                    return f"File deleted: {path}"
                return f"File not found: {path}"
            
            elif operation == "create_dir":
                path_obj.mkdir(parents=True, exist_ok=True)
                return f"Directory created: {path}"
            
            elif operation == "delete_dir":
                if path_obj.exists():
                    shutil.rmtree(path_obj)
                    return f"Directory deleted: {path}"
                return f"Directory not found: {path}"
            
            elif operation == "list_dir":
                if not path_obj.exists():
                    return f"Directory not found: {path}"
                items = []
                for item in path_obj.iterdir():
                    item_type = "DIR" if item.is_dir() else "FILE"
                    items.append(f"{item_type}: {item.name}")
                return "\n".join(items)
            
            elif operation == "copy_file":
                if destination is None:
                    return "Destination is required for copy operation"
                if not path_obj.exists():
                    return f"Source file not found: {path}"
                dest_obj = Path(destination)
                dest_obj.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path_obj, dest_obj)
                return f"File copied from {path} to {destination}"
            
            elif operation == "move_file":
                if destination is None:
                    return "Destination is required for move operation"
                if not path_obj.exists():
                    return f"Source file not found: {path}"
                dest_obj = Path(destination)
                dest_obj.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path_obj), str(dest_obj))
                return f"File moved from {path} to {destination}"
            
            else:
                return f"Unknown operation: {operation}"
                
        except Exception as e:
            return f"Error executing {operation}: {str(e)}"
