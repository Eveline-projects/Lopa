## Modular Architecture
The project uses the apps/ directory structure to separate business logic from the main configuration (config/). This approach (known as “Separation of Concerns”) makes it easier to manage a large number of Django applications, improves code readability, and allows for easier addition of new modules, such as the upcoming Blog or the Flashcards system.
```text
Lopa/
├── apps/                       # Domain Layer (Django Applications)
│   ├── problems/               # Domain: Problem management
│   │   ├── migrations/
│   │   ├── models.py           # Problem model
│   │   ├── services.py         # Business logic (ProblemService)
│   │   └── ...
│   ├── results/                # Domain: Evaluation & status tracking
│   │   ├── migrations/
│   │   ├── models.py           # Result model
│   │   ├── services.py         # Business logic (ResultService)
│   │   └── ...
│   ├── submissions/            # Domain: User code submissions
│   │   ├── migrations/
│   │   ├── models.py           # Submission model
│   │   ├── services.py         # Business logic (SubmissionService)
│   │   └── ...
│   ├── test_cases/             # Domain: Test data management
│   │   ├── migrations/
│   │   ├── models.py           # TestCase model
│   │   ├── services.py         # Business logic (TestCaseService)
│   │   └── ...
│   └── users/                  # Domain: User profiles & auth
│       ├── migrations/
│       ├── models.py           # Custom User Model
│       └── ...
├── config/                     # System configuration (Settings, URLs)
├── static/                     # Global static assets (CSS, JS)
├── templates/                  # Shared base templates and layouts
├── tests/                      # Automated Test Suite (Pytest)
│   ├── problems/               # Tests for Problems domain
│   ├── results/                # Tests for Results domain
│   ├── submissions/            # Tests for Submissions domain
│   ├── test_cases/             # Tests for TestCase domain
│   └── users/                  # Tests for Users domain
├── .python-version             # Python version (3.13)
├── Architecture.md             # Detailed architectural documentation
├── conftest.py                 # Shared Pytest fixtures
├── manage.py                   # Django management script
├── pyproject.toml              # Dependency management (uv)
├── pytest.ini                  # Pytest configuration
├──  README.md                  # Main project documentation
└── uv.lock                    # Deterministic dependency lockfile
```
