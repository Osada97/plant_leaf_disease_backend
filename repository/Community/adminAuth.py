from typing import List
from pydantic import parse_obj_as
import models
import os
import shutil
import time
from env import Environment
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from JWTtoken import create_access_token
from sqlalchemy.exc import IntegrityError
from repository.Community.defaults import Defaults
from repository.Community.hashing import Hash
from schemas import admin_schemas
from schemas.community_schemas import PostImages

# admin create account


def adminCreateAccount(request: admin_schemas.CreateAdmin, db: Session):

    new_admin = models.Admin(username=request.username,
                             password=Hash.bcrypt(request.password), profile_picture=Defaults.setDefaultImage(request, 'admin'))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"details": f"Admin {new_admin.username} {new_admin.id} is created"}

# admin login account


def adminLoginToAccount(request: admin_schemas.Login, db: Session):

    user = db.query(models.Admin).filter(
        models.Admin.username == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "userType": "admin"})
    return {"access_token": access_token, "token_type": "bearer", "details": {"id": user.id, "user name": user.username, "profile picture": Defaults.getDefaultImage(user, 'admin')}}

# get admin details


def getAdminDetails(db: Session, current_user):
    user = db.query(models.Admin).filter(
        models.Admin.id == current_user.id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    return {"id": user.id,  "user_name": user.username,  "profile_picture": Defaults.getDefaultImage(user, 'admin')}

# admin update account details


def adminUpdateAccountDetails(id: int, request: admin_schemas.Admin, db: Session):
    user = db.query(models.Admin).filter(
        models.Admin.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    user.username = request.username

    try:
        db.commit()
        db.refresh(user)
        user.profile_picture = Defaults.getDefaultImage(user, 'admin')
        return user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# admin update password


def adminUpdatePassword(request: admin_schemas.AdminUpdatePassword, db: Session, current_user):
    user = db.query(models.Admin).filter(
        models.Admin.id == current_user.id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(request.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")

    user.password = Hash.bcrypt(request.new_password)

    try:
        db.commit()
        db.refresh(user)
        return {"details": "Password Changed Successfully"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# admin upload profile picture


def adminUploadProfilePicture(db: Session, current_user, file):
    admin = db.query(models.Admin).filter(
        models.Admin.id == current_user.id).first()

    # check file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'{file.content_type} is invalid file type please upload jpeg and png files.')

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    path = './assets/profiles/admin'
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

    admin.profile_picture = filenames

    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)

        admin.profile_picture = Defaults.getDefaultImage(admin, 'admin')

        return admin
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'id {id} is not in the table please check the id and try again')


# admin get posts


def adminGetAllPosts(db: Session):
    posts = db.query(models.CommunityPost).all()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no posts")
    return getPostImage(posts)

# admin get approved posts


def adminGetApprovedPosts(db: Session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.is_approve == True).all()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no posts")

    return getPostImage(posts)
# admin get disapproved posts


def adminGetDisapprovedPosts(db: Session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.is_approve == False).all()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no posts")

    return getPostImage(posts)

# admin approve post


def adminApprovePost(id: int, db: Session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    if post.is_approve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Already approved post")

    post.is_approve = True

    try:
        db.commit()
        db.refresh(post)
        return {"details": "Post approved successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')
# admin disapprove


def adminDisapprovePost(id: int, db: Session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    if post.is_approve == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Already disapprove post")

    post.is_approve = False

    try:
        db.commit()
        db.refresh(post)
        return {"details": "Post disapprove successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# admin remove posts


def adminRemovePosts(id: int, db: Session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).delete(synchronize_session=False)
    db.commit()

    return {'details': f'Post {id} is Deleted'}

# admin remove comment


def adminRemoveComments(id: int, db: Session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    db.query(models.Comments).filter(
        models.Comments.id == id).delete(synchronize_session=False)
    db.commit()

    return {'details': f'Comment {id} is Deleted'}


def getPostImage(posts):
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
