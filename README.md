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
* **Language:** Python 3.12+
* **Framework:** Django 6.0.x
* **Database:** SQLite (dev/local)
* **Testing:** Pytest 9.0.x with Pytest-Django
* **Environment:** Django-environ (Configuration via .env)

## Quick Start
### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Eveline-projects/Lopa.git
cd Lopa

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt
```

### 2. Database configuration and startup
```bash
python manage.py migrate 

python manage.py runserver
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
The project prioritizes reliability, which is why every engine function is tested using pytest.
```bash
# Run all tests
pytest

# Run in detailed mode
pytest -v
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

## Modular Architecture
The project uses the apps/ directory structure to separate business logic from the main configuration (config/). This approach (known as “Separation of Concerns”) makes it easier to manage a large number of Django applications, improves code readability, and allows for easier addition of new modules, such as the upcoming Blog or the Flashcards system.
```text
Lopa/
├── apps/
│   ├── engine/
│   │   ├── migrations/
│   │   ├── models.py          # Modele Submission, Result
│   │   ├── apps.py
│   │   └── ...
│   ├── problems/
│       ├── migrations/        # Here are the files 0001_initial and 0002_testcase
│       ├── models.py          # Problem and Test Case Models
│       ├── apps.py
│       └── ...      
├── config/                      # Main project settings folder
│   ├── settings.py            # Configuration of databases, installed applications, and pytest
│   ├── urls.py
│   └── wsgi.py 
├── static/
│    ├── css/
│    └── js/
├── tests/                     # Folder containing automated tests
│   ├── test_engine.py         # Tests for Submission
│   └── test_problems.py       # Tests for Problem and TestCase
├── conftest.py                # Pytest fixtures (problem, submission, test_case, result)
├── manage.py                  # Django management script
├── pytest.ini                 # Pytest configuration
└── requirements.txt           # List of dependencies (Django, pytest-django, etc.)
```
