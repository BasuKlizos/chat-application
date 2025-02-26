from fastapi import APIRouter, HTTPException, status

from src.database import user_collections

user_routes = APIRouter(prefix="/user")


@user_routes.get("/get-users", status_code=status.HTTP_200_OK)
async def get_all_users():
    try:
        cursor_users = user_collections.find({}, {"_id": 0, "password": 0})
        users_list = await cursor_users.to_list()
        return {"users": users_list, "status": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}",
        )
