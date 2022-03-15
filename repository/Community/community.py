import models
import os
import shutil
import time
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError
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
            postId = int(posts[i].id)
            vote = db.query(models.VotePost).filter(
                (models.VotePost.postId == postId) & (models.VotePost.userId == id)).first()

            if vote is not None:
                if vote.is_up_vote == True:
                    setattr(posts[i], "isUpVoted", True)
                    setattr(posts[i], "isDownVoted", False)
                elif vote.is_down_vote == True:
                    setattr(posts[i], "isUpVoted", False)
                    setattr(posts[i], "isDownVoted", True)

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

# removes posts comment


def removeCommunityPostsComment(postId: int, commentId: int, req: Request, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == postId).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")
    if int(post.userId) != int(req.headers.get('id')):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{postId} Post not belong to this user")

    comments = db.query(models.Comments).filter(
        models.Comments.id == commentId).first()

    if comments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    db.query(models.Comments).filter(
        models.Comments.id == commentId).delete(synchronize_session=False)
    db.commit()

    return {'details': f'{postId} Post {commentId} comment is deleted successfully'}


# add up vote


def addUpVoteForPost(id: int, req: Request, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Id")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    userId = int(req.headers.get('id'))
    votes = db.query(models.VotePost).filter((models.VotePost.postId ==
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
        CountVote(db, id)
        return {"details": f'Up vote already added for post {votes.postId}'}


def CountVote(db: session, id):
    up_count = db.query(models.VotePost).filter(
        (models.VotePost.postId == id) & (models.VotePost.is_up_vote == True)).count()
    down_count = db.query(models.VotePost).filter(
        (models.VotePost.postId == id) & (models.VotePost.is_down_vote == True)).count()

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    post.up_vote_count = int(up_count)
    post.down_vote_count = int(down_count)

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
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Id")

    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    userId = int(req.headers.get('id'))
    votes = db.query(models.VotePost).filter((models.VotePost.postId ==
                                             id) & (models.VotePost.userId == userId)).first()

    if votes is None:
        vote_post = models.VotePost(
            postId=id, is_down_vote=True, userId=userId)
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
        return {"details": f'Down vote already added for post {votes.postId}'}


def CountDownVote(db: session, id):
    up_count = db.query(models.VotePost).filter(
        (models.VotePost.postId == id) & (models.VotePost.is_up_vote == True)).count()
    down_count = db.query(models.VotePost).filter(
        (models.VotePost.postId == id) & (models.VotePost.is_down_vote == True)).count()

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    post.up_vote_count = int(up_count)
    post.down_vote_count = int(down_count)

    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# add image to post


def addImageToCommunityPost(id: int, req: Request,  db: session, file):
    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Id Is Invalid")

    # check file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'{file.content_type} is invalid file type please upload jpeg and png files.')

    path = './assets/community_post_images'
    # check specific file directory exits
    isExist = os.path.exists(path)

    if not isExist:
        # create new directory
        os.makedirs(path)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filenames = timestr+file.filename
    file_location = f'{path}/{filenames}'
    with open(file_location, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_image = models.CommunityPostImages(image_name=filenames, postId=id)

    try:
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return {"msg": "Add new Image successfully", "details": new_image}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} is not in the disease table please check the id and try again')

# remove image from post


def removeImageFromPost(id: int, req: Request,  db: session):
    if req.headers.get('id') is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Please Send User ID on headers")

    # get the specific file name
    plant_image = db.query(models.CommunityPostImages).filter(
        models.CommunityPostImages.id == id).first()

    if plant_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} is not in the disease image table please check the id and try again')

    # get post using plant image post id
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == plant_image.postId).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'There is Nno post related to the {id}')

    if int(post.userId) != int(req.headers.get('id')):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'This user cannot remove post image')

    path = './assets/community_post_images'
    if os.path.exists(path):
        file_location = path + '/'+plant_image.image_name
        if os.path.exists(file_location):
            # remove the file from server
            os.remove(file_location)
            # remove row in the table
            db.query(models.CommunityPostImages).filter(
                models.CommunityPostImages.id == id).delete(synchronize_session=False)
            db.commit()
            return {'detail': f'{id} image deleted'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{plant_image.image_name} is not in the server')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There is no image in the server')
