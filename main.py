from fastapi import FastAPI, HTTPException
from typing import List
from .models import Post, Comment
from .storage import posts, comments

app = FastAPI(title="Posts + Comments API")


@app.post("/posts", response_model=Post)
def create_post(post: Post):
    if any(p.id == post.id for p in posts):
        raise HTTPException(status_code=400, detail="Post id already exists")
    posts.append(post)
    return post


@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts


@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    for p in posts:
        if p.id == post_id:
            return p
    raise HTTPException(status_code=404, detail="Post not found")


@app.post("/comments", response_model=Comment)
def create_comment(comment: Comment):
    if not any(p.id == comment.post_id for p in posts):
        raise HTTPException(status_code=404, detail="Post not found")

    if any(c.id == comment.id for c in comments):
        raise HTTPException(status_code=400, detail="Comment id already exists")

    comments.append(comment)
    return comment


@app.get("/posts/{post_id}/comments", response_model=List[Comment])
def get_comments(post_id: int):
    if not any(p.id == post_id for p in posts):
        raise HTTPException(status_code=404, detail="Post not found")

    return [c for c in comments if c.post_id == post_id]
