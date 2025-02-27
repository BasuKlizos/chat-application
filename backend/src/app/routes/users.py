from fastapi import APIRouter, Depends, HTTPException
from src.database import user_collections
from src.app.utils.jwt import JWTAuth

user_routes = APIRouter(prefix="/user")

@user_routes.get("/get-users")
async def get_all_users(token_payload: dict = Depends(JWTAuth.verify_token)):
    try:
        # print("Token Payload:", token_payload)
        
        users = user_collections.find({}, {"_id": 1, "username": 1, "is_online": 1})
        
        users_list = []
        async for user in users:
            users_list.append({
                "user_id": str(user["_id"]),
                "username": user.get("username", "Unknown"),
                "is_online": user.get("is_online", False),
            })
        
        if not users_list:
            raise HTTPException(status_code=404, detail="No users found")

        return {"users": users_list, "status": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
