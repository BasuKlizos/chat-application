from bson.objectid import ObjectId

from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse

from src.app.models.message_models import Message
from src.database import chat_collections

chat_routes = APIRouter(prefix="/chat")


@chat_routes.get("/get-chats/{user1_id}/{user2_id}", status_code=status.HTTP_200_OK)
async def get_chat_history(user1_id: str, user2_id: str):
    try:
        # print(f"Fetching chat history for: {user1_id} <-> {user2_id}")

        chat_history = await Message.get_chat_history(user1_id, user2_id)
        # print(chat_history)
        if not  chat_history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat History not found."
            )

        return JSONResponse(content={"messages": chat_history})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the chat history: {str(e)}",
        )
