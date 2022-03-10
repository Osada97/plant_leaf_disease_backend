from pydantic import BaseModel, Field
from datetime import datetime


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
    userId: int

    class Config():
        orm_mode = True
