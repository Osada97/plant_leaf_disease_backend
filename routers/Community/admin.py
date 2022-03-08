from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from repository.Community.adminAuth import adminCreateAccount, adminLoginToAccount, adminUpdateAccountDetails
from sqlalchemy.orm import session
from database import get_db
from schemas.admin_schemas import CreateAdmin,  Admin


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
def adminUpdateAccount(id: int, request: Admin, db: session = Depends(get_db)):
    return adminUpdateAccountDetails(id, request, db)


# update admin password
@router.put('/updatepassword/{id}')
def adminUpdateNewPassword():
    pass
# show admin details
