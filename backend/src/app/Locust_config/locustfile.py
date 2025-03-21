import json
import random
import logging
from pymongo import MongoClient
from locust import User, task, between

from websocket import create_connection

# from src.database import user_collections


client = MongoClient("mongodb://mongodb:27017/")
db = client["chat-application-db"]
user_collections = db["users"]

existing_users_count = user_collections.count_documents({})
if existing_users_count < 1000:
    users_to_create = 1000 - existing_users_count
    new_users = [
        {
            "username": f"user{i}",
            "email": f"user{i}@example.com",
            "password": "123",
            "confirm_password": "123",
        }
        for i in range(existing_users_count, 1000)
    ]
    user_collections.insert_many(new_users)
    logging.info(f"Added {users_to_create} new users.")

user_ids = [str(user["_id"]) for user in user_collections.find({}, {"_id": 1})]

if len(user_ids) < 2:
    raise ValueError("Not enough users for WebSocket testing.")


class WebSocketLocust(User):
    """Simulates WebSocket user behavior for load testing."""

    wait_time = between(1, 5)

    def on_start(self):
        """Initialize WebSocket connection."""
        self.current_id = random.choice(user_ids)
        self.selected_user_id = random.choice(
            [uid for uid in user_ids if uid != self.current_id]
        )
        self.ws_url = f"ws://backend:8000/ws/{self.current_id}"

        try:
            self.ws = create_connection(self.ws_url)
            logging.info(f"Connected: {self.ws_url}")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            self.ws = None

    def on_stop(self):
        """Close WebSocket connection."""
        if self.ws:
            self.ws.close()
            logging.info("Connection closed")

    @task
    def send_message(self):
        """Send and receive a WebSocket message."""
        if not self.ws:
            logging.error("No WebSocket connection.")
            return

        # message = {
        #     "text": "Hello from WebSocket load test.",
        #     "sender_id": self.current_id,
        #     "receiver_id": self.selected_user_id,
        # }
        msg_payload = f"{self.current_id}:{self.selected_user_id}:{'Hello from WebSocket load test.'}"

        try:
            self.ws.send(json.dumps(msg_payload))
            logging.info(f"Sent: {msg_payload}")
            response = self.ws.recv()
            logging.info(f"Received: {response}")
        except Exception as e:
            logging.error(f"Message error: {e}")


# # locust -f locustfile.py  --headless -u 10 -r 2 --host ws://localhost:8000
