"""Tests for Post endpoints."""


def test_create_post_success(client):
    """Test creating a post successfully."""
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post with enough content.",
        "author": "Test Author"
    }
    response = client.post("/posts", json=post_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post with enough content."
    assert data["author"] == "Test Author"
    assert "created_at" in data


def test_create_post_duplicate_id(client):
    """Test creating a post with duplicate ID fails."""
    post_data = {
        "id": 1,
        "title": "First Post",
        "content": "This is the first post.",
        "author": "Author One"
    }
    response1 = client.post("/posts", json=post_data)
    assert response1.status_code == 200
    
    # Try to create another post with the same ID
    post_data2 = {
        "id": 1,
        "title": "Second Post",
        "content": "This is the second post.",
        "author": "Author Two"
    }
    response2 = client.post("/posts", json=post_data2)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Post id already exists"


def test_create_post_invalid_title_too_short(client):
    """Test creating a post with too short title fails."""
    post_data = {
        "id": 1,
        "title": "Hi",  # Too short (min 3 chars)
        "content": "This is a test post.",
        "author": "Test Author"
    }
    response = client.post("/posts", json=post_data)
    assert response.status_code == 422


def test_create_post_invalid_content_too_short(client):
    """Test creating a post with too short content fails."""
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "Short",  # Too short (min 10 chars)
        "author": "Test Author"
    }
    response = client.post("/posts", json=post_data)
    assert response.status_code == 422


def test_get_posts_empty(client):
    """Test getting posts when none exist."""
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == []


def test_get_posts_multiple(client):
    """Test getting multiple posts."""
    # Create first post
    post1 = {
        "id": 1,
        "title": "First Post",
        "content": "Content of first post.",
        "author": "Author One"
    }
    client.post("/posts", json=post1)
    
    # Create second post
    post2 = {
        "id": 2,
        "title": "Second Post",
        "content": "Content of second post.",
        "author": "Author Two"
    }
    client.post("/posts", json=post2)
    
    # Get all posts
    response = client.get("/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


def test_get_post_by_id_success(client):
    """Test getting a specific post by ID."""
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Test Author"
    }
    client.post("/posts", json=post_data)
    
    response = client.get("/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Post"


def test_get_post_by_id_not_found(client):
    """Test getting a non-existent post returns 404."""
    response = client.get("/posts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_create_post_without_optional_author(client):
    """Test creating a post without optional author field."""
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post without author."
    }
    response = client.post("/posts", json=post_data)
    assert response.status_code == 200
    data = response.json()
    assert data["author"] is None
