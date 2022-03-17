from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from schemas.user_schemas import GetUser

# create and update community post


class CommunityPost(BaseModel):
    post_title: str = Field(..., min_length=1, max_length=155)
    description: str = Field(..., min_length=1, max_length=155)

    class Config():
        orm_mode = True


class CommunityPostImage(BaseModel):
    id: int
    image_name: str

    class Config():
        orm_mode = True


class ShowCommunityPost(CommunityPost):
    id: int
    post_date: datetime
    up_vote_count: int
    is_approve: bool
    down_vote_count: int
    owner: GetUser
    images: List[CommunityPostImage] = []

    class Config():
        orm_mode = True


class PostBool(ShowCommunityPost):
    isUser: Optional[bool] = False
    isUpVoted: Optional[bool] = False
    isDownVoted: Optional[bool] = False

    class Config():
        orm_mode = True


class ShowCommunityPostOnId(CommunityPost):
    post_date: datetime
    up_vote_count: int
    is_approve: bool
    down_vote_count: int
    owner: GetUser
    images: List[CommunityPostImage] = []

    class Config():
        orm_mode = True


class CommentImage(BaseModel):
    id: int
    image_name: str


class Comment(BaseModel):
    comment: str
    comment_date: datetime
    down_vote_count: int
    up_vote_count: int
    isUser: Optional[bool] = False
    isUpVoted: Optional[bool] = False
    isDownVoted: Optional[bool] = False
    user: GetUser
    image: List[CommentImage] = []

    class Config():
        orm_mode = True


class CreateComment(BaseModel):
    comment: str = Field(..., min_length=1)


class ShowComment(CreateComment):
    id: int
    comment_date: datetime

    class Config():
        orm_mode = True


class PostImages(BaseModel):
    id: int
    image_name: str

    class Config():
        orm_mode = True
