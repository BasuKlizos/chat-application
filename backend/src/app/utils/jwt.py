from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class JWTAuth:
    """JWT Authentication Class"""

    JWT_SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    @classmethod
    def generate_access_token(cls, user_data: dict):
        """Generate access token"""
        expire = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {
            "sub": str(user_data["_id"]),
            "username": user_data["username"],
            "iat": datetime.now(timezone.utc),
            "exp": expire,
            "token_type": "access",
        }
        return jwt.encode(payload, cls.JWT_SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def verify_token(cls, token: str = Depends(oauth2_scheme)):
        """Verify token"""
        try:
            payload = jwt.decode(token, cls.JWT_SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError as e:
            print(f"JWTError encountered: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error encountered: {e}")
            return None

    # @classmethod
    # def get_current_user(cls, token: str = Depends(oauth2_scheme)):
    #     try:
    #         payload = jwt.decode(token, cls.JWT_SECRET_KEY,
    #           algorithms=[cls.ALGORITHM])
    #         username = payload.get("username")
    #         if not username:
    #             raise HTTPException(status_code=401, detail="Username not found")
    #         return username
    #     except JWTError:
    #         raise HTTPException(status_code=401, detail="Token is invalid or
    #                                                               expired.")
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=500,
    #             detail=f"An error occurred while decoding the token: {e}",
    #         )
