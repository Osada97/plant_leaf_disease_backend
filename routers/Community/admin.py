from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from oauth2 import get_current_user
from repository.Community.adminAuth import adminCreateAccount, adminLoginToAccount, adminUpdateAccountDetails, adminUpdatePassword
from sqlalchemy.orm import session
from database import get_db
from schemas.admin_schemas import AdminUpdatePassword, CreateAdmin,  Admin, Login


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
def adminLoginAccount(request: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    return adminLoginToAccount(request, db)

# logout admin
# update admin


# admin upload profile picture
@router.put('/updatedetails/{id}', response_model=Admin)
def adminUpdateAccount(id: int, request: Admin, db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminUpdateAccountDetails(id, request, db)


# update admin password
@router.put('/updatepassword/{id}', response_model=Admin)
def adminUpdateNewPassword(id: int, request: AdminUpdatePassword, db: session = Depends(get_db), current_user: Login = Depends(get_current_user)):
    return adminUpdatePassword(id, request, db)

# admin approve post
# admin remove post before approve
# admin remove post
# admin remove comment in specific post
