from env import Environment
import models
import os
import shutil
import time
from fastapi import Request, status, HTTPException
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError
from schemas.community_schemas import CreateComment, ShowComment

# add comment to the post


def addCommentToPost(id: int, new_current_user, request: CreateComment, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invlid post id")

    userId = new_current_user.id

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
    getDefaultsImages(comment)
    return comment

# remove comment based on comment id


def removeCommentId(id: int, new_current_user, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    if new_current_user.id != int(comment.userid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Comment not belong to this user")

    db.query(models.Comments).filter(
        models.Comments.id == id).delete(synchronize_session=False)
    db.commit()

    return {'details': f'Id {id} Comment is deleted successfully'}


# update comment based on id
def updateCommentId(id: int, new_current_user, request: CreateComment, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    if new_current_user.id != int(comment.userid):
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


def addVoteForComment(id: int, new_current_user, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    userid = new_current_user.id

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

# calculate up vote and down vote count and update table


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

# add down vote for comment


def addDownVoteForComment(id: int, new_current_user, db: session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    userid = new_current_user.id

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

# add image to comment


def addImageToComment(id: int, db: session, file, new_current_user):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comments in this id")

    userId = new_current_user.id

    if userId != comment.userid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"This User Not Belong Comment {id}")

    for i in range(0, 2):
        # adding image
        # check file type
        if file[i].content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail=f'{file[i].content_type} is invalid file type please upload jpeg and png files.')

        path = './assets/community_post_comment_images'
        # check specific file directory exits
        isExist = os.path.exists(path)

        if not isExist:
            # create new directory
            os.makedirs(path)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        filenames = timestr+file[i].filename.replace(" ", "")
        file_location = f'{path}/{filenames}'
        with open(file_location, 'wb') as buffer:
            shutil.copyfileobj(file[i].file, buffer)

        new_image = models.CommunityCommentImage(
            image_name=filenames, commentsId=id)

        try:
            db.add(new_image)
            db.commit()
            db.refresh(new_image)

            new_image.image_name = f'{Environment.getBaseEnv()}assets/community_post_comment_images/{new_image.image_name}'

            reve = {"msg": "Add new Image successfully",
                    "details": f'{id} image uploaded'}
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'id {id} is not in the disease table please check the id and try again')

    return reve

# remove comment


def RemoveImageInComment(id: int, db: session,  new_current_user):
    commentImage = db.query(models.CommunityCommentImage).filter(
        models.CommunityCommentImage.id == id).first()

    if commentImage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no image in this id")

    # get parent comment that related to image
    comment = db.query(models.Comments).filter(
        models.Comments.id == commentImage.commentsId).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no comment belong this image")

    userId = new_current_user.id

    if userId != comment.userid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"This User Not Belong Comment {id}")

    # remove image

    path = './assets/community_post_comment_images'
    # # check specific file directory exits
    if os.path.exists(path):
        file_location = path + '/'+commentImage.image_name
        if os.path.exists(file_location):
            # remove the file from server
            os.remove(file_location)
            # remove row in the table
            db.query(models.CommunityCommentImage).filter(
                models.CommunityCommentImage.id == id).delete(synchronize_session=False)
            db.commit()
            return {'detail': f'{id} image deleted'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{commentImage.image_name} is not in the server')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no image in the server')


def getDefaultsImages(comment):
    if hasattr(comment, '__len__'):
        for i in range(len(comment)):
            comment[i].user.profile_picture = ""
            if comment[i].user.profile_picture is None or len(comment[i].user.profile_picture) == 0:
                comment[i].user.profile_picture = f"{Environment.getBaseEnv()}defaults/user.png"
            else:
                comment[i].user.profile_picture = f"{Environment.getBaseEnv()}profiles/user/{comment[i].user.profile_picture}"

            if len(comment[i].image) > 0:
                for j in range(len(comment[i].image)):
                    comment[i].image[j].image_name = f'{Environment.getBaseEnv()}assets/community_post_images/{comment[i].image[j].image_name}'

            else:
                s = []
                s = f'{Environment.getBaseEnv()}defaults/communityDefault.jpg'
                comment[i].default_image = s

        return comment
    else:
        if comment.user.profile_picture is None or len(comment.user.profile_picture) == 0:
            comment.user.profile_picture = f"{Environment.getBaseEnv()}defaults/user.png"
        else:
            comment.user.profile_picture = f"{Environment.getBaseEnv()}profiles/user/{comment.user.profile_picture}"

        if len(comment.image) > 0:
            for j in range(len(comment.image)):
                comment.image[j].image_name = f'{Environment.getBaseEnv()}assets/community_post_images/{comment.image[j].image_name}'

        else:
            s = []
            s = f'{Environment.getBaseEnv()}defaults/communityDefault.jpg'
            comment.default_image = s

        return comment
