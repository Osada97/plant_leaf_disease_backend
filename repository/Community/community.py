from operator import and_
from requests import post

from sqlalchemy import desc
import models
import os
import shutil
import time
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError
from repository.Community.comments import getDefaultsImagesComment
from schemas.community_schemas import CommunityPost

# create community posts


def createNewCommunityPost(request: CommunityPost, db: session, new_current_user):
    new_post = models.CommunityPost(
        post_title=request.post_title, description=request.description, userId=new_current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return getDefaultsImages(new_post)

# get community posts


def getCommunityPosts(req: Request, db: session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.is_approve == True).all()

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

    return getDefaultsImages(posts)

# get community post based on user id


def getCommunityPostById(id: int, db: session, new_current_user):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.userId == id).order_by(desc(models.CommunityPost.id)).all()

    if new_current_user.id:
        id = new_current_user.id
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

    return getDefaultsImages(posts)

# get post using post and comments id


def getSpecificPostByPostId(id: int, db: session, new_current_user):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).order_by(models.CommunityPost.id).first()

    if new_current_user.id:
        id = new_current_user.id
        postId = int(post.id)
        vote = db.query(models.VotePost).filter(and_(models.VotePost.postId == postId, models.VotePost.userId == id)
                                                ).order_by(models.VotePost.id).first()
        if vote is not None:
            if vote.is_up_vote == True:
                setattr(post, "isUpVoted", True)
                setattr(post, "isDownVoted", False)
            elif vote.is_down_vote == True:
                setattr(post, "isUpVoted", False)
                setattr(post, "isDownVoted", True)

        if post.userId == int(id):
            setattr(post, "isUser", True)
        else:
            setattr(post, "isUser", False)

        for i in range(len(post.comment)):
            comment = post.comment
            commentId = int(comment[i].id)
            vote = db.query(models.VoteComment).filter(and_(models.VoteComment.commentId == commentId, models.VoteComment.userId == id)
                                                       ).order_by(models.VoteComment.id).first()

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

    getDefaultsImagesComment(post.comment)
    return getDefaultsImagesInSpecific(post)

# update community posts


def updateCommunityPost(id: int, new_current_user, request: CommunityPost, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if new_current_user.id != int(post.userId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Post not belong to this user")

    post.post_title = request.post_title
    post.description = request.description

    try:
        db.commit()
        db.refresh(post)
        return getDefaultsImages(post)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# remove community post


def removeCommunityPost(id: int, new_current_user, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if new_current_user.id != int(post.userId):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Post not belong to this user")

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).delete(synchronize_session=False)
    db.commit()
    return {'details': f'{id} Post is deleted successfully'}

# removes posts comment


def removeCommunityPostsComment(postId: int, commentId: int, new_current_user, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == postId).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if int(post.userId) != new_current_user.id:
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


def addUpVoteForPost(id: int, new_current_user, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Id")

    userId = new_current_user.id
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


def addDownVoteForPost(id: int, new_current_user, db: session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Id")

    userId = new_current_user.id
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

# removed added vote


def removedAddedVote(id: int, new_current_user, db: session):
    post = db.query(models.VotePost).filter(and_(
        models.VotePost.postId == id, models.VotePost.userId == new_current_user.id)).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no vote")

    if post.is_up_vote:
        db.query(models.VotePost).filter(
            and_(
                models.VotePost.postId == id, models.VotePost.userId == new_current_user.id)).delete(synchronize_session=False)
        db.commit()

        if CountVote(db, id):
            return {"details": f'Remove vote form post'}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no up vote")


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

# removed added vote


def removedDownVote(id: int, new_current_user, db: session):
    post = db.query(models.VotePost).filter(and_(
        models.VotePost.postId == id, models.VotePost.userId == new_current_user.id)).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no vote")

    if post.is_down_vote:
        db.query(models.VotePost).filter(
            and_(
                models.VotePost.postId == id, models.VotePost.userId == new_current_user.id)).delete(synchronize_session=False)
        db.commit()

        if CountVote(db, id):
            return {"details": f'Remove vote form post'}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no down vote")

# add image to post


def addImageToCommunityPost(id: int, new_current_user, db: session, file):

    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Id Is Invalid")

    if int(post.userId) != new_current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'This user cannot add post image')

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
    filenames = timestr+file.filename.replace(" ", "")
    file_location = f'{path}/{filenames}'
    with open(file_location, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_image = models.CommunityPostImages(image_name=filenames, postId=id)

    try:
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        reva = {"msg": "Add new Image successfully",
                "details": f'{new_image.id} Images Uploaded'}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} is not in the disease table please check the id and try again')

    return reva

# remove image from post


def removeImageFromPost(id: int, new_current_user,  db: session):

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

    if int(post.userId) != new_current_user.id:
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

# set default owner image


def getDefaultsImages(posts):
    if hasattr(posts, '__len__'):
        pevId = ''
        for i in range(len(posts)):
            if len(posts[i].owner.profile_picture) == 0 and pevId != posts[i].owner.id:
                profile_pic = f"defaults/user.jpg"
                pevId = posts[i].owner.id
            else:
                if pevId != posts[i].owner.id:
                    profile_pic = f"assets/profiles/user/{posts[i].owner.profile_picture}"
                    pevId = posts[i].owner.id

            if len(posts[i].images) > 0:
                for j in range(len(posts[i].images)):
                    posts[i].images[
                        j].image_name = f'assets/community_post_images/{posts[i].images[j].image_name}'

            else:
                s = []
                s = f'defaults/communityDefault.jpg'
                posts[i].default_image = s

            posts[i].owner.profile_picture = profile_pic

        return posts

    else:
        pevId = ''
        print(len(posts.owner.profile_picture))
        print(pevId)
        if len(posts.owner.profile_picture) == 0 and pevId != posts.owner.id:
            posts.owner.profile_picture = f"defaults/user.jpg"
            pevId = posts.owner.id
        else:
            posts.owner.profile_picture = f"profiles/user/{posts.owner.profile_picture}"
            pevId = posts.owner.id

        if len(posts.images) > 0:
            for j in range(len(posts.images)):
                posts.images[j].image_name = f'assets/community_post_images/{posts.images[j].image_name}'

        else:
            s = []
            s = f'defaults/communityDefault.jpg'
            posts.default_image = s

        return posts


def getDefaultsImagesInSpecific(posts):
    if hasattr(posts, '__len__'):
        pevId = ''
        for i in range(len(posts)):
            if len(posts[i].comment) == 0:
                if len(posts[i].owner.profile_picture) == 0 and pevId != posts[i].owner.id:
                    profile_pic = f"defaults/user.jpg"
                    pevId = posts[i].owner.id
                else:
                    if pevId != posts[i].owner.id:
                        profile_pic = f"assets/profiles/user/{posts[i].owner.profile_picture}"
                        pevId = posts[i].owner.id

            if len(posts[i].images) > 0:
                for j in range(len(posts[i].images)):
                    posts[i].images[
                        j].image_name = f'assets/community_post_images/{posts[i].images[j].image_name}'

            else:
                s = []
                s = f'defaults/communityDefault.jpg'
                posts[i].default_image = s

            posts[i].owner.profile_picture = profile_pic

        return posts

    else:
        pevId = ''
        if len(posts.comment) == 0:
            if len(posts.owner.profile_picture) == 0 and pevId != posts.owner.id:
                posts.owner.profile_picture = f"defaults/user.jpg"
                pevId = posts.owner.id
            else:
                posts.owner.profile_picture = f"assets/profiles/user/{posts.owner.profile_picture}"
                pevId = posts.owner.id

        if len(posts.images) > 0:
            for j in range(len(posts.images)):
                posts.images[j].image_name = f'assets/community_post_images/{posts.images[j].image_name}'

        else:
            s = []
            s = f'defaults/communityDefault.jpg'
            posts.default_image = s

        return posts
