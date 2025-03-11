from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from src.app.models.message_models import Message
from src.app.utils.redis_dependencies import get_redis_client_http

chat_routes = APIRouter(prefix="/chat")


@chat_routes.get("/get-chats/{user1_id}/{user2_id}", status_code=status.HTTP_200_OK)
async def get_chat_history(
    user1_id: str, user2_id: str, redis: Redis = Depends(get_redis_client_http)
):
    try:
        # print(f"Fetching chat history for: {user1_id} <-> {user2_id}")

        chat_history = await Message.fetch_chat_history(user1_id, user2_id, redis)
        # print("Successfully fetched messages from db:")
        # task = MessageTasks.fetch_chats.delay(user1_id, user2_id)
        # chat_history = task.get(timeout=10)
        # print("Successfully fetched messages using Celery task:")
        # print(chat_history)

        if not chat_history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat History not found."
            )

        print("Successfully fetched messages using Redis cache (or DB fallback):")

        return JSONResponse(content={"messages": chat_history})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the chat history: {str(e)}",
        )
