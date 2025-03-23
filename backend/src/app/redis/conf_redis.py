import sys
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis, ConnectionPool

from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the lifespan of the Redis client within the FastAPI application.

    This asynchronous context manager initializes a Redis client and stores it
    in the application state. It checks the connection and closes the client
    when the application shuts down.

    Args:
        app: The FastAPI application instance.
    """
    pool = ConnectionPool.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=15000,
        decode_responses=True,
    )
    app.state.redis_client = Redis(connection_pool=pool)
    # app.state.redis_client = Redis(
    #     host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
    # )
    try:
        if not await app.state.redis_client.ping():
            # print("Redis is not running! Exiting application.")
            logging.error("Redis is not running! Exiting application.")
            sys.exit(1)

        # print("Redis connected!")
        logging.info("Redis connected!")
        yield

    finally:
        await app.state.redis_client.close()
        # print("Redis disconnected!")
        logging.info("Redis disconnected!")
