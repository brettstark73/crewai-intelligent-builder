#!/usr/bin/env python3
"""
Task Designer Agent - Analyzes project requirements and generates appropriate tasks
This is the missing piece that determines WHAT needs to be built before HOW to build it
"""

from crewai import Agent, Task
from langchain_openai import ChatOpenAI
import os
import json
from typing import Dict, List, Any

class TaskDesignerAgent:
    """Analyzes projects and generates appropriate development tasks"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
            temperature=0.1  # Very low for consistent analysis
        )

        self.analyzer_agent = Agent(
            role='Senior Technical Project Analyzer',
            goal='Analyze project requirements and determine the optimal development approach and task structure',
            backstory="""You are a senior technical analyst with 15+ years experience across
            web development, game development, mobile apps, AI/ML projects, and enterprise software.
            You excel at quickly understanding project requirements and determining:
            - What type of project this is (game, web app, mobile app, AI tool, etc.)
            - What technology stack is most appropriate
            - What development phases and tasks are needed
            - What potential challenges and requirements exist

            SPECIAL EXPERTISE: You understand common failure patterns and their prevention:

            GAMES: Memory leaks from uncleaned intervals/requestAnimationFrame, audio lifecycle issues,
            input event cleanup, mobile browser quirks, canvas rendering problems, game state corruption

            WEB APPS: Form validation bypasses, authentication flow breaks, API integration failures,
            XSS vulnerabilities, responsive design issues, accessibility problems

            MOBILE: Touch event conflicts, orientation handling, device integration failures,
            platform-specific behaviors, performance on lower-end devices

            AI TOOLS: Model loading failures, rate limiting issues, input/output validation problems,
            fallback mechanism absence, user experience during processing delays

            You create detailed project analysis that guides the entire development process.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def analyze_project(self, project_idea: str, target_audience: str = "general users", timeline: str = "8 weeks") -> Dict:
        """Analyze project and determine development approach"""

        analysis_task = Task(
            description=f"""Analyze this project idea and create a comprehensive project analysis:

            PROJECT: {project_idea}
            TARGET AUDIENCE: {target_audience}
            TIMELINE: {timeline}

            Provide a detailed analysis covering:

            1. PROJECT TYPE CLASSIFICATION:
               - Is this a game, web application, mobile app, AI tool, or other?
               - What are the core functional requirements?
               - What are the technical requirements?

            2. TECHNOLOGY STACK RECOMMENDATION:
               - What technologies are most appropriate?
               - Front-end requirements (HTML5 Canvas, React, Unity, etc.)
               - Back-end requirements (if any)
               - Database requirements (if any)
               - Third-party services needed

            3. DEVELOPMENT APPROACH:
               - Should this be built as a single HTML file, multi-file project, or complex application?
               - What are the main development phases?
               - What are the critical features vs nice-to-have features?

            4. SPECIFIC REQUIREMENTS:
               - For games: Game loop, rendering, input handling, collision detection, scoring, levels
               - For web apps: Database design, API endpoints, authentication, UI components
               - For mobile apps: Platform requirements, native features, offline capability
               - For AI tools: Model requirements, data processing, user interface

            5. RECOMMENDED TASK BREAKDOWN:
               - What specific development tasks should be created?
               - What order should tasks be completed in?
               - What are the deliverables for each task?
               - What testing and validation is needed?

            6. POTENTIAL CHALLENGES:
               - What technical challenges might arise?
               - What are the common pitfalls for this type of project?
               - What should be prioritized to ensure a working result?

            Format your response as a detailed analysis that will guide task creation.""",
            agent=self.analyzer_agent,
            expected_output="Comprehensive project analysis with technology recommendations, development approach, and detailed task breakdown recommendations"
        )

        result = analysis_task.execute_sync()
        return {
            'analysis': result,
            'project_idea': project_idea,
            'target_audience': target_audience,
            'timeline': timeline
        }

    def generate_custom_tasks(self, analysis_result: Dict) -> List[Dict]:
        """Generate custom tasks based on project analysis"""

        task_generation = Task(
            description=f"""Based on this project analysis, create specific development tasks:

            ANALYSIS RESULTS:
            {analysis_result['analysis']}

            PROJECT: {analysis_result['project_idea']}

            Create a detailed list of development tasks that will result in a WORKING implementation.
            Each task should be:
            - Specific and actionable
            - Focused on creating working code/features
            - Appropriate for the project type identified in the analysis
            - Designed to produce testable deliverables

            For each task, provide:
            1. TASK NAME: Clear, descriptive name
            2. DESCRIPTION: Detailed description of what needs to be built
            3. EXPECTED OUTPUT: Specific deliverable (working file, component, feature)
            4. SUCCESS CRITERIA: How to verify the task is complete and working
            5. DEPENDENCIES: What other tasks must be completed first
            6. ESTIMATED COMPLEXITY: Simple/Medium/Complex

            CRITICAL TESTING PATTERNS BY PROJECT TYPE:

            FOR GAMES - Always include these validation tasks:
            • "Game State Management Testing": Pause/resume/restart functionality, memory leak prevention (cleanup intervals/requestAnimationFrame), browser tab focus/blur handling
            • "Audio System Validation": Sound lifecycle testing, mobile browser compatibility, audioContext.resume() on ALL interactions, multiple sound overlap handling
            • "Input System Reliability": Keyboard cleanup, simultaneous key presses, mobile touch, prevent browser defaults (arrow keys scrolling)
            • "Performance & Rendering": Canvas clearing, animation cleanup, mobile device performance, rendering degradation over time
            • "Cross-Browser Game Testing": Different browsers, mobile devices, full-screen functionality

            FOR WEB APPS/SaaS - Always include these validation tasks:
            • "Form & Data Integrity Testing": Client+server validation, CRUD operations, data persistence, XSS prevention, input sanitization
            • "Authentication Flow Testing": Login/logout completeness, session timeout, protected routes, CSRF protection
            • "API Integration Robustness": Network failure handling, rate limiting, loading states, timeout handling, error user feedback
            • "Responsive & Accessibility Testing": Mobile/tablet/desktop layouts, keyboard navigation, screen reader compatibility, loading indicators
            • "Security Validation": Input sanitization, authentication bypass attempts, data exposure prevention

            FOR MOBILE APPS - Always include these validation tasks:
            • "Touch & Gesture Testing": Tap/swipe/pinch/long press, orientation changes, screen sizes, touch conflicts with browser gestures
            • "Device Integration Testing": Camera/GPS/sensors, offline functionality, app lifecycle, platform-specific behaviors
            • "Mobile Performance Testing": Battery usage, lower-end device performance, network connectivity changes
            • "Platform Compatibility": iOS Safari quirks, Android Chrome differences, PWA functionality

            FOR AI TOOLS - Always include these validation tasks:
            • "AI Integration Reliability": API failure handling, fallback mechanisms, rate limiting, quota management
            • "Data Processing Pipeline": Input validation, preprocessing, output formatting, large input handling, error recovery
            • "User Experience Flow": Real-time vs batch processing, progress indicators, user feedback during processing
            • "AI Service Testing": Model loading, initialization, versioning, timeout handling

            UNIVERSAL QUALITY CHECKLIST - Always include these for ALL project types:
            • "Cross-Browser Compatibility Testing": Chrome, Firefox, Safari, Edge testing
            • "Performance Optimization": Loading speed, memory usage, responsiveness under load
            • "Error Handling & User Feedback": Graceful error handling, informative error messages, loading states
            • "Code Quality & Maintainability": Clean code structure, commented critical sections, consistent patterns
            • "Final Integration Testing": End-to-end user workflows, edge case handling, production readiness

            Ensure tasks will result in a WORKING, TESTABLE implementation that matches the project requirements.

            Format as a JSON array of task objects.""",
            agent=self.analyzer_agent,
            expected_output="JSON array of custom development tasks specific to the project type and requirements"
        )

        result = task_generation.execute_sync()

        try:
            # Try to parse as JSON
            if hasattr(result, 'raw'):
                task_data = result.raw
            else:
                task_data = str(result)

            # Extract JSON from the response
            import re
            json_match = re.search(r'\[.*\]', task_data, re.DOTALL)
            if json_match:
                tasks = json.loads(json_match.group())
                return tasks
            else:
                # Fallback: parse the text response
                return self._parse_text_tasks(task_data)
        except Exception as e:
            print(f"Warning: Could not parse JSON tasks: {e}")
            return self._parse_text_tasks(str(result))

    def _parse_text_tasks(self, text: str) -> List[Dict]:
        """Fallback method to parse tasks from text response"""

        # This is a simplified parser - in production you'd want more robust parsing
        tasks = []
        lines = text.split('\n')
        current_task = {}

        for line in lines:
            line = line.strip()
            if 'TASK NAME:' in line:
                if current_task:
                    tasks.append(current_task)
                current_task = {'name': line.split('TASK NAME:')[1].strip()}
            elif 'DESCRIPTION:' in line:
                current_task['description'] = line.split('DESCRIPTION:')[1].strip()
            elif 'EXPECTED OUTPUT:' in line:
                current_task['expected_output'] = line.split('EXPECTED OUTPUT:')[1].strip()
            elif 'SUCCESS CRITERIA:' in line:
                current_task['success_criteria'] = line.split('SUCCESS CRITERIA:')[1].strip()

        if current_task:
            tasks.append(current_task)

        return tasks if tasks else self._generate_fallback_tasks()

    def _generate_fallback_tasks(self) -> List[Dict]:
        """Generate basic fallback tasks if parsing fails"""
        return [
            {
                "name": "Project Setup",
                "description": "Set up basic project structure and files",
                "expected_output": "Working project foundation",
                "success_criteria": "Files can be opened and basic structure exists"
            },
            {
                "name": "Core Implementation",
                "description": "Implement main functionality",
                "expected_output": "Working core features",
                "success_criteria": "Main features function as expected"
            },
            {
                "name": "Testing and Polish",
                "description": "Test functionality and add finishing touches",
                "expected_output": "Polished, working application",
                "success_criteria": "Application works without errors"
            }
        ]

    def create_project_guide(self, analysis_result: Dict, custom_tasks: List[Dict]) -> str:
        """Create a comprehensive project development guide"""

        guide = f"""# PROJECT DEVELOPMENT GUIDE
Generated: {analysis_result.get('timestamp', 'Unknown')}

## PROJECT OVERVIEW
**Idea:** {analysis_result['project_idea']}
**Target Audience:** {analysis_result['target_audience']}
**Timeline:** {analysis_result['timeline']}

## ANALYSIS RESULTS
{analysis_result['analysis']}

## DEVELOPMENT TASKS
Total Tasks: {len(custom_tasks)}

"""

        for i, task in enumerate(custom_tasks, 1):
            guide += f"""### Task {i}: {task.get('name', 'Unnamed Task')}

**Description:** {task.get('description', 'No description provided')}

**Expected Output:** {task.get('expected_output', 'No output specified')}

**Success Criteria:** {task.get('success_criteria', 'No criteria specified')}

**Dependencies:** {task.get('dependencies', 'None specified')}

**Complexity:** {task.get('estimated_complexity', 'Unknown')}

---

"""

        guide += """## IMPLEMENTATION NOTES

1. **Follow the task order** - dependencies matter
2. **Test each task** before moving to the next
3. **Focus on working code** over perfect code
4. **Validate success criteria** for each task
5. **Document any deviations** from the plan

## SUCCESS METRICS

- [ ] All tasks completed successfully
- [ ] Final deliverable works as intended
- [ ] Success criteria met for each task
- [ ] Project meets original requirements

"""

        return guide

def analyze_and_design_tasks(project_idea: str, target_audience: str = "general users", timeline: str = "8 weeks") -> Dict:
    """Main function to analyze project and generate custom tasks"""

    print("🔍 ANALYZING PROJECT REQUIREMENTS...")
    print("=" * 50)

    designer = TaskDesignerAgent()

    # Step 1: Analyze the project
    print("📊 Running project analysis...")
    analysis = designer.analyze_project(project_idea, target_audience, timeline)

    # Step 2: Generate custom tasks
    print("🛠️ Generating custom development tasks...")
    custom_tasks = designer.generate_custom_tasks(analysis)

    # Step 3: Create project guide
    print("📚 Creating project development guide...")
    guide = designer.create_project_guide(analysis, custom_tasks)

    result = {
        'analysis': analysis,
        'custom_tasks': custom_tasks,
        'project_guide': guide,
        'project_type': 'Detected from analysis',
        'recommended_approach': 'Custom task-driven development'
    }

    print(f"✅ Analysis complete! Generated {len(custom_tasks)} custom tasks")
    print("🎯 Ready for implementation with project-specific tasks")

    return result

if __name__ == "__main__":
    # Test with space invaders
    result = analyze_and_design_tasks(
        project_idea="space invaders arcade game with HTML5 canvas",
        target_audience="casual gamers",
        timeline="2 weeks"
    )

    print("\n" + "="*60)
    print("PROJECT ANALYSIS COMPLETE")
    print("="*60)
    print(f"Generated {len(result['custom_tasks'])} custom tasks")
    print("\nFirst task:")
    if result['custom_tasks']:
        first_task = result['custom_tasks'][0]
        print(f"Name: {first_task.get('name', 'Unnamed')}")
        print(f"Description: {first_task.get('description', 'No description')[:100]}...")