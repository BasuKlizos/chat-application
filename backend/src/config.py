import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    MONGO_URI: str = os.getenv("MONGO_URI")
    ALGORITHM: str = os.getenv("ALGORITHM")


settings = Settings()
