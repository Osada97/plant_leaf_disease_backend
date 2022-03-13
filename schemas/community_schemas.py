from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from schemas.user_schemas import GetUser

# create and update community post


class CommunityPost(BaseModel):
    post_title: str = Field(..., min_length=1, max_length=155)
    description: str = Field(..., min_length=1, max_length=155)

    class Config():
        orm_mode = True


class ShowCommunityPost(CommunityPost):
    post_date: datetime
    up_vote_count: int
    is_approve: bool
    down_vote_count: int
    owner: GetUser
    isUser: Optional[bool] = False

    class Config():
        orm_mode = True


class Comment(BaseModel):
    comment: str
    comment_date: datetime
    down_vote_count: int
    up_vote_count: int
    isUser: Optional[bool] = False
    user: GetUser

    class Config():
        orm_mode = True


class CreateComment(BaseModel):
    comment: str = Field(..., min_length=1)


class ShowComment(CreateComment):
    comment_date: datetime

    class Config():
        orm_mode = True
