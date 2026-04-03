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
│   │   ├── migrations/        # Here are the files 0001_initial and 0002_testcase
│   │   ├── models.py          # Problem and Test Case Models
│   │   ├── apps.py
│   │   └── ...
│   └── users/                 # Custom User Model & Authentication logic
│       ├── migrations/
│       ├── models.py          # Custom User model (Architects/Developers)
│       ├── apps.py
│       └── ...      
├── config/                    # Main project settings folder
│   ├── settings.py            # Configuration of databases, apps, and pytest
│   ├── urls.py
│   └── wsgi.py 
├── static/                    # Global static files
│    ├── css/
│    └── js/
├── templates/                 # Global templates for the whole project
│    ├── base.html             # Main layout (navbar, footer, etc.)
│    └── index.html            # Landing page
├── tests/                     # Folder containing automated tests
│   ├── test_engine.py         # Tests for Submission logic
│   ├── test_problems.py       # Tests for Problem and TestCase models
│   └── test_users.py          # Tests for User registration and login
├── .python-version            # Defines the project's Python version (3.13)
├── conftest.py                # Pytest fixtures (shared test data)
├── manage.py                  # Django management script
├── pyproject.toml             # Modern project configuration (dependencies)
├── pytest.ini                 # Pytest configuration
├── README.md                  # Project documentation
└── uv.lock                    # Deterministic dependency lockfile
```
