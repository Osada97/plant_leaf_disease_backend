from fastapi import Request
from sqlalchemy.orm import session
from models import CommunityPost
import models


def createNewCommunityPost(id, request: CommunityPost, db: session):
    new_post = models.CommunityPost(
        post_title=request.post_title, description=request.description, userId=id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def getCommunityPosts(req: Request, db: session):
    posts = db.query(models.CommunityPost).all()

    if req.headers.get('id'):
        id = req.headers.get('id')
        for i in range(len(posts)):
            if posts[i].userId == int(id):
                setattr(posts[i], "isUser", True)
            else:
                setattr(posts[i], "isUser", False)

    return posts


def getCommunityPostById(id: int, db: session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.userId == id).all()

    return posts
