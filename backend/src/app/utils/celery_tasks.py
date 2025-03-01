import asyncio

from src.app.celery.celery_worker import celery_app
from src.app.models.message_models import Message


class MessageTasks:
    @staticmethod
    @celery_app.task(name="Store chats to db")
    def store_messages(sender_id: str, receiver_id: str, message: str):
        return asyncio.run(Message.save_messaage(sender_id, receiver_id, message))
