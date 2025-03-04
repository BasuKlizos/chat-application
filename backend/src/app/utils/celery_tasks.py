import asyncio
from asgiref.sync import async_to_sync

from src.app.celery.celery_worker import celery_app
from src.app.models.message_models import Message


class MessageTasks:
    @staticmethod
    @celery_app.task(name="Store chats to db", ignore_result=True)
    def store_messages(sender_id: str, receiver_id: str, message: str):
        from eventlet import greenthread
        greenthread.spawn_n(asyncio.run, Message.save_messaage(sender_id, receiver_id, message))

    # @celery_app.task(name="Store chats to db")
    # def store_messages(sender_id: str, receiver_id: str, message: str):
    #     # return asyncio.run(Message.save_messaage(sender_id, receiver_id, message))
    #     # return async_to_sync(Message.save_messaage)(sender_id, receiver_id, message)
    #     loop = asyncio.new_event_loop()
    #     try:
    #         asyncio.set_event_loop(loop)
    #         result = loop.run_until_complete(
    #             Message.save_messaage(sender_id, receiver_id, message)
    #         )
    #     finally:
    #         loop.close()
    #         asyncio.set_event_loop(None)
    #     return result

    # @staticmethod
    # @celery_app.task(name="fetch-chats-from-db")
    # def fetch_chats(user1_id, user2_id):
    #     # return asyncio.run(Message.fetch_chat_history(user1_id, user2_id))
    #     return async_to_sync(Message.fetch_chat_history)(user1_id, user2_id)
