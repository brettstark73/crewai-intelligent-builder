# CrewAI Intelligent Builder

An intelligent AI-powered development system using CrewAI framework. This system analyzes project requirements and generates appropriate development tasks for creating working applications - games, web apps, tools, and more.

## 🧠 What Makes This Different

Unlike generic development frameworks, this system:

1. **Analyzes Your Project** - Understands if you're building a game vs web app vs mobile app vs tool
2. **Generates Custom Tasks** - Creates project-specific tasks (games: canvas/collision detection, web apps: components/APIs, tools: functionality/UI)
3. **Handles Rate Limits** - Chunks large requests to stay under OpenAI's token limits
4. **Creates Working Applications** - Focuses on functional, testable results

## 🧠 The Intelligent System

### Task Designer Agent
- Analyzes project requirements
- Determines project type (game, web app, etc.)
- Generates appropriate development tasks
- Creates implementation guides

### Intelligent Crew Runner
- Executes custom tasks with rate limit handling
- Uses project-specific development approaches
- Produces working, testable applications

## 🚀 Quick Start

1. **Set Up Environment**
   ```bash
   # Make sure you have your OpenAI API key
   export OPENAI_API_KEY="your-key-here"
   export OPENAI_MODEL_NAME="gpt-4o-mini"
   ```

2. **Build Any Application**
   ```bash
   # Build a game
   python intelligent_crew_runner.py "tetris puzzle game"

   # Build a web app
   python intelligent_crew_runner.py "todo list with user accounts"

   # Build a tool
   python intelligent_crew_runner.py "password generator with strength meter"
   ```

3. **Improve Existing Projects**
   ```bash
   python project_improver.py "/path/to/project" "add dark mode and animations"
   ```

## 🎯 Example Applications Built

The system successfully creates working applications like:
- **Games**: Space Invaders, Frogger, Tetris, Snake
- **Web Apps**: Todo lists, calculators, dashboards
- **Tools**: Generators, converters, utilities
- **Interactive Apps**: Drawing tools, simulators

## 🔧 Components

- `task_designer_agent.py` - Analyzes projects and creates custom tasks
- `intelligent_crew_runner.py` - Main runner with intelligent task generation
- `agents.py` - Development team agents
- `tasks.py` - Generic task templates (mostly unused now)

## 📊 Why This Approach Works

**Problem:** Generic CrewAI setups use one-size-fits-all tasks, resulting in broken applications

**Solution:** Analyze the project first, then generate appropriate tasks for that specific type of application

**Result:** Working, functional applications instead of code that looks good but doesn't work

---

*Intelligent development system - build anything that actually works!*