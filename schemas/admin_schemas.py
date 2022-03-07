from typing import Optional
from pydantic import BaseModel, Field


class CreateAdmin(BaseModel):
    username: str = Field(..., min_length=1, max_length=155)
    password: str = Field(..., min_length=6)
    profile_picture: Optional[str] = None
