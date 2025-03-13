from fastapi import APIRouter, HTTPException, status, Depends
from bson.objectid import ObjectId

from src.app.schemas.schemas import (
    UserCreate,
    UserResponse,
    GetUserData,
    LoginRequest,
    LoginResponse,
)
from src.app.utils.users_validation import UserValidation
from src.app.utils.hashing import Hash
from src.database import user_collections
from src.app.utils.jwt import JWTAuth
from src.app.utils.metrics import USER_REGISTRATIONS

auth_routes = APIRouter(prefix="/auth")


@auth_routes.post(
    "/user/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def user_signup(user_create: UserCreate):
    """Handles user login requests.

    This endpoint verifies user credentials, updates their online status, and generates an access token.
    """
    # print("successfully user registered to db.")
    try:
        await UserValidation.is_user_exists(
            username=user_create.username, email=user_create.email
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User exists or validation falied: {str(e)}",
        )

    try:
        await UserValidation.is_password_matched(
            user_create.password, user_create.confirm_password
        )
        hashed_password = Hash.hash_password(user_create.password)
        user_create.password = hashed_password
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Password hashing failed: {str(e)}"
        )

    try:
        user_dict = user_create.model_dump(exclude={"confirm_password"})
        user_result = await user_collections.insert_one(user_dict)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting user: {str(e)}")

    user_response = UserResponse(
        msg="User created successfully",
        data=GetUserData(
            id=UserValidation.object_id_to_str(user_result.inserted_id),
            username=user_dict["username"],
            email=user_dict["email"],
            created_at=user_dict["created_at"],
            is_online=user_dict["is_online"],
        ),
    )
    user_response_dict = user_response.model_dump()

    USER_REGISTRATIONS.inc()

    return user_response_dict


@auth_routes.post(
    "/login", response_model=LoginResponse, status_code=status.HTTP_200_OK
)
async def login(user_login: LoginRequest):
    """Handles user login requests.

    This endpoint verifies user credentials, updates their online status, and generates an access token.
    """
    try:
        user = await UserValidation.get_user_by_email_or_username(
            user_login.username_or_email
        )
        # print("-------------------------------------------------------------------")
        # print(user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await UserValidation.verify_user_password(user["password"], user_login.password)

        await user_collections.update_one(
            {"_id": user["_id"]}, {"$set": {"is_online": True}}
        )

        access_token = JWTAuth.generate_access_token(user)

        login_user_response = LoginResponse(
            msg="User successfully Logged In",
            data=GetUserData(
                id=UserValidation.object_id_to_str(user["_id"]),
                username=user["username"],
                email=user["email"],
                created_at=user["created_at"],
                is_online=True,
            ),
            access_token=access_token,
        )
        login_user_response_dict = login_user_response.model_dump()

        return login_user_response_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_routes.post("/logout")
async def logout_user(token_payload: dict = Depends(JWTAuth.verify_token)):
    try:
        user_id = token_payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        result = await user_collections.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"is_online": False}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User logged out successfully", "status": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")
