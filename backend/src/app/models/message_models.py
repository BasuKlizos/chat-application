import json
import time

from datetime import datetime, timezone
from redis.asyncio import Redis
from dateutil import parser

from src.database import chat_collections
from src.app.utils.serialization import Serialization

# from src.app.utils.task_queue import broker


class Message:
    """Handles message-related operations, including saving, fetching, and caching.

    This class provides static methods for interacting with message data,
    both in the database and in a Redis cache.
    """

    @staticmethod
    async def save_messaage(sender_id: str, receiver_id: str, message: str):
        """Saves a message to the database.

        Args:
            sender_id: The ID of the sender.
            receiver_id: The ID of the receiver.
            message: The message content.
        """
        chat_data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "timestamp": datetime.now(timezone.utc),
        }

        await chat_collections.insert_one(chat_data)

    # @staticmethod
    # @broker.task
    # async def queue_message(sender_id: str, receiver_id: str, message: str):
    #     try:
    #         await Message.save_messaage(sender_id, receiver_id, message)
    #     except Exception as e:
    #         print(f"Error storing message: {e}")

    @staticmethod
    async def fetch_chat_history(user1_id: str, user2_id: str, redis: Redis):
        """Fetches chat history between two users, utilizing a Redis cache.

        Args:
            user1_id: The ID of the first user.
            user2_id: The ID of the second user.
            redis: The Redis client instance.

        Returns:
            A list of chat messages.
        """

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

    @staticmethod
    async def cache_new_message(
        user1_id: str, user2_id: str, message: dict, redis: Redis
    ):
        """Caches a new message in Redis.

        Args:
            user1_id: The ID of the first user.
            user2_id: The ID of the second user.
            message: The message data to cache.
            redis: The Redis client instance.
        """
        sorted_ids = sorted([user1_id, user2_id])
        conversation_key = f"chat_history:{sorted_ids[0]}:{sorted_ids[1]}"

        message_copy = message.copy()

        #  Timestamp JSON-serializable format (ISO string)
        ts = message_copy.get("timestamp")
        ts_float = ts.timestamp() if isinstance(ts, datetime) else time.time()

        message_copy["timestamp"] = ts.isoformat()
        try:
            await redis.zadd(conversation_key, {json.dumps(message_copy): ts_float})
            await redis.expire(conversation_key, 86400)
        except Exception as e:
            print(f"[Redis Error] Failed to cache message: {e}")

       
        # if isinstance(ts, datetime):
        #     message_copy["timestamp"] = ts.isoformat()
        # elif isinstance(ts, str):
        #     try:

        #         message_copy["timestamp"] = parser.parse(ts).isoformat()
        #     except Exception:

        #         pass

        # #  numeric score using the original timestamp value.
        # if isinstance(ts, str):
        #     try:
        #         ts_float = parser.parse(ts).timestamp()
        #     except Exception:
        #         ts_float = time.time()
        # elif isinstance(ts, datetime):
        #     ts_float = ts.timestamp()
        # else:
        #     ts_float = time.time()

        # await redis.zadd(conversation_key, {json.dumps(message_copy): ts_float})

        # await redis.expire(conversation_key, 86400)

    # @staticmethod
    # async def make_user_offile(user_id: str): ...
