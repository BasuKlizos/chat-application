from bson.objectid import ObjectId

from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.database import user_collections


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserValidation:
    """Provides methods for validating user data and credentials.

    This class includes methods for checking user existence, password matching,
    retrieving users, and verifying passwords.
    """

    @classmethod
    async def is_user_exists(cls, username: str = None, email: str = None):
        """Checks if a user with the given username or email already exists.

        Args:
            username (str, optional): The username to check. Defaults to None.
            email (str, optional): The email to check. Defaults to None.

        Raises:
            HTTPException: If a user with the given username or email already exists.
        """
        if username:
            user_by_username = await user_collections.find_one({"username": username})
            if user_by_username:
                raise HTTPException(status_code=409, detail="Username already exists")
        if email:
            user_by_email = await user_collections.find_one({"email": email})
            if user_by_email:
                raise HTTPException(status_code=409, detail="Email already exists")

    @classmethod
    async def is_password_matched(cls, password: str, confirm_password: str):
        """Checks if the password and confirm password match.

        Args:
            password (str): The password.
            confirm_password (str): The confirm password.

        Raises:
            HTTPException: If the password and confirm password do not match.
        """
        if password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Password and confirm-password do not match.",
            )

    @classmethod
    async def get_user_by_email_or_username(cls, email_or_username: str):
        """Retrieves a user by their email or username.

        Args:
            email_or_username (str): The email or username.

        Returns:
            The user document.

        Raises:
            HTTPException: If the user is not found.
        """
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
        """Retrieves a user by their ID.

        Args:
            user_id (str): The user ID.

        Returns:
            The user document.

        Raises:
            HTTPException: If the user is not found.
        """
        user = await user_collections.find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")

    @classmethod
    async def verify_user_password(cls, hashed_password: str, password: str):
        """Verifies a user's password against a hashed password.

        Args:
            hashed_password (str): The hashed password.
            password (str): The password to verify.

        Raises:
            HTTPException: If the password does not match the hashed password.
        """

        if not pwd_context.verify(password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    @classmethod
    def object_id_to_str(cls, obj):
        """Converts an ObjectId to a string.

        Args:
            obj: The ObjectId.

        Returns:
            The string representation of the ObjectId, or None if the input is None.
        """
        return str(obj) if obj else None


# class UserValidation:

#     @classmethod
#     async def is_user_exists(cls, username: str = None, email: str = None):
#         if username:
#             user_by_username = await user_collections.find_one({"username": username})
#             if user_by_username:
#                 raise HTTPException(status_code=409, detail="Username already exists")
#         if email:
#             user_by_email = await user_collections.find_one({"email": email})
#             if user_by_email:
#                 raise HTTPException(status_code=409, detail="Email already exists")

#     @classmethod
#     async def is_password_matched(cls, password: str, confirm_password: str):
#         if password != confirm_password:
#             raise HTTPException(
#                 status_code=status.HTTP_406_NOT_ACCEPTABLE,
#                 detail="Password and confirm-password do not match.",
#             )

#     @classmethod
#     async def get_user_by_email_or_username(cls, email_or_username: str):
#         user = await user_collections.find_one(
#             {
#                 "$or": [
#                     {"email": email_or_username},
#                     {"username": email_or_username},
#                 ]
#             }
#         )

#         if not user:
#             raise HTTPException(status_code=404, detail="User Not found")
#         return user

#     @classmethod
#     async def get_user_by_id(cls, user_id: str):
#         user = await user_collections.find_one({"_id": ObjectId(user_id)})
#         if user:
#             return user
#         raise HTTPException(status_code=404, detail="User not found")

#     @classmethod
#     async def verify_user_password(cls, hashed_password: str, password: str):

#         if not pwd_context.verify(password, hashed_password):
#             raise HTTPException(status_code=401, detail="Invalid credentials")

#     @classmethod
#     def object_id_to_str(cls, obj):
#         return str(obj) if obj else None
