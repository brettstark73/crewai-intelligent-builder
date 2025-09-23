# CrewAI Game Studio

An intelligent AI-powered game development studio using CrewAI framework. This system analyzes project requirements and generates appropriate development tasks for creating working games.

## 🎮 What Makes This Different

Unlike generic development frameworks, this system:

1. **Analyzes Your Project** - Understands if you're building a game vs web app vs mobile app
2. **Generates Custom Tasks** - Creates game-specific tasks (canvas, game loop, collision detection) instead of web app tasks (databases, APIs)
3. **Handles Rate Limits** - Chunks large requests to stay under OpenAI's token limits
4. **Creates Working Games** - Focuses on functional, playable results

## 🧠 The Intelligent System

### Task Designer Agent
- Analyzes project requirements
- Determines project type (game, web app, etc.)
- Generates appropriate development tasks
- Creates implementation guides

### Intelligent Crew Runner
- Executes custom tasks with rate limit handling
- Uses game-specific development approaches
- Produces working, testable code

## 🚀 Quick Start

1. **Set Up Environment**
   ```bash
   # Make sure you have your OpenAI API key
   export OPENAI_API_KEY="your-key-here"
   export OPENAI_MODEL_NAME="gpt-4o-mini"
   ```

2. **Run Game Generation**
   ```bash
   python intelligent_crew_runner.py
   ```

3. **Find Your Game**
   ```
   /Users/brettstark/Projects/space-invaders-game/
   ```

## 🎯 Current Focus: Space Invaders

The system is currently configured to generate a space invaders arcade game with:
- HTML5 Canvas rendering
- Player movement and shooting
- Enemy waves and collision detection
- Scoring system
- Working game controls

## 🔧 Components

- `task_designer_agent.py` - Analyzes projects and creates custom tasks
- `intelligent_crew_runner.py` - Main runner with intelligent task generation
- `agents.py` - Development team agents
- `tasks.py` - Generic task templates (mostly unused now)

## 📊 Why This Approach Works

**Problem:** Generic CrewAI setups use web app tasks for everything, resulting in broken games

**Solution:** Analyze the project first, then generate appropriate tasks

**Result:** Working games instead of code that looks good but doesn't function

---

*Generated with intelligent task design - no more broken games!*