from bson.objectid import ObjectId

from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.database import user_collections


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserValidation:

    @classmethod
    async def is_user_exists(cls, username: str = None, email: str = None):
        if username:
            user_by_username = await user_collections.find_one({"username": username})
            if user_by_username:
                raise HTTPException(status_code=400, detail="Username already exists")
        if email:
            user_by_email = await user_collections.find_one({"email": email})
            if user_by_email:
                raise HTTPException(status_code=400, detail="Email already exists")

    @classmethod
    async def is_password_matched(cls, password: str, confirm_password: str):
        if password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Password and confirm-password do not match.",
            )

    @classmethod
    async def get_user_by_email_or_username(cls, email_or_username: str):
        user = await user_collections.find_one(
            {
                "$or": [
                    {"email": email_or_username},
                    {"username": email_or_username},
                ]
            }
        )

        if not user:
            raise HTTPException(status_code=404, detail="User Not found")
        return user

    @classmethod
    async def get_user_by_id(cls, user_id: str):
        user = await user_collections.find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")

    @classmethod
    async def verify_user_password(cls, hashed_password: str, password: str):

        if not pwd_context.verify(password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    @classmethod
    def object_id_to_str(cls, obj):
        return str(obj) if obj else None
