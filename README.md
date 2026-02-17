# FastAPI Posts + Comments API

A simple FastAPI application for managing posts and comments.

## Features

- Create and retrieve posts
- Create and retrieve comments for posts
- Input validation using Pydantic models
- Comprehensive test suite with pytest

## Installation

1. Create a virtual environment:
```powershell
py -m venv venv
```

2. Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```powershell
.\venv\Scripts\uvicorn.exe app.main:app --reload
```

The API will be available at:
- **API Docs (Swagger UI):** http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc):** http://127.0.0.1:8000/redoc
- **API Base URL:** http://127.0.0.1:8000

## API Endpoints

### Posts
- `POST /posts` - Create a new post
- `GET /posts` - Get all posts
- `GET /posts/{post_id}` - Get a specific post

### Comments
- `POST /comments` - Create a comment
- `GET /posts/{post_id}/comments` - Get comments for a post

## Running Tests

### Option 1: Using the PowerShell script
```powershell
.\venv\Scripts\Activate.ps1
.\run_tests.ps1
```

### Option 2: Direct pytest command
```powershell
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
pytest -v
```

### Run specific test file
```powershell
$env:PYTHONPATH = "."
pytest tests/test_posts.py -v
```

### Run with coverage
```powershell
$env:PYTHONPATH = "."
pytest --cov=app --cov-report=html
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures and configuration
├── test_posts.py        # Tests for post endpoints
└── test_comments.py     # Tests for comment endpoints
```

**Current test coverage:** 18 tests covering all endpoints

## Project Structure

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # Pydantic models
│   └── storage.py       # In-memory data storage
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_posts.py
│   └── test_comments.py
├── venv/                # Virtual environment
├── .gitignore
├── requirements.txt
├── pyproject.toml       # Pytest configuration
├── run_tests.ps1        # Test runner script
└── README.md
```

## Development

To contribute to this project:

1. Make your changes
2. Run tests to ensure everything works
3. Commit and push to GitHub

```powershell
git add .
git commit -m "Your commit message"
git push
```
