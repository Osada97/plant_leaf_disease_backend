from urllib import request
import models
from fastapi import Request, status, HTTPException
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError
from schemas.community_schemas import CreateComment, ShowComment

# add comment to the post


def addCommentToPost(id: int, req: Request, request: CreateComment, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invlid post id")

    userId = int(req.headers.get('id'))

    new_comment = models.Comments(
        comment=request.comment, postId=id, userid=userId)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

# get comment based on post id


def getCommentOnId(id: int, req: Request, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.postId == id).all()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments related to the post")

    if req.headers.get('id'):
        id = req.headers.get('id')
        for i in range(len(comment)):
            if comment[i].userid == int(id):
                setattr(comment[i], "isUser", True)
            else:
                setattr(comment[i], "isUser", False)

    return comment

# remove comment based on comment id


def removeCommentId(id: int, req: Request, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    if int(req.headers.get('id')) != int(comment.userid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Comment not belong to this user")

    db.query(models.Comments).filter(
        models.Comments.id == id).delete(synchronize_session=False)
    db.commit()

    return {'details': f'Id {id} Comment is deleted successfully'}


# update comment based on id
def updateCommentId(id: int, req: Request, request: CreateComment, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    if int(req.headers.get('id')) != int(comment.userid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Comment not belong to this user")

    comment.comment = request.comment

    try:
        db.commit()
        db.refresh(comment)
        return comment
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')
