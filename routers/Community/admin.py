from fastapi import APIRouter, Depends
from repository.Community.adminAuth import adminCreateAccount
from sqlalchemy.orm import session
from database import get_db
from schemas.admin_schemas import CreateAdmin


router = APIRouter()

# create admin


@router.post('/admin/signup', tags=["Admin Auth"])
def adminAccountCreate(request: CreateAdmin, db: session = Depends(get_db)):
    return adminCreateAccount(request, db)

# login admin
# update admin
# show admin details
