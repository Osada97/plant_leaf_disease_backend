from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from oauth2 import get_current_user
from repository.Community.adminAuth import adminApprovePost, adminCreateAccount, adminDisapprovePost, adminGetAllPosts, adminGetApprovedPosts, adminGetDisapprovedPosts, adminLoginToAccount, adminRemoveComments, adminRemovePosts, adminUpdateAccountDetails, adminUpdatePassword, adminUploadProfilePicture, getAdminDetails
from sqlalchemy.orm import session
from database import get_db
from schemas.admin_schemas import AdminGetPosts, AdminUpdate, AdminUpdatePassword, CreateAdmin,  Admin, Login

router = APIRouter(
    tags=["Admin Auth"],
    prefix='/admin'
)

# create admin


@router.post('/signup')
def adminAccountCreate(request: CreateAdmin, db: session = Depends(get_db)):
    return adminCreateAccount(request, db)

# login admin


@router.post('/login')
def adminLoginAccount(request: Login, db: session = Depends(get_db)):
    return adminLoginToAccount(request, db)

# logout admin

# get admin details


@router.get('/getdetails')
def getDetails(db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return getAdminDetails(db, current_user)

# update admin


# admin upload profile picture
@router.put('/updatedetails/{id}', response_model=Admin)
def adminUpdateAccount(id: int, request: AdminUpdate, db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminUpdateAccountDetails(id, request, db)


# update admin password
@router.put('/updatepassword', response_model=Admin)
def adminUpdateNewPassword(request: AdminUpdatePassword, db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminUpdatePassword(request, db, current_user)

# adding image to admin


@router.post('/uploadprofilepic', response_model=Admin)
def admingUploadImage(db: session = Depends(get_db), current_user: Login = Depends(get_current_user), file: UploadFile = File(..., media_type='image/jpeg')):
    return adminUploadProfilePicture(db, current_user, file)

# admin get all post


@router.get('/getpost', response_model=List[AdminGetPosts])
def adminGetPost(db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminGetAllPosts(db)

# admin get approved post


@router.get('/getapprovepost', response_model=List[AdminGetPosts])
def adminGetApprovedPost(db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminGetApprovedPosts(db)
# admin get unapproved post


@router.get('/getdisapprovepost', response_model=List[AdminGetPosts])
def adminGetDispprovedPost(db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminGetDisapprovedPosts(db)

# admin approve post


@router.post('/approvepost/{id}')
def adminApprove(id: int,  db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminApprovePost(id, db)

# admin disapprove post


@router.post('/disapprovepost/{id}')
def admminDisapprove(id: int,  db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminDisapprovePost(id, db)

# admin remove post


@router.delete('/removepost/{id}')
def adminRemovePost(id: int,  db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminRemovePosts(id, db)
# admin remove comment in specific post


@router.delete('/removecomment/{id}')
def adminRemoveComment(id: int,  db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminRemoveComments(id, db)
