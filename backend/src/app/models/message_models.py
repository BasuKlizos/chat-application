from datetime import datetime, timezone
from bson.objectid import ObjectId

from src.database import chat_collections
from src.app.utils.serialization import Serialization


class Message:

    @staticmethod
    async def save_messaage(sender_id: str, receiver_id: str, message: str):
        chat_data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "timestamp": datetime.now(timezone.utc),
        }

        await chat_collections.insert_one(chat_data)

    @staticmethod
    async def get_chat_history(user1_id, user2_id):

        query = {
            "$or": [
                {"sender_id": user1_id, "receiver_id": user2_id},
                {"sender_id": user2_id, "receiver_id": user1_id},
            ]
        }

        chats_cursor = chat_collections.find(query).sort(
            [("timestamp", 1)]
        )  # assending order

        chat_list = await chats_cursor.to_list(length=None)
        print(f"Fetched Messages: {chat_list}")

        return Serialization.serialize_list(chat_list)
