from fastapi import Request, HTTPException, status
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError
import models
from schemas.community_schemas import CommunityPost

# create community posts


def createNewCommunityPost(id, request: CommunityPost, db: session):
    new_post = models.CommunityPost(
        post_title=request.post_title, description=request.description, userId=id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get community posts


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

# get community post based on user id


def getCommunityPostById(id: int, db: session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.userId == id).all()

    return posts

# update community posts


def updateCommunityPost(id: int, req: Request, request: CommunityPost, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    if int(req.headers.get('id')) != int(post.userId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Post not belong to this user")

    post.post_title = request.post_title
    post.description = request.description

    try:
        db.commit()
        db.refresh(post)
        return post
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# remove community post


def removeCommunityPost(id: int, req: Request, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    if int(req.headers.get('id')) != int(post.userId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Post not belong to this user")

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).delete(synchronize_session=False)
    db.commit()
    return {'details': f'{id} Post is deleted successfully'}


# add up vote
def addUpVoteForPost(id: int, req: Request, db: session):
    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    userId = int(req.headers.get('id'))
    votes = db.query(models.VotePost).filter((models.VotePost.id ==
                                             id) & (models.VotePost.userId == userId)).first()

    if votes is None:
        vote_post = models.VotePost(
            postId=id, is_up_vote=True, userId=userId)
        db.add(vote_post)
        db.commit()
        db.refresh(vote_post)

        vote_post = vote_post

        if CountVote(db, id):
            return {"details": f'added vote for post {vote_post.postId}'}

    elif votes.is_down_vote == True:

        votes.is_up_vote = True
        votes.is_down_vote = False

        db.add(votes)
        db.commit()
        db.refresh(votes)
        votes = votes

        if CountVote(db, id):
            return {"details": f'added vote for post {votes.postId}'}

    elif votes.is_up_vote == True:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Up vote already added")


def CountVote(db: session, id):
    up_count = db.query(models.VotePost).filter(
        (models.VotePost.id == id) & (models.VotePost.is_up_vote == True)).count()

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    post.up_vote_count = int(up_count)

    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# added down vote


def addDownVoteForPost(id: int, req: Request, db: session):
    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    userId = int(req.headers.get('id'))
    votes = db.query(models.VotePost).filter((models.VotePost.id ==
                                             id) & (models.VotePost.userId == userId)).first()

    if votes is None:
        vote_post = models.VotePost(
            postId=id, is_up_vote=True, userId=userId)
        db.add(vote_post)
        db.commit()
        db.refresh(vote_post)

        vote_post = vote_post

        if CountDownVote(db, id):
            return {"details": f'added down vote for post {vote_post.postId}'}

    elif votes.is_up_vote == True:

        votes.is_up_vote = False
        votes.is_down_vote = True

        db.add(votes)
        db.commit()
        db.refresh(votes)
        votes = votes

        if CountDownVote(db, id):
            return {"details": f'added down vote for post {votes.postId}'}

    elif votes.is_down_vote == True:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail=f"Up vote already added")


def CountDownVote(db: session, id):
    up_count = db.query(models.VotePost).filter(
        (models.VotePost.id == id) & (models.VotePost.is_down_vote == True)).count()

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    post.up_vote_count = int(up_count)

    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')
