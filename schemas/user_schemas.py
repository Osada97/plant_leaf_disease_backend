from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=155)
    last_name: str = Field(..., min_length=1, max_length=155)
    username: str = Field(..., min_length=1, max_length=155)
    email: str = Field(..., min_length=1, max_length=155)
    phone_number: str = Field(..., min_length=1, max_length=35)
    location: str = Field(..., min_length=1, max_length=155)
    password: str = Field(..., min_length=1)
    profile_picture:  Optional[str] = None


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=155)
    password: str = Field(..., min_length=1)
