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


def getCommunityPosts(db: session):
    posts = db.query(models.CommunityPost).all()
    return posts
