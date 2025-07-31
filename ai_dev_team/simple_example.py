#!/usr/bin/env python3
"""
Simple Example - AI Development Team
Demonstrates the basic functionality without complex workflows
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task
from crewai.llm import LLM

# Load environment variables
load_dotenv()

def simple_analysis_example():
    """Simple example with just one agent doing analysis"""
    
    print("🤖 AI Development Team - Simple Analysis Example")
    print("=" * 60)
    
    # Initialize LLM
    llm = LLM(
        model=f"ollama/{os.getenv('DEFAULT_LLM_MODEL', 'llama3.2:3b')}",
        base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    )
    
    # Create analyst agent
    analyst = Agent(
        role="Technical Analyst",
        goal="Analyze project requirements and provide technical recommendations",
        backstory="You are a technical analyst with expertise in software architecture and development planning.",
        llm=llm,
        verbose=True,
        max_iter=1,
        max_execution_time=30
    )
    
    # Project description
    project = "Create a REST API for a todo application with CRUD operations"
    
    # Create analysis task
    task = Task(
        description=f"""
        Analyze this project: {project}
        
        Provide a brief analysis including:
        1. Project overview
        2. Key technical requirements
        3. Recommended technology stack
        4. Basic implementation approach
        
        Keep it concise and practical.
        """,
        expected_output="A structured technical analysis with recommendations",
        agent=analyst
    )
    
    print(f"📝 Analyzing: {project}")
    print("=" * 60)
    
    # Execute task using agent
    result = analyst.execute_task(task)
    
    print("=" * 60)
    print("✅ Analysis completed!")
    print("=" * 60)
    print("📋 RESULT:")
    print(result)
    print("=" * 60)
    
    # Save result
    with open("output/simple_analysis.md", "w") as f:
        f.write(f"# Technical Analysis\n\n**Project:** {project}\n\n## Analysis Result\n\n{result}\n")
    
    print("📁 Result saved to: output/simple_analysis.md")
    
    return result

if __name__ == "__main__":
    try:
        simple_analysis_example()
    except Exception as e:
        print(f"❌ Error: {str(e)}")