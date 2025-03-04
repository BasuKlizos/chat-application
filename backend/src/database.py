from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings

MONGO_URI = settings.MONGO_URI
# print(MONGO_URI, "====================================================")
client = AsyncIOMotorClient(MONGO_URI)
db = client["chat-application-db"]
user_collections = db["users"]
chat_collections = db["chats"]
