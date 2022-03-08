from typing import Optional
from pydantic import BaseModel, Field


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


class AdminUpdatePassword(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
