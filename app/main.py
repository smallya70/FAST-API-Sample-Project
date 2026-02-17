from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .models import Post, PostCreate, Comment, CommentCreate
from .database import engine, get_db, Base
from . import db_models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Posts + Comments API")


@app.post("/posts", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Create a new post."""
    db_post = db_models.DBPost(
        title=post.title,
        content=post.content,
        author=post.author
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    """Get all posts."""
    return db.query(db_models.DBPost).all()


@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post by ID."""
    db_post = db.query(db_models.DBPost).filter(db_models.DBPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.post("/comments", response_model=Comment, status_code=201)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """Create a new comment on a post."""
    # Check if post exists
    db_post = db.query(db_models.DBPost).filter(db_models.DBPost.id == comment.post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = db_models.DBComment(
        post_id=comment.post_id,
        content=comment.content,
        author=comment.author
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@app.get("/posts/{post_id}/comments", response_model=List[Comment])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Get all comments for a specific post."""
    # Check if post exists
    db_post = db.query(db_models.DBPost).filter(db_models.DBPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return db.query(db_models.DBComment).filter(db_models.DBComment.post_id == post_id).all()
