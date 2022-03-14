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
            commentId = int(comment[i].id)
            vote = db.query(models.VoteComment).filter(
                (models.VoteComment.commentId == commentId) & (models.VoteComment.userId == id)).first()

            if vote is not None:
                if vote.is_up_vote == True:
                    setattr(comment[i], "isUpVoted", True)
                    setattr(comment[i], "isDownVoted", False)
                elif vote.is_down_vote == True:
                    setattr(comment[i], "isUpVoted", False)
                    setattr(comment[i], "isDownVoted", True)

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
# adding up vote


def addVoteForComment(id: int, req: Request, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    userid = int(req.headers.get('id'))

    vote = db.query(models.VoteComment).filter(
        (models.VoteComment.commentId == id) & (models.VoteComment.userId == userid)).first()

    if vote is None:
        add_vote = models.VoteComment(
            commentId=id, is_up_vote=True, userId=userid)

        db.add(add_vote)
        db.commit()
        db.refresh(add_vote)

        if countUpVote(id, db, comment):
            return {"details": f'added up vote for comment {add_vote.id}'}

    elif vote.is_down_vote == True:
        vote.is_down_vote = False
        vote.is_up_vote = True

        db.add(vote)
        db.commit()
        db.refresh(vote)

        if countUpVote(id, db, comment):
            return {"details": f'added up vote for comment {comment.id}'}

    elif vote.is_up_vote == True:
        return {"details": f'up vote already added for comment {comment.id}'}


def countUpVote(commentId, db, comment):
    up_count = db.query(models.VoteComment).filter(
        (models.VoteComment.commentId == commentId) & (models.VoteComment.is_up_vote == True)).count()
    down_count = db.query(models.VoteComment).filter(
        (models.VoteComment.commentId == commentId) & (models.VoteComment.is_down_vote == True)).count()

    print(up_count, down_count)

    comment.up_vote_count = int(up_count)
    comment.down_vote_count = int(down_count)

    try:
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')


def addDownVoteForComment(id: int, req: Request, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    userid = int(req.headers.get('id'))

    vote = db.query(models.VoteComment).filter(
        (models.VoteComment.commentId == id) & (models.VoteComment.userId == userid)).first()

    if vote is None:
        add_vote = models.VoteComment(
            commentId=id, is_down_vote=True, userId=userid)

        db.add(add_vote)
        db.commit()
        db.refresh(add_vote)

        if countUpVote(id, db, comment):
            return {"details": f'added down vote for comment {add_vote.id}'}

    elif vote.is_up_vote == True:
        vote.is_up_vote = False
        vote.is_down_vote = True

        db.add(vote)
        db.commit()
        db.refresh(vote)

        if countUpVote(id, db, comment):
            return {"details": f'added down vote for comment {vote.id}'}

    elif vote.is_down_vote == True:
        return {"details": f'down vote already added for comment {vote.id}'}
