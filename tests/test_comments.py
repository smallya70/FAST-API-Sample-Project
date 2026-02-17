"""Tests for Comment endpoints."""


def test_create_comment_success(client):
    """Test creating a comment successfully."""
    # First create a post
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Post Author"
    }
    client.post("/posts", json=post_data)
    
    # Create a comment
    comment_data = {
        "id": 1,
        "post_id": 1,
        "content": "This is a test comment.",
        "author": "Comment Author"
    }
    response = client.post("/comments", json=comment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["post_id"] == 1
    assert data["content"] == "This is a test comment."
    assert data["author"] == "Comment Author"
    assert "created_at" in data


def test_create_comment_post_not_found(client):
    """Test creating a comment for non-existent post fails."""
    comment_data = {
        "id": 1,
        "post_id": 999,  # Post doesn't exist
        "content": "This is a test comment.",
        "author": "Comment Author"
    }
    response = client.post("/comments", json=comment_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_create_comment_duplicate_id(client):
    """Test creating a comment with duplicate ID fails."""
    # Create a post
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Post Author"
    }
    client.post("/posts", json=post_data)
    
    # Create first comment
    comment_data1 = {
        "id": 1,
        "post_id": 1,
        "content": "First comment.",
        "author": "Author One"
    }
    response1 = client.post("/comments", json=comment_data1)
    assert response1.status_code == 200
    
    # Try to create another comment with the same ID
    comment_data2 = {
        "id": 1,
        "post_id": 1,
        "content": "Second comment.",
        "author": "Author Two"
    }
    response2 = client.post("/comments", json=comment_data2)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Comment id already exists"


def test_create_comment_invalid_content_too_short(client):
    """Test creating a comment with too short content fails."""
    # Create a post
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Post Author"
    }
    client.post("/posts", json=post_data)
    
    # Try to create comment with too short content
    comment_data = {
        "id": 1,
        "post_id": 1,
        "content": "X",  # Too short (min 2 chars)
        "author": "Comment Author"
    }
    response = client.post("/comments", json=comment_data)
    assert response.status_code == 422


def test_get_comments_for_post_empty(client):
    """Test getting comments for a post when none exist."""
    # Create a post
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Post Author"
    }
    client.post("/posts", json=post_data)
    
    # Get comments for the post
    response = client.get("/posts/1/comments")
    assert response.status_code == 200
    assert response.json() == []


def test_get_comments_for_post_multiple(client):
    """Test getting multiple comments for a post."""
    # Create a post
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Post Author"
    }
    client.post("/posts", json=post_data)
    
    # Create first comment
    comment1 = {
        "id": 1,
        "post_id": 1,
        "content": "First comment on post.",
        "author": "Author One"
    }
    client.post("/comments", json=comment1)
    
    # Create second comment
    comment2 = {
        "id": 2,
        "post_id": 1,
        "content": "Second comment on post.",
        "author": "Author Two"
    }
    client.post("/comments", json=comment2)
    
    # Get comments for the post
    response = client.get("/posts/1/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2
    assert all(comment["post_id"] == 1 for comment in data)


def test_get_comments_for_non_existent_post(client):
    """Test getting comments for a non-existent post fails."""
    response = client.get("/posts/999/comments")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_get_comments_filters_by_post_id(client):
    """Test that getting comments only returns comments for the specified post."""
    # Create two posts
    client.post("/posts", json={
        "id": 1,
        "title": "First Post",
        "content": "Content of first post.",
        "author": "Author One"
    })
    client.post("/posts", json={
        "id": 2,
        "title": "Second Post",
        "content": "Content of second post.",
        "author": "Author Two"
    })
    
    # Create comments for both posts
    client.post("/comments", json={
        "id": 1,
        "post_id": 1,
        "content": "Comment on first post.",
        "author": "Commenter"
    })
    client.post("/comments", json={
        "id": 2,
        "post_id": 2,
        "content": "Comment on second post.",
        "author": "Commenter"
    })
    
    # Get comments for first post only
    response = client.get("/posts/1/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["post_id"] == 1
    assert data[0]["content"] == "Comment on first post."


def test_create_comment_without_optional_author(client):
    """Test creating a comment without optional author field."""
    # Create a post
    post_data = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post.",
        "author": "Post Author"
    }
    client.post("/posts", json=post_data)
    
    # Create comment without author
    comment_data = {
        "id": 1,
        "post_id": 1,
        "content": "Comment without author."
    }
    response = client.post("/comments", json=comment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["author"] is None
