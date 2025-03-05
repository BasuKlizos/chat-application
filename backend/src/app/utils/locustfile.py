from locust import HttpUser, task, between
from locust.contrib.fasthttp import FastHttpUser
import random
import string
import asyncio
import websockets
import json

class FastAPIUser(HttpUser):
    wait_time = between(1, 3) 

    def on_start(self):
        self.user_data = self.signup()
        if self.user_data:
            self.login()

    def random_string(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def signup(self):
        random_username = self.random_string()
        user_payload = {
            "username": random_username,
            "email": f"{random_username}@example.com",
            "password": "testpassword123",
            "confirm_password": "testpassword123"
        }

        response = self.client.post("/auth/user/signup", json=user_payload)

        if response.status_code == 201:
            # print(f"Signed up user: {random_username}")
            return {
                "username_or_email": user_payload["email"],
                "password": user_payload["password"]
            }
        else:
            # print(f"Signup failed: {response.text}")
            return None

    @task
    def login(self):
        if self.user_data:
            login_payload = {
                "username_or_email": self.user_data["username_or_email"],
                "password": self.user_data["password"]
            }

        response = self.client.post("/auth/login", json=login_payload)

        if response.status_code == 200:
            data = response.json()
            self.user_id = data["data"]["id"]
            self.access_token = data["access_token"]
            self.ws_url = f"ws://127.0.0.1:8000/ws/{self.user_id}"
                
            print(f"Login successful! WebSocket URL: {self.ws_url}")
        else:
            print(f"Login failed: {response.text}")
    
    @task
    def websocket_chat(self):
        if hasattr(self, "ws_url"):
            asyncio.run(self.ws_connect(self.ws_url))

    async def ws_connect(self, ws_url):
        try:
            async with websockets.connect(ws_url) as websocket:
                print(f"WebSocket connected: {ws_url}")

                receiver_id = self.user_id
                random_message = self.random_message()
                msg_payload = f"{self.user_id}:{receiver_id}:{random_message}"

                await websocket.send(msg_payload)
                print(f"Sent: {msg_payload}")

                response = await websocket.recv()
                print(f"Received: {response}")

        except Exception as e:
            print(f"WebSocket error: {e}")
    
    def random_message(self):
        """Generates a random message for chat testing."""
        messages = [
            "Hey there!",
            "How’s it going?",
            "What’s up?",
            "Testing WebSockets!",
            "This is a random chat message.",
            "Hello from Locust!",
            "Sending random messages for load testing.",
            "FastAPI + WebSockets = Rocket",
            "Let's see how this chat handles load!",
            "Hello, world!"
        ]
        return random.choice(messages)