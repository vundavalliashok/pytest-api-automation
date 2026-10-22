# Pytest API Automation Framework

A portfolio-ready REST API testing project using **Python, FastAPI, pytest, TestClient, parameterized tests, coverage, and GitHub Actions**.

## Features

- FastAPI REST endpoints: health check and user create/list/get/delete
- Positive, negative, duplicate-data, and validation tests
- pytest fixtures for reusable test setup and isolated test data
- Parameterized validation cases
- Coverage summary and HTML coverage report
- GitHub Actions CI on pushes, pull requests, and manual runs
- Interactive API documentation at `/docs`

> **Demo limitation:** users are stored in memory, so data disappears when the process restarts. The `/testing/reset` route exists only to simplify test isolation. Do not expose it in production.

## Requirements

- Python 3.11 or 3.12 recommended
- VS Code with the Python extension
- Git (for GitHub publishing)

Check Python from the VS Code terminal:

```powershell
python --version
python -m pip --version
```

If `python` is not recognized on Windows, install Python from https://www.python.org/downloads/ and enable **Add python.exe to PATH**, then restart VS Code. You can also try `py --version` if the Python launcher is installed.

## Setup in VS Code (Windows PowerShell)

Open the project folder in VS Code, then choose **Terminal → New Terminal**. Run these commands from the folder containing `requirements.txt`.

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, either use Command Prompt with `.venv\Scripts\activate.bat`, or for the current PowerShell session run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

In VS Code, use **Ctrl+Shift+P → Python: Select Interpreter** and select the interpreter inside `.venv`.

## Run the tests

Run all tests and coverage:

```powershell
python -m pytest
```

Run one test file:

```powershell
python -m pytest tests/test_health.py
```

Run one test by name:

```powershell
python -m pytest -k duplicate_email
```

Run without coverage:

```powershell
python -m pytest -o addopts=""
```

The suite uses FastAPI's in-process `TestClient`; **you do not need to start the API server to run tests**.

## Start the API manually

```powershell
python -m uvicorn app.main:app --reload
```

Then visit:

- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Stop the server with `Ctrl+C`.

## Expected test output

Exact durations and coverage percentages can vary by Python/dependency versions. A successful run ends with output similar to:

```text
============================= test session starts =============================
collected 12 items

tests/test_health.py .                                                   [  8%]
tests/test_users.py ...........                                          [100%]

============================== 12 passed ==============================
---------- coverage: ... ----------
Coverage HTML written to dir htmlcov
```

Open the HTML report after running tests:

```powershell
code htmlcov/index.html
```

If `code` is unavailable, open `htmlcov\index.html` from File Explorer.

## API examples

Create a user:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/users `
  -ContentType "application/json" `
  -Body '{"name":"Asha Rao","email":"asha@example.com","age":30}'
```

List users:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/users
```

## GitHub portfolio setup

Create an empty GitHub repository named `pytest-api-automation`. From the project root:

```powershell
git init
git add .
git commit -m "Build FastAPI pytest automation framework"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/pytest-api-automation.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If the repository already contains a README or other commits, create it empty or pull/reconcile the existing history before pushing.

GitHub Actions runs the test suite on pushes and pull requests. View the result in the repository's **Actions** tab.

## Troubleshooting

### `No module named pytest` or `No module named fastapi`

Activate `.venv`, then run:

```powershell
python -m pip install -r requirements.txt
```

### `python` is not recognized

Install Python and enable PATH, restart VS Code, then check `python --version`. If available, try `py -m venv .venv`.

### `ModuleNotFoundError: No module named 'app'`

Run pytest from the project root—the same folder that contains `app`, `tests`, `pytest.ini`, and `requirements.txt`:

```powershell
python -m pytest
```

Do not run it from inside `app` or `tests`.

### PowerShell says script execution is disabled

Use the process-only execution policy command in the activation section, or activate from Command Prompt with `.venv\Scripts\activate.bat`.

### Port 8000 is already in use

Stop the other process, or run `python -m uvicorn app.main:app --reload --port 8001`.

### Test count differs from the README

The test count may change as you add cases. The important success signal is that pytest reports zero failures and exits with code `0`.

## Suggested next improvements

1. Add SQL Server or PostgreSQL persistence and database fixtures.
2. Add request/response schema contract tests.
3. Add mocks for external dependencies.
4. Add JUnit XML output for CI test reporting.
5. Add linting with Ruff and security checks.
6. Add Docker and a multi-stage build.
