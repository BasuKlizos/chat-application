# from locust import HttpUser, task, between
# from locust.contrib.fasthttp import FastHttpUser
# import random
# import string
# import asyncio
# import websockets
# import json

# class FastAPIUser(HttpUser):
#     wait_time = between(1, 3)
#     logged_in_users = []

#     def on_start(self):
#         self.user_data = self.signup()
#         if self.user_data:
#             self.login()

#     def random_string(self, length=8):
#         return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

#     def signup(self):
#         random_username = self.random_string()
#         user_payload = {
#             "username": random_username,
#             "email": f"{random_username}@example.com",
#             "password": "testpassword123",
#             "confirm_password": "testpassword123"
#         }

#         response = self.client.post("/auth/user/signup", json=user_payload)

#         if response.status_code == 201:
#             # print(f"Signed up user: {random_username}")
#             return {
#                 "username_or_email": user_payload["email"],
#                 "password": user_payload["password"]
#             }
#         else:
#             # print(f"Signup failed: {response.text}")
#             return None

#     @task
#     def login(self):
#         if self.user_data:
#             login_payload = {
#                 "username_or_email": self.user_data["username_or_email"],
#                 "password": self.user_data["password"]
#             }
#             response = self.client.post("/auth/login", json=login_payload)


#         if response.status_code == 200:
#             data = response.json()
#             self.user_id = data["data"]["id"]
#             self.access_token = data["access_token"]
#             self.ws_url = f"ws://127.0.0.1:8000/ws/{self.user_id}"

#             print(f"Login successful! WebSocket URL: {self.ws_url}")
#         else:
#             print(f"Login failed: {response.text}")

#         FastAPIUser.logged_in_users.append(self.user_id)

#     @task
#     def websocket_chat(self):
#         if hasattr(self, "ws_url"):
#             asyncio.run(self.ws_connect(self.ws_url))

#     async def ws_connect(self, ws_url):
#         try:
#             async with websockets.connect(ws_url) as websocket:
#                 print(f"WebSocket connected: {ws_url}")

#                 if len(FastAPIUser.logged_in_users) > 1:
#                     receiver_id = self.user_id
#                     while receiver_id == self.user_id:
#                         receiver_id = random.choice(FastAPIUser.logged_in_users)
#                 else:
#                     print("No other users online to chat with.")
#                     return
#                 random_message = self.random_message()
#                 msg_payload = f"{self.user_id}:{receiver_id}:{random_message}"

#                 await websocket.send(msg_payload)
#                 print(f"Sent: {msg_payload}")

#                 response = await websocket.recv()
#                 print(f"Received: {response}")

#         except Exception as e:
#             print(f"WebSocket error: {e}")

# def random_message(self):
#     """Generates a random message for chat testing."""
#     messages = [
#         "Hey there!",
#         "How’s it going?",
#         "What’s up?",
#         "Testing WebSockets!",
#         "This is a random chat message.",
#         "Hello from Locust!",
#         "Sending random messages for load testing.",
#         "FastAPI + WebSockets = Rocket",
#         "Let's see how this chat handles load!",
#         "Hello, world!"
#     ]
#     return random.choice(messages)


import json
import random
import logging
from pymongo import MongoClient
from locust import User, task

from websocket import create_connection

# from src.database import user_collections


client = MongoClient("mongodb://localhost:27017/")
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

    def on_start(self):
        """Initialize WebSocket connection."""
        self.current_id = random.choice(user_ids)
        self.selected_user_id = random.choice(
            [uid for uid in user_ids if uid != self.current_id]
        )
        self.ws_url = f"ws://127.0.0.1:8000/ws/{self.current_id}"

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
        msg_payload = f"""{self.current_id}\
            :{self.selected_user_id}:\
                {'Hello from WebSocket load test.'}"""

        try:
            self.ws.send(json.dumps(msg_payload))
            logging.info(f"Sent: {msg_payload}")
            response = self.ws.recv()
            logging.info(f"Received: {response}")
        except Exception as e:
            logging.error(f"Message error: {e}")


# # locust -f locustfile.py  --headless -u 10 -r 2 --host ws://localhost:8000
