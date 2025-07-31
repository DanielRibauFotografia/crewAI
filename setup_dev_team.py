#!/usr/bin/env python3
"""
CrewAI Development Team Setup Script
====================================

This script sets up a complete AI-powered development team using CrewAI with local models.
It creates a ready-to-use environment with pre-configured agents for software development.

Features:
- Automatic Ollama installation and model setup
- Pre-configured development team agents
- Essential development tools integration
- Local execution without paid APIs
- One-command setup

Usage: python setup_dev_team.py
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path
from typing import Dict, List

class DevTeamSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.project_name = "ai_dev_team"
        self.project_dir = self.base_dir / self.project_name
        
    def print_banner(self):
        """Print setup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CrewAI Development Team Setup                             ║
║                                                                              ║
║  🚀 Setting up your AI-powered development team                             ║
║  🤖 Local models with Ollama                                                ║
║  👥 Complete dev team: Developers, Testers, Analysts, Tech Leads           ║
║  🛠️  Pre-configured tools and workflows                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_system_requirements(self):
        """Check if system meets requirements"""
        print("🔍 Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 10) or python_version >= (3, 14):
            print("❌ Python version must be >= 3.10 and < 3.14")
            sys.exit(1)
        print(f"✅ Python {python_version.major}.{python_version.minor} detected")
        
        # Check if git is available
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            print("✅ Git is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Git is required but not found")
            sys.exit(1)
    
    def install_ollama(self):
        """Install Ollama for local LLM support"""
        print("🤖 Setting up Ollama for local AI models...")
        
        system = platform.system().lower()
        
        try:
            # Check if Ollama is already installed
            result = subprocess.run(["ollama", "--version"], capture_output=True)
            if result.returncode == 0:
                print("✅ Ollama is already installed")
                return
        except FileNotFoundError:
            pass
        
        print("📥 Installing Ollama...")
        
        if system == "linux" or system == "darwin":  # macOS
            # Download and install Ollama
            install_cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
            subprocess.run(install_cmd, shell=True, check=True)
        elif system == "windows":
            print("🪟 For Windows, please download Ollama from: https://ollama.ai/download")
            print("   After installation, run this script again.")
            sys.exit(1)
        else:
            print(f"❌ Unsupported system: {system}")
            sys.exit(1)
        
        print("✅ Ollama installed successfully")
    
    def setup_ollama_models(self):
        """Download and setup required Ollama models"""
        print("📦 Setting up AI models...")
        
        models = [
            "llama3.2:3b",      # Fast model for quick tasks
            "codellama:7b",     # Code-specialized model
            "mistral:7b"        # General purpose model
        ]
        
        for model in models:
            print(f"📥 Downloading {model}...")
            try:
                subprocess.run(["ollama", "pull", model], check=True)
                print(f"✅ {model} downloaded successfully")
            except subprocess.CalledProcessError:
                print(f"⚠️  Failed to download {model}, continuing...")
    
    def create_project_structure(self):
        """Create the development team project structure"""
        print("📁 Creating project structure...")
        
        if self.project_dir.exists():
            print(f"⚠️  Project directory {self.project_dir} already exists")
            response = input("Do you want to overwrite it? (y/N): ")
            if response.lower() != 'y':
                print("❌ Setup cancelled")
                sys.exit(1)
            shutil.rmtree(self.project_dir)
        
        # Create main project structure
        directories = [
            "src/ai_dev_team",
            "src/ai_dev_team/config",
            "src/ai_dev_team/tools",
            "src/ai_dev_team/crews",
            "src/ai_dev_team/flows",
            "templates",
            "examples",
            "docs",
            "output"
        ]
        
        for directory in directories:
            (self.project_dir / directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ Project structure created")
    
    def create_configuration_files(self):
        """Create configuration files"""
        print("⚙️  Creating configuration files...")
        
        # Create .env file
        env_content = """# CrewAI Development Team Configuration
# Local Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LLM_MODEL=llama3.2:3b
CODE_LLM_MODEL=codellama:7b
ANALYSIS_LLM_MODEL=mistral:7b

# Optional: Add API keys for additional tools
# SERPER_API_KEY=your_serper_key_here
# GITHUB_TOKEN=your_github_token_here

# Project Settings
PROJECT_NAME=AI Development Team
OUTPUT_DIR=./output
VERBOSE=true
"""
        
        with open(self.project_dir / ".env", "w") as f:
            f.write(env_content)
        
        # Create pyproject.toml
        pyproject_content = """[project]
name = "ai-dev-team"
version = "1.0.0"
description = "AI-powered development team using CrewAI with local models"
requires-python = ">=3.10,<3.14"
dependencies = [
    "crewai[tools]>=0.80.0",
    "ollama>=0.3.0",
    "python-dotenv>=1.0.0",
    "gitpython>=3.1.0",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "selenium>=4.15.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
    "pytest>=7.4.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "bandit>=1.7.0",
    "safety>=2.3.0",
    "pre-commit>=3.4.0",
]

[project.scripts]
dev-team = "ai_dev_team.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""
        
        with open(self.project_dir / "pyproject.toml", "w") as f:
            f.write(pyproject_content)
        
        print("✅ Configuration files created")
    
    def create_agents_config(self):
        """Create agents configuration"""
        print("👥 Creating development team agents...")
        
        agents_config = """# Development Team Agents Configuration

# Senior Software Developer
senior_developer:
  role: >
    Senior Software Developer
  goal: >
    Design and implement high-quality, scalable software solutions following best practices
  backstory: >
    You are a seasoned software developer with 10+ years of experience in multiple programming 
    languages and frameworks. You excel at writing clean, maintainable code and have deep 
    knowledge of software architecture patterns, design principles, and modern development practices.
    You mentor junior developers and lead technical discussions.
  max_iter: 3
  max_execution_time: 300

# Frontend Developer
frontend_developer:
  role: >
    Frontend Developer
  goal: >
    Create responsive, user-friendly interfaces with modern web technologies
  backstory: >
    You are a skilled frontend developer specializing in modern JavaScript frameworks like React, 
    Vue, and Angular. You have expertise in HTML5, CSS3, responsive design, and user experience 
    principles. You stay updated with the latest frontend trends and tools.
  max_iter: 3
  max_execution_time: 300

# Backend Developer
backend_developer:
  role: >
    Backend Developer
  goal: >
    Build robust, scalable server-side applications and APIs
  backstory: >
    You are an experienced backend developer with expertise in server-side technologies, 
    databases, API design, and cloud services. You understand microservices architecture, 
    security best practices, and performance optimization.
  max_iter: 3
  max_execution_time: 300

# DevOps Engineer
devops_engineer:
  role: >
    DevOps Engineer
  goal: >
    Implement CI/CD pipelines, infrastructure automation, and deployment strategies
  backstory: >
    You are a DevOps engineer with expertise in containerization, orchestration, cloud platforms, 
    and infrastructure as code. You focus on automation, monitoring, and ensuring reliable, 
    scalable deployments.
  max_iter: 3
  max_execution_time: 300

# QA Engineer
qa_engineer:
  role: >
    Quality Assurance Engineer
  goal: >
    Ensure software quality through comprehensive testing strategies and automation
  backstory: >
    You are a meticulous QA engineer with experience in manual and automated testing. 
    You understand various testing methodologies, tools, and frameworks. You focus on 
    finding bugs, ensuring quality, and improving testing processes.
  max_iter: 3
  max_execution_time: 300

# Technical Lead
tech_lead:
  role: >
    Technical Lead
  goal: >
    Provide technical leadership, make architectural decisions, and coordinate development efforts
  backstory: >
    You are a technical leader with extensive experience in software development and team 
    management. You make high-level technical decisions, review code, mentor team members, 
    and ensure projects meet technical requirements and deadlines.
  max_iter: 3
  max_execution_time: 300

# Business Analyst
business_analyst:
  role: >
    Business Analyst
  goal: >
    Analyze business requirements and translate them into technical specifications
  backstory: >
    You are a business analyst who bridges the gap between business stakeholders and 
    technical teams. You excel at gathering requirements, creating documentation, 
    and ensuring solutions meet business needs.
  max_iter: 3
  max_execution_time: 300

# Security Specialist
security_specialist:
  role: >
    Security Specialist
  goal: >
    Identify security vulnerabilities and implement security best practices
  backstory: >
    You are a cybersecurity expert with deep knowledge of application security, 
    penetration testing, and security frameworks. You focus on identifying vulnerabilities 
    and implementing security measures to protect applications and data.
  max_iter: 3
  max_execution_time: 300

# Database Administrator
database_admin:
  role: >
    Database Administrator
  goal: >
    Design, optimize, and maintain database systems for optimal performance
  backstory: >
    You are a database expert with experience in various database systems, query optimization, 
    backup strategies, and data modeling. You ensure data integrity, performance, and availability.
  max_iter: 3
  max_execution_time: 300

# UI/UX Designer
ui_ux_designer:
  role: >
    UI/UX Designer
  goal: >
    Create intuitive, user-centered designs and improve user experience
  backstory: >
    You are a creative UI/UX designer with expertise in user research, wireframing, 
    prototyping, and design systems. You focus on creating beautiful, functional 
    interfaces that provide excellent user experiences.
  max_iter: 3
  max_execution_time: 300
"""
        
        with open(self.project_dir / "src/ai_dev_team/config/agents.yaml", "w") as f:
            f.write(agents_config)
        
        print("✅ Agents configuration created")
    
    def create_tasks_config(self):
        """Create tasks configuration"""
        print("📋 Creating development tasks...")
        
        tasks_config = """# Development Team Tasks Configuration

# Project Analysis Task
analyze_project:
  description: >
    Analyze the project requirements: {project_description}
    
    Consider the following aspects:
    - Technical requirements and constraints
    - Architecture and design patterns
    - Technology stack recommendations
    - Timeline and resource estimation
    - Risk assessment and mitigation strategies
    
    Provide a comprehensive analysis with actionable recommendations.
  expected_output: >
    A detailed project analysis document including:
    - Executive summary
    - Technical requirements breakdown
    - Recommended architecture and technology stack
    - Development timeline and milestones
    - Risk assessment and mitigation plan
    - Resource allocation recommendations
  agent: business_analyst

# Architecture Design Task
design_architecture:
  description: >
    Based on the project analysis, design a comprehensive software architecture for: {project_description}
    
    Include:
    - System architecture diagram
    - Component breakdown and responsibilities
    - Data flow and integration points
    - Security considerations
    - Scalability and performance requirements
    - Technology stack justification
  expected_output: >
    A complete architecture design document with:
    - High-level system architecture
    - Detailed component specifications
    - Database schema design
    - API specifications
    - Security architecture
    - Deployment architecture
  agent: tech_lead

# Backend Development Task
develop_backend:
  description: >
    Implement the backend components for: {project_description}
    
    Based on the architecture design, create:
    - RESTful API endpoints
    - Database models and migrations
    - Business logic implementation
    - Authentication and authorization
    - Error handling and logging
    - Unit tests for backend components
  expected_output: >
    Complete backend implementation including:
    - Source code with proper structure
    - API documentation
    - Database setup scripts
    - Configuration files
    - Unit tests with good coverage
    - Deployment instructions
  agent: backend_developer

# Frontend Development Task
develop_frontend:
  description: >
    Create the frontend application for: {project_description}
    
    Implement:
    - User interface components
    - State management
    - API integration
    - Responsive design
    - User experience optimizations
    - Frontend testing
  expected_output: >
    Complete frontend application with:
    - Source code with component structure
    - Responsive UI implementation
    - API integration layer
    - State management setup
    - Frontend tests
    - Build and deployment configuration
  agent: frontend_developer

# Database Design Task
design_database:
  description: >
    Design and implement the database schema for: {project_description}
    
    Create:
    - Entity-relationship diagrams
    - Database schema with proper normalization
    - Indexes for performance optimization
    - Data migration scripts
    - Backup and recovery procedures
  expected_output: >
    Complete database design including:
    - ER diagrams and schema documentation
    - SQL scripts for table creation
    - Index optimization recommendations
    - Data migration procedures
    - Backup and recovery plan
  agent: database_admin

# Security Assessment Task
assess_security:
  description: >
    Perform a comprehensive security assessment for: {project_description}
    
    Evaluate:
    - Authentication and authorization mechanisms
    - Data encryption and protection
    - Input validation and sanitization
    - API security measures
    - Infrastructure security
    - Compliance requirements
  expected_output: >
    Security assessment report with:
    - Identified vulnerabilities and risks
    - Security recommendations and best practices
    - Implementation guidelines
    - Compliance checklist
    - Security testing procedures
  agent: security_specialist

# Testing Strategy Task
create_testing_strategy:
  description: >
    Develop a comprehensive testing strategy for: {project_description}
    
    Include:
    - Test planning and strategy
    - Unit testing framework setup
    - Integration testing procedures
    - End-to-end testing scenarios
    - Performance testing guidelines
    - Test automation implementation
  expected_output: >
    Complete testing strategy document with:
    - Test plan and coverage requirements
    - Testing framework recommendations
    - Automated test suites
    - Performance testing procedures
    - Quality assurance checklist
    - Bug tracking and reporting process
  agent: qa_engineer

# DevOps Setup Task
setup_devops:
  description: >
    Set up DevOps infrastructure and CI/CD pipeline for: {project_description}
    
    Implement:
    - Version control workflow
    - Continuous integration pipeline
    - Automated deployment process
    - Infrastructure as code
    - Monitoring and logging
    - Container orchestration
  expected_output: >
    Complete DevOps setup including:
    - CI/CD pipeline configuration
    - Infrastructure automation scripts
    - Deployment procedures
    - Monitoring and alerting setup
    - Documentation for operations
    - Disaster recovery procedures
  agent: devops_engineer

# UI/UX Design Task
design_user_experience:
  description: >
    Create user experience design for: {project_description}
    
    Develop:
    - User personas and journey maps
    - Wireframes and mockups
    - Interactive prototypes
    - Design system and style guide
    - Accessibility considerations
    - Usability testing plan
  expected_output: >
    Complete UX design package with:
    - User research and personas
    - Wireframes and high-fidelity mockups
    - Interactive prototype
    - Design system documentation
    - Accessibility guidelines
    - Usability testing procedures
  agent: ui_ux_designer

# Code Review Task
review_code:
  description: >
    Perform comprehensive code review for the project: {project_description}
    
    Review:
    - Code quality and best practices
    - Architecture adherence
    - Security considerations
    - Performance optimizations
    - Documentation completeness
    - Test coverage
  expected_output: >
    Code review report including:
    - Code quality assessment
    - Identified issues and recommendations
    - Best practices compliance
    - Security review findings
    - Performance optimization suggestions
    - Documentation review
  agent: senior_developer
"""
        
        with open(self.project_dir / "src/ai_dev_team/config/tasks.yaml", "w") as f:
            f.write(tasks_config)
        
        print("✅ Tasks configuration created")
    
    def create_development_tools(self):
        """Create development tools"""
        print("🛠️  Creating development tools...")
        
        # File System Tool
        file_tool_content = '''"""
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
'''
        
        with open(self.project_dir / "src/ai_dev_team/tools/file_system_tool.py", "w") as f:
            f.write(file_tool_content)
        
        # Git Tool
        git_tool_content = '''"""
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
                return f"Git {operation} failed:\\n{result.stderr}"
                
        except Exception as e:
            return f"Error executing Git {operation}: {str(e)}"
'''
        
        with open(self.project_dir / "src/ai_dev_team/tools/git_tool.py", "w") as f:
            f.write(git_tool_content)
        
        # Code Analysis Tool
        code_analysis_tool_content = '''"""
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
                    return f"Complexity Analysis:\\n{result.stdout}"
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
                return f"Linting Issues:\\n{result.stdout}"
            else:
                return "No linting issues found"
                
        except Exception as e:
            return f"Error linting code: {str(e)}"
    
    def _analyze_code_quality(self, file_path: Path, language: str) -> str:
        """General code quality analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\\n')
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if not line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            
            result = f"Code Quality Analysis for {file_path.name}:\\n"
            result += f"Total lines: {total_lines}\\n"
            result += f"Blank lines: {blank_lines}\\n"
            result += f"Comment lines: {comment_lines}\\n"
            result += f"Code lines: {total_lines - blank_lines - comment_lines}\\n"
            result += f"Comment ratio: {comment_lines / total_lines * 100:.1f}%"
            
            return result
            
        except Exception as e:
            return f"Error analyzing code quality: {str(e)}"
'''
        
        with open(self.project_dir / "src/ai_dev_team/tools/code_analysis_tool.py", "w") as f:
            f.write(code_analysis_tool_content)
        
        # Web Research Tool
        web_research_tool_content = '''"""
Web Research Tool for Development Team
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
from crewai.tools import BaseTool


class WebResearchTool(BaseTool):
    name: str = "Web Research Tool"
    description: str = "Tool for web research, documentation lookup, and technology information gathering"

    def _run(self, operation: str, query: str, url: Optional[str] = None) -> str:
        """
        Perform web research operations
        
        Args:
            operation: Research type (search, scrape, documentation)
            query: Search query or content to look for
            url: Specific URL to scrape (optional)
        """
        try:
            if operation == "search":
                return self._search_web(query)
            
            elif operation == "scrape" and url:
                return self._scrape_url(url)
            
            elif operation == "documentation":
                return self._search_documentation(query)
            
            else:
                return f"Unknown operation: {operation}"
                
        except Exception as e:
            return f"Error in web research: {str(e)}"
    
    def _search_web(self, query: str) -> str:
        """Search web for information"""
        try:
            # Using DuckDuckGo Instant Answer API (no API key required)
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                result = f"Search results for: {query}\\n\\n"
                
                if data.get('Abstract'):
                    result += f"Summary: {data['Abstract']}\\n\\n"
                
                if data.get('RelatedTopics'):
                    result += "Related Topics:\\n"
                    for topic in data['RelatedTopics'][:5]:
                        if isinstance(topic, dict) and 'Text' in topic:
                            result += f"- {topic['Text']}\\n"
                
                return result if len(result) > 50 else "No detailed results found for this query"
            
            else:
                return f"Search failed with status code: {response.status_code}"
                
        except Exception as e:
            return f"Error searching web: {str(e)}"
    
    def _scrape_url(self, url: str) -> str:
        """Scrape content from a specific URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                # Limit text length
                if len(text) > 2000:
                    text = text[:2000] + "... (truncated)"
                
                return f"Content from {url}:\\n\\n{text}"
            
            else:
                return f"Failed to scrape URL. Status code: {response.status_code}"
                
        except Exception as e:
            return f"Error scraping URL: {str(e)}"
    
    def _search_documentation(self, query: str) -> str:
        """Search for documentation and technical resources"""
        try:
            # Search for documentation on common sites
            doc_sites = [
                f"site:docs.python.org {query}",
                f"site:developer.mozilla.org {query}",
                f"site:stackoverflow.com {query}",
                f"site:github.com {query}"
            ]
            
            results = []
            for site_query in doc_sites[:2]:  # Limit to 2 sites to avoid rate limiting
                try:
                    search_result = self._search_web(site_query)
                    if search_result and "No detailed results" not in search_result:
                        results.append(search_result)
                except:
                    continue
            
            if results:
                return "\\n\\n".join(results)
            else:
                return f"No documentation found for: {query}"
                
        except Exception as e:
            return f"Error searching documentation: {str(e)}"
'''
        
        with open(self.project_dir / "src/ai_dev_team/tools/web_research_tool.py", "w") as f:
            f.write(web_research_tool_content)
        
        # Tools __init__.py
        tools_init_content = '''"""
Development Team Tools
"""

from .file_system_tool import FileSystemTool
from .git_tool import GitTool
from .code_analysis_tool import CodeAnalysisTool
from .web_research_tool import WebResearchTool

__all__ = [
    "FileSystemTool",
    "GitTool", 
    "CodeAnalysisTool",
    "WebResearchTool"
]
'''
        
        with open(self.project_dir / "src/ai_dev_team/tools/__init__.py", "w") as f:
            f.write(tools_init_content)
        
        print("✅ Development tools created")
    
    def create_main_crew_file(self):
        """Create the main crew file"""
        print("🎯 Creating main crew implementation...")
        
        crew_content = '''"""
AI Development Team Crew
"""

import os
from typing import List, Dict, Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.llm import LLM

from .tools import FileSystemTool, GitTool, CodeAnalysisTool, WebResearchTool


@CrewBase
class AiDevTeamCrew:
    """AI Development Team Crew"""
    
    def __init__(self):
        # Initialize LLM with Ollama
        self.llm = LLM(
            model=f"ollama/{os.getenv('DEFAULT_LLM_MODEL', 'llama3.2:3b')}",
            base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        )
        
        self.code_llm = LLM(
            model=f"ollama/{os.getenv('CODE_LLM_MODEL', 'codellama:7b')}",
            base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        )
        
        # Initialize tools
        self.file_tool = FileSystemTool()
        self.git_tool = GitTool()
        self.code_tool = CodeAnalysisTool()
        self.web_tool = WebResearchTool()
        
        # Common tools for all agents
        self.common_tools = [
            self.file_tool,
            self.git_tool,
            self.code_tool,
            self.web_tool
        ]

    @agent
    def senior_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_developer'],
            llm=self.code_llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            llm=self.code_llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            llm=self.code_llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def tech_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_lead'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def security_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['security_specialist'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def database_admin(self) -> Agent:
        return Agent(
            config=self.agents_config['database_admin'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    @agent
    def ui_ux_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_ux_designer'],
            llm=self.llm,
            tools=self.common_tools,
            verbose=True
        )

    # Tasks
    @task
    def analyze_project(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_project'],
            agent=self.business_analyst(),
            output_file='output/project_analysis.md'
        )

    @task
    def design_architecture(self) -> Task:
        return Task(
            config=self.tasks_config['design_architecture'],
            agent=self.tech_lead(),
            output_file='output/architecture_design.md'
        )

    @task
    def develop_backend(self) -> Task:
        return Task(
            config=self.tasks_config['develop_backend'],
            agent=self.backend_developer(),
            output_file='output/backend_implementation.md'
        )

    @task
    def develop_frontend(self) -> Task:
        return Task(
            config=self.tasks_config['develop_frontend'],
            agent=self.frontend_developer(),
            output_file='output/frontend_implementation.md'
        )

    @task
    def design_database(self) -> Task:
        return Task(
            config=self.tasks_config['design_database'],
            agent=self.database_admin(),
            output_file='output/database_design.md'
        )

    @task
    def assess_security(self) -> Task:
        return Task(
            config=self.tasks_config['assess_security'],
            agent=self.security_specialist(),
            output_file='output/security_assessment.md'
        )

    @task
    def create_testing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['create_testing_strategy'],
            agent=self.qa_engineer(),
            output_file='output/testing_strategy.md'
        )

    @task
    def setup_devops(self) -> Task:
        return Task(
            config=self.tasks_config['setup_devops'],
            agent=self.devops_engineer(),
            output_file='output/devops_setup.md'
        )

    @task
    def design_user_experience(self) -> Task:
        return Task(
            config=self.tasks_config['design_user_experience'],
            agent=self.ui_ux_designer(),
            output_file='output/ux_design.md'
        )

    @task
    def review_code(self) -> Task:
        return Task(
            config=self.tasks_config['review_code'],
            agent=self.senior_developer(),
            output_file='output/code_review.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AI Development Team crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "nomic-embed-text",
                    "base_url": os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                }
            }
        )
    
    def create_custom_crew(self, agents_list: List[str], tasks_list: List[str]) -> Crew:
        """Create a custom crew with specific agents and tasks"""
        
        # Map agent names to agent methods
        agent_map = {
            'senior_developer': self.senior_developer,
            'frontend_developer': self.frontend_developer,
            'backend_developer': self.backend_developer,
            'devops_engineer': self.devops_engineer,
            'qa_engineer': self.qa_engineer,
            'tech_lead': self.tech_lead,
            'business_analyst': self.business_analyst,
            'security_specialist': self.security_specialist,
            'database_admin': self.database_admin,
            'ui_ux_designer': self.ui_ux_designer
        }
        
        # Map task names to task methods
        task_map = {
            'analyze_project': self.analyze_project,
            'design_architecture': self.design_architecture,
            'develop_backend': self.develop_backend,
            'develop_frontend': self.develop_frontend,
            'design_database': self.design_database,
            'assess_security': self.assess_security,
            'create_testing_strategy': self.create_testing_strategy,
            'setup_devops': self.setup_devops,
            'design_user_experience': self.design_user_experience,
            'review_code': self.review_code
        }
        
        # Create selected agents and tasks
        selected_agents = [agent_map[name]() for name in agents_list if name in agent_map]
        selected_tasks = [task_map[name]() for name in tasks_list if name in task_map]
        
        return Crew(
            agents=selected_agents,
            tasks=selected_tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder={
                "provider": "ollama",
                "config": {
                    "model": "nomic-embed-text",
                    "base_url": os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                }
            }
        )
'''
        
        with open(self.project_dir / "src/ai_dev_team/crew.py", "w") as f:
            f.write(crew_content)
        
        print("✅ Main crew file created")
    
    def create_main_script(self):
        """Create the main execution script"""
        print("🚀 Creating main execution script...")
        
        main_content = '''#!/usr/bin/env python3
"""
AI Development Team - Main Execution Script
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from ai_dev_team.crew import AiDevTeamCrew


def main():
    """Main execution function"""
    
    # Load environment variables
    load_dotenv()
    
    print("🤖 AI Development Team Starting...")
    print("=" * 60)
    
    # Get project description from user
    if len(sys.argv) > 1:
        project_description = " ".join(sys.argv[1:])
    else:
        project_description = input("📝 Enter your project description: ")
    
    if not project_description.strip():
        print("❌ Project description is required!")
        sys.exit(1)
    
    print(f"🎯 Project: {project_description}")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize the crew
    try:
        crew_instance = AiDevTeamCrew()
        crew = crew_instance.crew()
        
        # Prepare inputs
        inputs = {
            'project_description': project_description
        }
        
        print("🚀 Starting development team workflow...")
        print("This may take several minutes depending on the project complexity.")
        print("=" * 60)
        
        # Execute the crew
        result = crew.kickoff(inputs=inputs)
        
        print("=" * 60)
        print("✅ Development team workflow completed!")
        print(f"📁 Results saved in: {output_dir.absolute()}")
        print("=" * 60)
        
        # Print summary
        print("📋 Generated Documents:")
        for file in output_dir.glob("*.md"):
            print(f"   - {file.name}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error executing crew: {str(e)}")
        sys.exit(1)


def run_custom_workflow():
    """Run a custom workflow with selected agents and tasks"""
    
    load_dotenv()
    
    print("🎛️  Custom AI Development Team Workflow")
    print("=" * 60)
    
    # Available agents
    available_agents = [
        'senior_developer', 'frontend_developer', 'backend_developer',
        'devops_engineer', 'qa_engineer', 'tech_lead', 'business_analyst',
        'security_specialist', 'database_admin', 'ui_ux_designer'
    ]
    
    # Available tasks
    available_tasks = [
        'analyze_project', 'design_architecture', 'develop_backend',
        'develop_frontend', 'design_database', 'assess_security',
        'create_testing_strategy', 'setup_devops', 'design_user_experience',
        'review_code'
    ]
    
    print("Available Agents:")
    for i, agent in enumerate(available_agents, 1):
        print(f"  {i}. {agent}")
    
    print("\\nAvailable Tasks:")
    for i, task in enumerate(available_tasks, 1):
        print(f"  {i}. {task}")
    
    # Get user selections
    print("\\n" + "=" * 60)
    agent_selection = input("Select agents (comma-separated numbers or names): ").strip()
    task_selection = input("Select tasks (comma-separated numbers or names): ").strip()
    project_description = input("Enter project description: ").strip()
    
    if not all([agent_selection, task_selection, project_description]):
        print("❌ All fields are required!")
        sys.exit(1)
    
    # Parse selections
    def parse_selection(selection, available_list):
        selected = []
        for item in selection.split(','):
            item = item.strip()
            if item.isdigit():
                idx = int(item) - 1
                if 0 <= idx < len(available_list):
                    selected.append(available_list[idx])
            elif item in available_list:
                selected.append(item)
        return selected
    
    selected_agents = parse_selection(agent_selection, available_agents)
    selected_tasks = parse_selection(task_selection, available_tasks)
    
    if not selected_agents or not selected_tasks:
        print("❌ Invalid agent or task selection!")
        sys.exit(1)
    
    print(f"\\n🎯 Selected Agents: {', '.join(selected_agents)}")
    print(f"🎯 Selected Tasks: {', '.join(selected_tasks)}")
    print(f"🎯 Project: {project_description}")
    print("=" * 60)
    
    # Create and run custom crew
    try:
        crew_instance = AiDevTeamCrew()
        custom_crew = crew_instance.create_custom_crew(selected_agents, selected_tasks)
        
        inputs = {'project_description': project_description}
        
        print("🚀 Starting custom workflow...")
        result = custom_crew.kickoff(inputs=inputs)
        
        print("✅ Custom workflow completed!")
        return result
        
    except Exception as e:
        print(f"❌ Error executing custom workflow: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--custom":
        run_custom_workflow()
    else:
        main()
'''
        
        with open(self.project_dir / "src/ai_dev_team/main.py", "w") as f:
            f.write(main_content)
        
        # Create __init__.py files
        init_content = '''"""
AI Development Team - CrewAI Based Development Team
"""

__version__ = "1.0.0"
'''
        
        with open(self.project_dir / "src/ai_dev_team/__init__.py", "w") as f:
            f.write(init_content)
        
        with open(self.project_dir / "src/__init__.py", "w") as f:
            f.write("")
        
        print("✅ Main execution script created")
    
    def create_examples_and_templates(self):
        """Create example projects and templates"""
        print("📚 Creating examples and templates...")
        
        # Example 1: Web Application
        web_app_example = '''# Web Application Development Example

## Usage
```bash
cd ai_dev_team
python src/ai_dev_team/main.py "Create a modern web application for task management with user authentication, real-time updates, and mobile responsiveness. Include features like project creation, task assignment, progress tracking, and team collaboration tools."
```

## Expected Output
- Project analysis and requirements
- System architecture design
- Backend API implementation plan
- Frontend application design
- Database schema
- Security assessment
- Testing strategy
- DevOps setup guide
- UI/UX design recommendations
- Code review guidelines

## Agents Involved
- Business Analyst
- Tech Lead
- Backend Developer
- Frontend Developer
- Database Administrator
- Security Specialist
- QA Engineer
- DevOps Engineer
- UI/UX Designer
- Senior Developer
'''
        
        with open(self.project_dir / "examples/web_application.md", "w") as f:
            f.write(web_app_example)
        
        # Example 2: API Development
        api_example = '''# REST API Development Example

## Usage
```bash
cd ai_dev_team
python src/ai_dev_team/main.py --custom
# Select: backend_developer, database_admin, security_specialist, qa_engineer
# Select: analyze_project, design_architecture, develop_backend, design_database, assess_security, create_testing_strategy
```

## Project Description
"Develop a RESTful API for an e-commerce platform with product catalog, user management, order processing, payment integration, and inventory management."

## Expected Output
- API architecture and design
- Database schema for e-commerce
- Backend implementation plan
- Security measures and authentication
- Testing strategy for APIs
- Documentation and deployment guide
'''
        
        with open(self.project_dir / "examples/api_development.md", "w") as f:
            f.write(api_example)
        
        # Example 3: Mobile App
        mobile_app_example = '''# Mobile Application Development Example

## Usage
```bash
cd ai_dev_team
python src/ai_dev_team/main.py "Design and develop a cross-platform mobile application for fitness tracking with features like workout logging, progress visualization, social sharing, and integration with wearable devices."
```

## Focus Areas
- Cross-platform development strategy
- Mobile UI/UX design principles
- Backend API for mobile clients
- Data synchronization and offline support
- Performance optimization
- Security for mobile applications
- Testing on multiple devices
- App store deployment strategy
'''
        
        with open(self.project_dir / "examples/mobile_application.md", "w") as f:
            f.write(mobile_app_example)
        
        # Quick Start Guide
        quick_start = '''# AI Development Team - Quick Start Guide

## Prerequisites
- Python 3.10+ installed
- Ollama installed and running
- Git installed

## Quick Setup
1. Run the setup script:
   ```bash
   python setup_dev_team.py
   ```

2. Navigate to the project:
   ```bash
   cd ai_dev_team
   ```

3. Start your first project:
   ```bash
   python src/ai_dev_team/main.py "Your project description here"
   ```

## Available Commands

### Full Development Workflow
```bash
python src/ai_dev_team/main.py "Create a web application for..."
```

### Custom Workflow
```bash
python src/ai_dev_team/main.py --custom
```

### Environment Variables
Edit `.env` file to customize:
- `DEFAULT_LLM_MODEL`: Default language model
- `CODE_LLM_MODEL`: Model for code-related tasks
- `OLLAMA_BASE_URL`: Ollama server URL

## Team Members

### Core Development Team
- **Senior Developer**: Code architecture and best practices
- **Frontend Developer**: User interface and client-side development
- **Backend Developer**: Server-side logic and APIs
- **DevOps Engineer**: Infrastructure and deployment
- **QA Engineer**: Testing and quality assurance

### Specialized Roles
- **Tech Lead**: Technical leadership and coordination
- **Business Analyst**: Requirements analysis and documentation
- **Security Specialist**: Security assessment and implementation
- **Database Administrator**: Database design and optimization
- **UI/UX Designer**: User experience and interface design

## Output Files
All results are saved in the `output/` directory:
- `project_analysis.md`: Business requirements and analysis
- `architecture_design.md`: System architecture and design
- `backend_implementation.md`: Backend development plan
- `frontend_implementation.md`: Frontend development plan
- `database_design.md`: Database schema and design
- `security_assessment.md`: Security analysis and recommendations
- `testing_strategy.md`: Testing plan and procedures
- `devops_setup.md`: Infrastructure and deployment guide
- `ux_design.md`: User experience design
- `code_review.md`: Code quality and review guidelines

## Tips for Best Results
1. **Be Specific**: Provide detailed project descriptions
2. **Include Context**: Mention target audience, scale, and constraints
3. **Specify Technology**: If you have preferences, include them
4. **Define Scope**: Clearly outline what you want to build
5. **Mention Requirements**: Include any specific requirements or constraints

## Example Project Descriptions

### Good Examples
- "Create a modern e-commerce web application with React frontend, Node.js backend, PostgreSQL database, supporting 10,000+ concurrent users, with features like product catalog, shopping cart, payment processing, and admin dashboard."

- "Develop a mobile-first task management application using React Native, with offline support, real-time synchronization, team collaboration features, and integration with popular calendar applications."

### Avoid Vague Descriptions
- "Build an app"
- "Create a website"
- "Make something cool"

## Troubleshooting

### Ollama Issues
- Ensure Ollama is running: `ollama serve`
- Check available models: `ollama list`
- Pull required models: `ollama pull llama3.2:3b`

### Performance Tips
- Use smaller models for faster responses
- Limit the number of agents for simple projects
- Use custom workflows for specific needs

## Support
For issues and questions:
1. Check the examples in the `examples/` directory
2. Review the configuration in `.env` file
3. Ensure all dependencies are installed
4. Verify Ollama is running and models are available
'''
        
        with open(self.project_dir / "README.md", "w") as f:
            f.write(quick_start)
        
        print("✅ Examples and templates created")
    
    def create_startup_script(self):
        """Create a startup script for easy execution"""
        print("🎬 Creating startup script...")
        
        startup_script = '''#!/bin/bash

# AI Development Team Startup Script

echo "🤖 AI Development Team - Startup Script"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "src/ai_dev_team/main.py" ]; then
    echo "❌ Please run this script from the ai_dev_team directory"
    exit 1
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Check if required models are available
echo "🔍 Checking AI models..."
if ! ollama list | grep -q "llama3.2:3b"; then
    echo "📥 Downloading llama3.2:3b model..."
    ollama pull llama3.2:3b
fi

if ! ollama list | grep -q "codellama:7b"; then
    echo "📥 Downloading codellama:7b model..."
    ollama pull codellama:7b
fi

if ! ollama list | grep -q "nomic-embed-text"; then
    echo "📥 Downloading nomic-embed-text model..."
    ollama pull nomic-embed-text
fi

echo "✅ All models ready!"
echo ""

# Show usage options
echo "🎯 Usage Options:"
echo "1. Full development workflow:"
echo "   python src/ai_dev_team/main.py \"Your project description\""
echo ""
echo "2. Custom workflow:"
echo "   python src/ai_dev_team/main.py --custom"
echo ""
echo "3. Interactive mode:"
echo "   python src/ai_dev_team/main.py"
echo ""

# Ask user what they want to do
read -p "Choose an option (1/2/3) or press Enter to exit: " choice

case $choice in
    1)
        read -p "Enter your project description: " project_desc
        python src/ai_dev_team/main.py "$project_desc"
        ;;
    2)
        python src/ai_dev_team/main.py --custom
        ;;
    3)
        python src/ai_dev_team/main.py
        ;;
    *)
        echo "👋 Goodbye!"
        ;;
esac
'''
        
        with open(self.project_dir / "start.sh", "w") as f:
            f.write(startup_script)
        
        # Make it executable
        os.chmod(self.project_dir / "start.sh", 0o755)
        
        # Windows batch file
        windows_script = '''@echo off
echo 🤖 AI Development Team - Startup Script
echo ======================================

REM Check if we're in the right directory
if not exist "src\\ai_dev_team\\main.py" (
    echo ❌ Please run this script from the ai_dev_team directory
    pause
    exit /b 1
)

REM Check if Ollama is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo 🚀 Starting Ollama...
    start /B ollama serve
    timeout /t 5 /nobreak >nul
)

echo 🔍 Checking AI models...
ollama list | findstr "llama3.2:3b" >nul
if errorlevel 1 (
    echo 📥 Downloading llama3.2:3b model...
    ollama pull llama3.2:3b
)

ollama list | findstr "codellama:7b" >nul
if errorlevel 1 (
    echo 📥 Downloading codellama:7b model...
    ollama pull codellama:7b
)

ollama list | findstr "nomic-embed-text" >nul
if errorlevel 1 (
    echo 📥 Downloading nomic-embed-text model...
    ollama pull nomic-embed-text
)

echo ✅ All models ready!
echo.

echo 🎯 Usage Options:
echo 1. Full development workflow:
echo    python src\\ai_dev_team\\main.py "Your project description"
echo.
echo 2. Custom workflow:
echo    python src\\ai_dev_team\\main.py --custom
echo.
echo 3. Interactive mode:
echo    python src\\ai_dev_team\\main.py
echo.

set /p choice="Choose an option (1/2/3) or press Enter to exit: "

if "%choice%"=="1" (
    set /p project_desc="Enter your project description: "
    python src\\ai_dev_team\\main.py "%project_desc%"
) else if "%choice%"=="2" (
    python src\\ai_dev_team\\main.py --custom
) else if "%choice%"=="3" (
    python src\\ai_dev_team\\main.py
) else (
    echo 👋 Goodbye!
)

pause
'''
        
        with open(self.project_dir / "start.bat", "w") as f:
            f.write(windows_script)
        
        print("✅ Startup scripts created")
    
    def install_dependencies(self):
        """Install project dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            # Change to project directory
            os.chdir(self.project_dir)
            
            # Install dependencies using pip
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-e", "."
            ], check=True)
            
            print("✅ Dependencies installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Failed to install dependencies: {e}")
            print("You can install them manually later with: pip install -e .")
    
    def run_setup(self):
        """Run the complete setup process"""
        try:
            self.print_banner()
            self.check_system_requirements()
            self.install_ollama()
            self.setup_ollama_models()
            self.create_project_structure()
            self.create_configuration_files()
            self.create_agents_config()
            self.create_tasks_config()
            self.create_development_tools()
            self.create_main_crew_file()
            self.create_main_script()
            self.create_examples_and_templates()
            self.create_startup_script()
            self.install_dependencies()
            
            # Final success message
            success_message = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🎉 SETUP COMPLETED! 🎉                             ║
║                                                                              ║
║  Your AI Development Team is ready to use!                                  ║
║                                                                              ║
║  📁 Project Location: {self.project_dir}                    ║
║                                                                              ║
║  🚀 Quick Start:                                                             ║
║     cd {self.project_name}                                                   ║
║     ./start.sh  (Linux/Mac) or start.bat (Windows)                          ║
║                                                                              ║
║  📖 Or read the README.md for detailed instructions                         ║
║                                                                              ║
║  🤖 Your team includes:                                                      ║
║     • Senior Developer    • Frontend Developer   • Backend Developer        ║
║     • DevOps Engineer     • QA Engineer         • Tech Lead                 ║
║     • Business Analyst    • Security Specialist • Database Admin           ║
║     • UI/UX Designer                                                         ║
║                                                                              ║
║  🛠️  Pre-configured with local AI models (no API costs!)                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
            """
            
            print(success_message)
            
        except KeyboardInterrupt:
            print("\n❌ Setup interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Setup failed: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    setup = DevTeamSetup()
    setup.run_setup()