#!/usr/bin/env python3
"""
Intelligent CrewAI Runner - Uses Task Designer Agent to create project-specific tasks
Replaces the generic hard-coded tasks with dynamically generated ones
"""

import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from crewai import Crew, Agent, Task
from task_designer_agent import TaskDesignerAgent, analyze_and_design_tasks

class IntelligentCrewRunner:
    """Runs CrewAI with dynamically generated, project-specific tasks"""

    def __init__(self, max_tokens_per_chunk=180000, delay_between_chunks=65):
        self.max_tokens_per_chunk = max_tokens_per_chunk
        self.delay_between_chunks = delay_between_chunks
        self.task_designer = TaskDesignerAgent()

    def run_intelligent_crew(self, project_idea: str, target_audience: str = "general users", timeline: str = "4 weeks") -> Dict:
        """Run crew with intelligent task generation"""

        print("🧠 INTELLIGENT CREW EXECUTION")
        print("=" * 60)
        print(f"📊 Project: {project_idea}")
        print(f"👥 Audience: {target_audience}")
        print(f"⏰ Timeline: {timeline}")
        print()

        # Step 1: Analyze project and generate custom tasks
        print("🔍 PHASE 1: PROJECT ANALYSIS & TASK DESIGN")
        print("-" * 40)

        analysis_result = analyze_and_design_tasks(project_idea, target_audience, timeline)
        custom_tasks = analysis_result['custom_tasks']

        print(f"✅ Generated {len(custom_tasks)} project-specific tasks")
        print()

        # Step 2: Create a simple agent for task execution
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
            temperature=0.3
        )

        executor_agent = Agent(
            role='Expert Full Stack Developer & Game Developer',
            goal='Execute development tasks with precision, creating working, testable code',
            backstory="""You are an expert developer with deep experience in:
            - HTML5 Canvas game development
            - JavaScript game programming
            - Web application development
            - Frontend and backend technologies
            - Creating working, polished applications

            You focus on writing clean, functional code that actually works when tested.
            You pay attention to details like event handling, game loops, collision detection,
            and user interaction. You always deliver working implementations.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        # Step 3: Execute custom tasks in chunks
        print("🛠️ PHASE 2: CHUNKED TASK EXECUTION")
        print("-" * 40)

        results = {}

        for i, task_config in enumerate(custom_tasks, 1):
            print(f"🎯 TASK {i}/{len(custom_tasks)}: {task_config.get('name', 'Unnamed Task')}")

            # Estimate tokens for this task
            task_description = task_config.get('description', '')
            estimated_tokens = len(task_description) * 4  # Rough estimation
            print(f"📊 Estimated tokens: {estimated_tokens:,}")

            if estimated_tokens > self.max_tokens_per_chunk:
                print("⚠️ Large task - may need chunking...")

            try:
                # Create CrewAI Task from our custom task config
                crew_task = Task(
                    description=f"""
                    TASK: {task_config.get('name', 'Development Task')}

                    DESCRIPTION: {task_config.get('description', 'Complete this development task')}

                    EXPECTED OUTPUT: {task_config.get('expected_output', 'Working implementation')}

                    SUCCESS CRITERIA: {task_config.get('success_criteria', 'Code functions without errors')}

                    PROJECT CONTEXT: {project_idea}

                    IMPORTANT: Create working, testable code. Focus on functionality over perfection.
                    If this is a game, ensure the game loop, rendering, and interaction work properly.
                    If this is a web app, ensure the UI and functionality work as expected.

                    Provide complete, runnable code that can be tested immediately.
                    """,
                    agent=executor_agent,
                    expected_output=task_config.get('expected_output', 'Working implementation')
                )

                # Execute the task
                start_time = time.time()
                print(f"⚡ Executing task...")

                result = crew_task.execute_sync()
                execution_time = time.time() - start_time

                results[f"task_{i}_{task_config.get('name', 'unnamed').replace(' ', '_').lower()}"] = {
                    'task_config': task_config,
                    'result': result,
                    'execution_time': execution_time,
                    'estimated_tokens': estimated_tokens,
                    'timestamp': datetime.now().isoformat()
                }

                print(f"✅ Completed in {execution_time:.1f}s")

                # Wait between tasks (except for last one)
                if i < len(custom_tasks):
                    print(f"⏳ Waiting {self.delay_between_chunks}s before next task...")
                    time.sleep(self.delay_between_chunks)

            except Exception as e:
                error_msg = str(e)
                print(f"❌ Task failed: {error_msg}")

                results[f"task_{i}_failed"] = {
                    'task_config': task_config,
                    'error': error_msg,
                    'timestamp': datetime.now().isoformat()
                }

                if "RateLimitError" in error_msg:
                    print("🔄 Rate limit detected - increasing delay...")
                    extra_delay = 120
                    print(f"⏳ Waiting additional {extra_delay}s...")
                    time.sleep(extra_delay)

            print()

        # Step 4: Combine and finalize results
        print("🎉 PHASE 3: RESULT COMPILATION")
        print("-" * 40)

        successful_tasks = [k for k, v in results.items() if 'error' not in v]
        failed_tasks = [k for k, v in results.items() if 'error' in v]

        print(f"✅ Successful tasks: {len(successful_tasks)}")
        print(f"❌ Failed tasks: {len(failed_tasks)}")

        if successful_tasks:
            combined_result = self.combine_intelligent_results(results, analysis_result)
            results['combined'] = combined_result
            results['analysis'] = analysis_result
            print("📄 Combined final output generated")
        else:
            print("⚠️ No successful tasks to combine")

        return results

    def combine_intelligent_results(self, task_results: Dict, analysis_result: Dict) -> str:
        """Combine task results with analysis information"""

        combined = []
        combined.append("# INTELLIGENT PROJECT DEVELOPMENT RESULTS")
        combined.append(f"Generated: {datetime.now().isoformat()}")
        combined.append("")
        combined.append("## PROJECT ANALYSIS")
        combined.append(str(analysis_result.get('analysis', {}).get('analysis', 'No analysis available')))
        combined.append("")
        combined.append("## TASK EXECUTION RESULTS")
        combined.append("")

        for task_name, task_data in task_results.items():
            if task_name in ['combined', 'analysis']:
                continue

            combined.append(f"### {task_name.replace('_', ' ').title()}")

            if 'error' in task_data:
                combined.append(f"**Status:** Failed")
                combined.append(f"**Error:** {task_data['error']}")
            else:
                combined.append(f"**Status:** Success")
                combined.append(f"**Execution Time:** {task_data.get('execution_time', 0):.1f}s")

                result = task_data.get('result', '')
                if hasattr(result, 'raw'):
                    combined.append(str(result.raw))
                else:
                    combined.append(str(result))

            combined.append("")

        combined.append("## IMPLEMENTATION GUIDE")
        combined.append(analysis_result.get('project_guide', 'No guide available'))

        return "\n".join(combined)

def run_space_invaders():
    """Run space invaders generation with intelligent task design"""

    runner = IntelligentCrewRunner(
        max_tokens_per_chunk=180000,
        delay_between_chunks=65
    )

    project_idea = "space invaders arcade game with HTML5 canvas, player movement, shooting, enemy waves, collision detection, and scoring"

    print("🚀 Starting space invaders generation...")
    results = runner.run_intelligent_crew(
        project_idea=project_idea,
        target_audience="casual gamers who want a quick, fun arcade experience",
        timeline="1 week"
    )

    # Save results
    output_dir = "/Users/brettstark/Projects/space-invaders-game"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save detailed results
    output_file = f"{output_dir}/game_output_{timestamp}.json"
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"💾 Detailed results saved to: {output_file}")

    # Save combined markdown
    if 'combined' in results:
        combined_file = f"{output_dir}/game_output_{timestamp}_combined.md"
        with open(combined_file, 'w') as f:
            f.write(results['combined'])
        print(f"📄 Combined output: {combined_file}")

    # Save project guide
    if 'analysis' in results and 'project_guide' in results['analysis']:
        guide_file = f"{output_dir}/project_guide_{timestamp}.md"
        with open(guide_file, 'w') as f:
            f.write(results['analysis']['project_guide'])
        print(f"📚 Project guide: {guide_file}")

    return results

if __name__ == "__main__":
    result = run_space_invaders()
    print("\n🎉 SPACE INVADERS GENERATION COMPLETE!")

    if 'combined' in result:
        print("✅ Successfully generated project with custom tasks")
    else:
        print("⚠️ Generation completed with some issues - check output files")