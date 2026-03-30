# 🐤 Lopa
Algorithms explained in simple terms. Manage tasks, test code, and learn data structures without unnecessary complexity.

## About the project:
Lopa (from the Polish "łopatologicznie" meaning straightforward or down-to-earth) is an educational platform built with Python and Django. It’s designed for those who—like me—want to truly grasp how algorithms work. It’s more than just a dry code-grading system; it’s a space for learning through practice, visualization, and a guided hint system.

### Why Lopa?
- Understanding the mechanisms: Focusing on the underlying principles of how algorithms work, which allows for intuitive solution design rather than simply replicating existing patterns.
- Educational Support: A module featuring flashcards and articles that explain the theory “in real time” while you work through exercises, thereby breaking down barriers to tackling more challenging topics.
- Balanced Gamification: The point system encourages players to solve problems on their own while offering access to hints in exchange for earned points. This allows for a smooth learning experience without getting stuck.

### Key Features:
- Core Execution Engine: Automatic verification of solutions with time tracking and isolated environments.
- Knowledge Base (Coming Soon): A blog with step-by-step explanations of algorithms and data structures.
- Interactive Flashcards (Coming Soon): A quick review of the theory available right as you work through the problem.
- Hint System (Coming Soon): You'll be able to purchase hints for tasks using points earned in the system.
- Error reporting: Clear information about `Runtime Error`,  `Time Limit Exceeded` or `Wrong Answer`.

### 🛠 Technologies:
* **Language:** Python 3.13+ (via `uv`)
* **Framework:** Django 6.0.x
* **Package Manager:** uv (Extremely fast Python package installer and resolver)
* **Database:** SQLite (dev/local)
* **Testing:** Pytest 9.0.x with Pytest-Django
* **Configuration:** `pyproject.toml` & `uv.lock` (Modern dependency management)
* **Environment:** Django-environ (Configuration via `.env`)

## Quick Start
### 1. Installation
Lopa uses uv for lightning-fast dependency management. Install uv if you haven't already.
```bash
# Clone the repository
git clone https://github.com/Eveline-projects/Lopa.git
cd Lopa

# Setup environment and install dependencies automatically
uv sync
```

### 2. Database configuration and startup
You don't need to manually activate the virtual environment; uv run handles it for you.
```bash
# Run migrations
uv run manage.py migrate 

# Start the development server
uv run manage.py runserver
```

The app is available at: `http://127.0.0.1:8000/`

## Data Architecture:
The system is based on the logical interconnection of four pillars:

| Model | Description                                                                        |
| :--- |-----------------------------------------------------------------------------| 
| **Problem** | Challenge definition: includes the task description, requirements specification, and assigned difficulty level.                            |
| **TestCase** | Datasets: input vs. expected output.               |
| **Submission** | The user's ID and their current status in the queue.                            |
| **Result** | Detailed execution report: execution time and error messages for a single test. |

## Automated Testing
The project prioritizes reliability, using uv to orchestrate tests using pytest.
```bash
# Run all tests
uv run pytest

# Run in detailed mode
uv run pytest -v
```
## Test Structure:
- `tests/test_problems.py` – model and relationship validation.
- `tests/test_engine.py` – code verification tests.
- `conftest.py` – common test data (fixtures).

## Project Roadmap:
- [x] Core Execution Engine
- [ ] Blog Module (articles explained in simple terms)
- [ ] Flashcard system linked to assignments
- [ ] Point system and user rankings
- [ ] Hints system

## Project Documentation
- [Architecture Details](./Architecture.md)