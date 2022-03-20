from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from schemas.community_schemas import PostImages


class CreateAdmin(BaseModel):
    username: str = Field(..., min_length=1, max_length=155)
    password: str = Field(..., min_length=6)
    profile_picture: Optional[str] = None


class Login(BaseModel):
    username: str = Field(..., min_length=1, max_length=155)
    password: str = Field(..., min_length=6)


class Admin(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=155)
    profile_picture: Optional[str] = None

    class Config():
        orm_mode = True


class AdminUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=155)

    class Config():
        orm_mode = True


class AdminUpdatePassword(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)


class AdminGetPosts(BaseModel):
    id: int
    post_title: str
    description: str
    down_vote_count: int
    userId: int
    post_date: datetime
    up_vote_count: int
    is_approve: bool
    images: List[PostImages] = []
    image: Optional[List] = []

    class Config():
        orm_mode = True
