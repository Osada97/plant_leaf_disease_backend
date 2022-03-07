from sqlalchemy.orm import Session
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
