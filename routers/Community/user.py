from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import session
from database import get_db
from oauth2 import get_current_plantUser
from repository.Community.userAuth import changedUserPassword, createNewUserAccount, getUserdDetailsUsingToken, loginUser, updateProfileDetails, uploadProfilePicture
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

# user details using token


@router.get('/getdetails')
def getDetails(db: session = Depends(get_db), current_user: loginUser = Depends(get_current_plantUser)):
    return getUserdDetailsUsingToken(db, current_user)


# update user profile
@router.put('/updateprofile/{id}', response_model=user_schemas.ProfileUpdate)
def updateUserProfile(id: int, request: user_schemas.ProfileUpdate, db: session = Depends(get_db), new_current_user: loginUser = Depends(get_current_plantUser)):
    return updateProfileDetails(id, request, db)


@router.post('/uploadprofilepic', response_model=user_schemas.User)
def updateProfilePic(db: session = Depends(get_db), current_user: loginUser = Depends(get_current_plantUser), file: UploadFile = File(..., media_type='image/jpeg')):
    return uploadProfilePicture(db, current_user, file)

# changed password


@router.put('/updatepassword/{id}')
def changedPassword(id: int, request: user_schemas.UpdatePassword, db: session = Depends(get_db), new_current_user: loginUser = Depends(get_current_plantUser)):
    return changedUserPassword(id, request, db)

# update profile picture
