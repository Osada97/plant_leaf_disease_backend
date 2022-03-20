import models
import os
from fastapi import HTTPException, status
from JWTtoken import create_access_token
from env import Environment
from repository.Community.defaults import Defaults
from schemas import user_schemas
from sqlalchemy.orm import session
from repository.Community.hashing import Hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError

# create account


def createNewUserAccount(request: user_schemas.User, db: session):
    # check username is already exists
    user_exists = db.query(models.User).filter(models.User.username ==
                                               request.username).first()

    email_exists = db.query(models.User).filter(models.User.email ==
                                                request.email).first()

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username is already exits")

    elif email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email is already exits")

    else:
        new_user = models.User(first_name=request.first_name, last_name=request.last_name, username=request.username, email=request.email,
                               phone_number=request.phone_number, location=request.location, password=Hash.bcrypt(request.password), profile_picture=Defaults.setDefaultImage(request, 'user'))

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {'details': f'{new_user.username} Is Created'}

        except SQLAlchemyError as e:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Somthing Went Wrong")

# login user


def loginUser(request: user_schemas.UserLogin, db: session):
    user = db.query(models.User).filter(
        models.User.username == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")

    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "userType": "user"})
    return {"access_token": access_token, "token_type": "bearer", "details": {"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "user name": user.username, "location": user.location, "profile picture": Defaults.getDefaultImage(user, 'user')}}

# update profile details


def updateProfileDetails(id: int, request: user_schemas.ProfileUpdate,  db: session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    user.first_name = request.first_name
    user.last_name = request.last_name
    user.username = request.username
    user.email = request.email
    user.phone_number = request.phone_number
    user.location = request.location
    user.profile_picture = Defaults.setDefaultImage(user, 'user')

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# changed password


def changedUserPassword(id: int, request: user_schemas.UpdatePassword,  db: session):
    user = db.query(models.User).filter(models.User.id == id).first()

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

# default image


def getPostImage(post):
    for i in range(len(post)):
        new_post = list(post)
        if len(new_post[i].images) > 0:
            for j in range(len(new_post[i].images)):
                new_post[i].images[j].image_name = f'{Environment.getBaseEnv()}/assets/community_post_images/{post[i].images[j].image_name}'

        else:
            s = []
            s = list(new_post[i].images)
            s.append(
                {'default_image': f'{Environment.getBaseEnv()}/assets/community_post_images/asd'})
            new_post[i].image = s

    return new_post
