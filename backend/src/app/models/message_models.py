import json
import time

from datetime import datetime, timezone
from bson.objectid import ObjectId
from redis.asyncio import Redis
from dateutil import parser

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
    async def fetch_chat_history(user1_id: str, user2_id: str, redis: Redis):

        sorted_ids = sorted([user1_id, user2_id])
        conversation_key = f"chat_history:{sorted_ids[0]}:{sorted_ids[1]}"

        cached_messages = await redis.zrange(conversation_key, 0, -1)
        if cached_messages:
            print("Cache hit!")
            chat_list = [json.loads(msg) for msg in cached_messages]
            return chat_list

        print("Cache miss! Fetching from DB...")

        # If the cache is empty, query the database.
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
        # print(f"Fetched Messages: {chat_list}")
        serialized_chat = Serialization.serialize_list(chat_list)

        for message in serialized_chat:
            ts = message.get("timestamp")
            if isinstance(ts, str):
                try:
                    ts_float = parser.parse(ts).timestamp()
                except Exception:
                    ts_float = time.time()
            elif isinstance(ts, datetime):
                ts_float = ts.timestamp()
            else:
                ts_float = time.time()
            await redis.zadd(conversation_key, {json.dumps(message): ts_float})

        await redis.expire(conversation_key, 86400)  # set an expiration (1 days).
        
        return serialized_chat
