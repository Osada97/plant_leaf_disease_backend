from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from database import get_db
from oauth2 import get_current_plantUser
from repository.Community.userAuth import changedUserPassword, createNewUserAccount, loginUser, updateProfileDetails
from schemas import user_schemas

router = APIRouter(
    tags=["User Auth"],
    prefix='/user'
)


# create user
@router.post('/createaccount')
def createUserAccount(request: user_schemas.User, db: session = Depends(get_db)):
    return createNewUserAccount(request, db)


# login user
@router.post('/login')
def loginAccount(request: user_schemas.UserLogin, db: session = Depends(get_db)):
    return loginUser(request, db)


# update user profile
@router.put('/updateprofile/{id}', response_model=user_schemas.ProfileUpdate)
def updateUserProfile(id: int, request: user_schemas.ProfileUpdate, db: session = Depends(get_db), new_current_user: loginUser = Depends(get_current_plantUser)):
    return updateProfileDetails(id, request, db)

# changed password


@router.put('/updatepassword/{id}')
def changedPassword(id: int, request: user_schemas.UpdatePassword, db: session = Depends(get_db), new_current_user: loginUser = Depends(get_current_plantUser)):
    return changedUserPassword(id, request, db)
