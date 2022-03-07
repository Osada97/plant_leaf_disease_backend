from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from repository.Community.adminAuth import adminCreateAccount, adminLoginToAccount
from sqlalchemy.orm import session
from database import get_db
from schemas.admin_schemas import CreateAdmin, Login


router = APIRouter(
    tags=["Admin Auth"]
)

# create admin


@router.post('/admin/signup')
def adminAccountCreate(request: CreateAdmin, db: session = Depends(get_db)):
    return adminCreateAccount(request, db)

# login admin


@router.post('/admin/login')
def adminLoginAccount(request: OAuth2PasswordRequestForm = Depends(), db: session = Depends(get_db)):
    return adminLoginToAccount(request, db)

# logout admin
# update admin
# show admin details
