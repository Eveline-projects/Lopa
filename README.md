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
* **API Layer:** Django Ninja
* **Schemas / Validation:** Django Ninja Schema (Pydantic-based)
* **Package Manager:** uv (Extremely fast Python package installer and resolver)
* **Database:** SQLite (dev/local)
* **Testing:** Pytest 9.0.x with Pytest-Django & Playwright (E2E)
* **Reporting** pytest-html
* **Configuration:** `pyproject.toml` & `uv.lock` (Modern dependency management)
* **Environment:** Django-environ (Configuration via `.env`)
* **Code Quality:** Ruff

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
Lopa uses **Django** for the web application and **Django Ninja** for the API layer.
```bash
# Run migrations
uv run manage.py migrate 

# Start the development server
uv run manage.py runserver
```

The app is available at: `http://127.0.0.1:8000/`
API documentation will be available at: `http://127.0.0.1:8000/api/docs`

### 3. Populating the Database (Seeding)
To quickly get started with sample data (e.g., Two Sum, Palindrome tasks), use the custom management command. This will load problems from a JSON file using the service layer to ensure data integrity.
```bash
# Load initial algorithm problems
uv run manage.py load_problems initial_problems.json
```
### 4. Frontend & User Interface
Lopa uses Django Templates with Tailwind CSS (via CDN for development) to provide a clean and responsive UI. No separate frontend build steps (like npm/yarn) are required for the basic setup.

View Problems: Navigate to http://127.0.0.1:8000/problems/ to see the list of loaded tasks.

Admin Panel: Access the database directly at http://127.0.0.1:8000/admin/ (requires creating a superuser).
```bash
# Create a superuser to access the admin panel
uv run manage.py createsuperuser
```

## Data Architecture:
The system is based on the logical interconnection of four pillars:

| Model | Description                                                                        |
| :--- |-----------------------------------------------------------------------------| 
| **Problem** | Challenge definition: includes the task description, requirements specification, and assigned difficulty level, and associated test cases.                            |
| **TestCase** | Datasets: input vs. expected output for automated verification.               |
| **Submission** | User solution: contains user code, associated problem, current status (`PENDING`, `DONE`, `WRONG_ANSWER`, `ERROR`), and evaluation results.                            |
| **Result** | Test execution report: status per test case (`PASSED`, `WRONG_ANSWER`, `RUNTIME_ERROR`, etc.), execution time, and `actual_output`. |

## API structure

- `problems/` — problems management and public problem views
- `submissions/` — create and fetch submissions
- `results/` — fetch submission/test results
- `test_cases/` — problem test cases

## Automated Testing
The project prioritizes reliability, using uv to orchestrate tests using pytest.
```bash
# Run all tests
uv run pytest

# Run in detailed mode
uv run pytest -v
```

## E2E Testing (Playwright)
Lopa includes End-to-End tests to ensure that the core user flows (like browsing problems and submitting code) work correctly in the browser.
```bash
# Installation
uv run playwright install
# Run tests in the background
uv run pytest --playwright
# Run tests with a visible browser (headed)
uv run pytest --playwright --headed
```

## Generating & Viewing Reports
After running the tests, Playwright can generate a detailed HTML report. This is particularly useful for debugging:
```bash
# Generate report during execution
uv run pytest --html=report.html --self-contained-html

# Open the report
xdg-open report.html  # Linux
# or just open report.html manually in your browser
```
### Troubleshooting Playwright (Linux)
If you encounter a "Host system is missing dependencies" warning, run the following command to install the required system libraries:
```bash
sudo playwright install-deps
#or
sudo ./.venv/bin/playwright install-deps
```

## Test Structure:
The test suite is organized by application modules to reflect the project structure and keep tests easier to maintain.
- `tests/test_problems.py` – tests for the `Problem` model, validations, and problem-related logic.
- `tests/test_test_cases.py` – tests for the `TestCase` creation, relationships, and expected input/output data.
- `tests/test_submissions.py` – tests for the `Submission` creation, evaluation flow, and submission status updates.
- `tests/test_results.py` – tests for `Result` creation and result status handling.
- `tests/test_users.py` – tests for user-related models and logic.
- `conftest.py` – common test data (fixtures).
- `e2e/test_submission_flow.py` – end-to-end tests for the complete user journey (browser-based).
- `e2e/conftest.py` – specific fixtures for browser and page initialization.

## Project Roadmap:
- [x] Core Execution Engine
- [ ] Blog Module (articles explained in simple terms)
- [ ] Flashcard system linked to assignments
- [ ] Point system and user rankings
- [ ] Hints system

## Project Documentation
- [Architecture Details](./Architecture.md)