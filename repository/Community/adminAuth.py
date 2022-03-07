from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from JWTtoken import create_access_token
import models
from repository.Community.hashing import Hash
from schemas import admin_schemas


def adminCreateAccount(request: admin_schemas.CreateAdmin, db: Session):
    new_admin = models.Admin(username=request.username,
                             password=Hash.bcrypt(request.password), profile_picture=request.profile_picture)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"details": f"Admin {new_admin.username} {new_admin.id} is created"}


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
        data={"sub": user.username, "userType": "admin"})
    return {"access_token": access_token, "token_type": "bearer"}
