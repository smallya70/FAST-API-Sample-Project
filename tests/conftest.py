import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import posts, comments


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear the storage before each test."""
    posts.clear()
    comments.clear()
    yield
    posts.clear()
    comments.clear()
