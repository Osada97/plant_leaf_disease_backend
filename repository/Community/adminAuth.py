from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from JWTtoken import create_access_token
import models
from sqlalchemy.exc import IntegrityError
from repository.Community.hashing import Hash
from schemas import admin_schemas

# admin create account


def adminCreateAccount(request: admin_schemas.CreateAdmin, db: Session):
    new_admin = models.Admin(username=request.username,
                             password=Hash.bcrypt(request.password), profile_picture=request.profile_picture)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"details": f"Admin {new_admin.username} {new_admin.id} is created"}

# admin login account


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
        data={"sub": user.username, "id": user.id, "userType": "admin"})
    return {"access_token": access_token, "token_type": "bearer", "details": {"id": user.id, "user name": user.username, "profile picture": user.profile_picture}}

# admin update account details


def adminUpdateAccountDetails(id: int, request: admin_schemas.Admin, db: Session):
    user = db.query(models.Admin).filter(
        models.Admin.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    user.username = request.username
    user.profile_picture = request.profile_picture

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# admin update password


def adminUpdatePassword(id: int, request: admin_schemas.AdminUpdatePassword, db: Session):
    user = db.query(models.Admin).filter(models.Admin.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(request.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")

    user.password = Hash.bcrypt(request.new_password)

    try:
        db.commit()
        db.refresh(user)
        return {"details": "Password Changed Successfully"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# admin get posts


def adminGetAllPosts(db: Session):
    posts = db.query(models.CommunityPost).all()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no posts")

    return posts

# admin get approved posts


def adminGetApprovedPosts(db: Session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.is_approve == True).all()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no posts")

    return posts
# admin get disapproved posts


def adminGetDisapprovedPosts(db: Session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.is_approve == False).all()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no posts")

    return posts

# admin approve post


def adminApprovePost(id: int, db: Session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    if post.is_approve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Already approved post")

    post.is_approve = True

    try:
        db.commit()
        db.refresh(post)
        return {"details": "Post approved successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')
# admin disapprove


def adminDisapprovePost(id: int, db: Session):
    post = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    if post.is_approve == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Already disapprove post")

    post.is_approve = False

    try:
        db.commit()
        db.refresh(post)
        return {"details": "Post disapprove successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Somthing Went Wrong')

# admin remove posts


def adminRemovePosts(id: int, db: Session):
    posts = db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).first()

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    db.query(models.CommunityPost).filter(
        models.CommunityPost.id == id).delete(synchronize_session=False)
    db.commit()

    return {'details': f'Post {id} is Deleted'}

# admin remove comment


def adminRemoveComments(id: int, db: Session):
    comment = db.query(models.Comments).filter(
        models.Comments.id == id).first()

    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id")

    db.query(models.Comments).filter(
        models.Comments.id == id).delete(synchronize_session=False)
    db.commit()

    return {'details': f'Comment {id} is Deleted'}
