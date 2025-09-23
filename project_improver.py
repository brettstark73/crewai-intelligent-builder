#!/usr/bin/env python3
"""
Project Improver - Takes existing projects and improvement requests
Uses the intelligent system to enhance generated projects
"""

import sys
import os
from task_designer_agent import TaskDesignerAgent, analyze_and_design_tasks
from intelligent_crew_runner import IntelligentCrewRunner

def improve_project(project_path, improvement_request, target_audience="general users"):
    """Improve an existing project based on user feedback"""

    print("🔧 PROJECT IMPROVEMENT SYSTEM")
    print("=" * 50)
    print(f"📁 Project: {project_path}")
    print(f"🎯 Improvements: {improvement_request}")
    print()

    # Read existing project files
    project_files = {}
    if os.path.exists(project_path):
        for file in os.listdir(project_path):
            if file.endswith(('.html', '.js', '.css')):
                file_path = os.path.join(project_path, file)
                with open(file_path, 'r') as f:
                    project_files[file] = f.read()

    # Create improvement-focused project description
    project_context = f"""
    EXISTING PROJECT IMPROVEMENT:

    Current Project Files: {list(project_files.keys())}

    Improvement Request: {improvement_request}

    Instructions: Analyze the existing code and implement the requested improvements.
    Focus on enhancing the existing functionality rather than rebuilding from scratch.
    Maintain compatibility with the current project structure.
    """

    # Use intelligent system for improvements
    runner = IntelligentCrewRunner(max_tokens_per_chunk=180000, delay_between_chunks=65)

    results = runner.run_intelligent_crew(
        project_idea=project_context,
        target_audience=target_audience,
        timeline="3-5 days"
    )

    return results

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("🔧 PROJECT IMPROVER")
        print("=" * 30)
        print("Usage: python project_improver.py <project_path> \"<improvement_request>\"")
        print()
        print("Examples:")
        print('  python project_improver.py "/Users/brettstark/Projects/space-invaders-game" "add sprite graphics and sound effects"')
        print('  python project_improver.py "/Users/brettstark/Projects/todo-app" "add drag and drop functionality"')
        print('  python project_improver.py "/Users/brettstark/Projects/calculator" "add scientific calculator functions"')
        sys.exit(1)

    project_path = sys.argv[1]
    improvement_request = sys.argv[2]
    target_audience = sys.argv[3] if len(sys.argv) > 3 else "general users"

    if not os.path.exists(project_path):
        print(f"❌ Project path not found: {project_path}")
        sys.exit(1)

    results = improve_project(project_path, improvement_request, target_audience)
    print("\n🎉 PROJECT IMPROVEMENT COMPLETE!")