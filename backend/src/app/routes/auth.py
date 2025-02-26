from fastapi import APIRouter, HTTPException, status

from src.app.schemas.schemas import UserCreate, UserResponse, GetUserData
from src.app.utils.users_validation import UserValidation
from src.app.utils.hashing import Hash
from src.database import user_collections

auth_routes = APIRouter(prefix="/auth")


@auth_routes.post(
    "/user/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def user_signup(user_create: UserCreate):
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
        user_dict = user_create.model_dump()
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
        ),
    )
    user_response_dict = user_response.model_dump()
    return user_response_dict

@auth_routes.post("/user/login", status_code=status.HTTP_200_OK)
async def login():
    ...
