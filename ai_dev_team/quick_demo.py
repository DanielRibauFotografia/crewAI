#!/usr/bin/env python3
"""
Quick Demo - AI Development Team
Simple demonstration of the AI development team capabilities
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM

# Load environment variables
load_dotenv()

def create_simple_demo():
    """Create a simple demo with fewer agents for faster execution"""
    
    print("🚀 AI Development Team - Quick Demo")
    print("=" * 50)
    
    # Initialize LLM with Ollama
    llm = LLM(
        model=f"ollama/{os.getenv('DEFAULT_LLM_MODEL', 'llama3.2:3b')}",
        base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    )
    
    # Create a simple business analyst agent
    business_analyst = Agent(
        role="Business Analyst",
        goal="Analyze project requirements and create technical specifications",
        backstory="""You are an experienced business analyst who excels at understanding 
        project requirements and translating them into clear technical specifications.""",
        llm=llm,
        verbose=True,
        max_iter=2,
        max_execution_time=60
    )
    
    # Create a simple developer agent
    developer = Agent(
        role="Senior Developer",
        goal="Design software architecture and provide implementation guidance",
        backstory="""You are a senior software developer with expertise in creating 
        scalable applications and providing clear implementation guidance.""",
        llm=llm,
        verbose=True,
        max_iter=2,
        max_execution_time=60
    )
    
    # Get project description
    if len(sys.argv) > 1:
        project_description = " ".join(sys.argv[1:])
    else:
        project_description = input("Enter your project description: ")
    
    print(f"📝 Project: {project_description}")
    print("=" * 50)
    
    # Create analysis task
    analysis_task = Task(
        description=f"""
        Analyze the following project requirements: {project_description}
        
        Provide:
        1. Project overview and objectives
        2. Key features and functionality
        3. Technical requirements
        4. Recommended technology stack
        5. Basic project structure
        
        Keep the analysis concise but comprehensive.
        """,
        expected_output="""
        A structured project analysis document with:
        - Project overview
        - Key features list
        - Technical requirements
        - Technology recommendations
        - Project structure outline
        """,
        agent=business_analyst
    )
    
    # Create development task
    development_task = Task(
        description=f"""
        Based on the project analysis, create a development plan for: {project_description}
        
        Provide:
        1. System architecture overview
        2. Database design recommendations
        3. API structure and endpoints
        4. Implementation steps
        5. Code examples for key components
        
        Focus on practical, implementable solutions.
        """,
        expected_output="""
        A development plan including:
        - System architecture diagram (text-based)
        - Database schema recommendations
        - API endpoint specifications
        - Step-by-step implementation guide
        - Sample code snippets
        """,
        agent=developer
    )
    
    # Create crew
    crew = Crew(
        agents=[business_analyst, developer],
        tasks=[analysis_task, development_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute crew
    print("🚀 Starting analysis and development planning...")
    result = crew.kickoff()
    
    # Save results
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "quick_demo_result.md", "w") as f:
        f.write(f"# AI Development Team - Quick Demo Results\n\n")
        f.write(f"**Project:** {project_description}\n\n")
        f.write(f"## Results\n\n{result}\n")
    
    print("=" * 50)
    print("✅ Demo completed!")
    print(f"📁 Results saved to: {output_dir / 'quick_demo_result.md'}")
    print("=" * 50)
    
    return result

if __name__ == "__main__":
    try:
        create_simple_demo()
    except KeyboardInterrupt:
        print("\n❌ Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        sys.exit(1)