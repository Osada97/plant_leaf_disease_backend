from fastapi import HTTPException, status
from JWTtoken import create_access_token
from schemas import user_schemas
from sqlalchemy.orm import session
from repository.Community.hashing import Hash
from sqlalchemy.exc import SQLAlchemyError
import models


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
                               phone_number=request.phone_number, location=request.location, password=Hash.bcrypt(request.password), profile_picture=request.profile_picture)

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {'details': f'{new_user.username} Is Created'}

        except SQLAlchemyError as e:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Somthing Went Wrong")


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
        data={"sub": user.username, "userType": "user"})
    return {"access_token": access_token, "token_type": "bearer", "details": {"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "user name": user.username, "location": user.location, "profile picture": user.profile_picture}}
