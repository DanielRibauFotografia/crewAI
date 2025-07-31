"""
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
