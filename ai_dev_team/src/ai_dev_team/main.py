#!/usr/bin/env python3
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
    
    print("\nAvailable Tasks:")
    for i, task in enumerate(available_tasks, 1):
        print(f"  {i}. {task}")
    
    # Get user selections
    print("\n" + "=" * 60)
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
    
    print(f"\n🎯 Selected Agents: {', '.join(selected_agents)}")
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
