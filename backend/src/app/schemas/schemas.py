from datetime import datetime, timezone
from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None
    is_online: Optional[bool] = False


class UserCreate(UserBase):
    password: str
    confirm_password: Optional[str] = None


class GetUserData(BaseModel):
    id: str  # MongoDB ObjectId as string
    username: str
    email: str
    created_at: datetime
    is_online: bool


class UserResponse(BaseModel):
    msg: Optional[str] = None
    data: GetUserData

class LoginRequest(BaseModel):
    username_or_email: Union[EmailStr, str]
    password: str

class LoginResponse(UserResponse):
    access_token: str
