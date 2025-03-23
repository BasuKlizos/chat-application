import logging

from fastapi import WebSocket, Request
from redis.asyncio import Redis


def get_redis_client_ws(websocket: WebSocket) -> Redis:
    """Retrieves the Redis client instance from the WebSocket's application state.

    This function accesses the application state of the provided WebSocket
    to get the initialized Redis client. It raises a RuntimeError if the
    client is not found.

    Args:
        websocket: The WebSocket from which to retrieve the Redis client.

    Returns:
        The initialized Redis client instance.

    Raises:
        RuntimeError: If the Redis client is not initialized in the app state.
    """
    redis_client = websocket.app.state.redis_client
    if not redis_client:
        raise RuntimeError("Redis client is not initialized!")

    # print("Redis client successfully retrieved.")
    logging.info("Redis client successfully retrieved.")
    return redis_client


def get_redis_client_http(request: Request) -> Redis:
    redis_client = request.app.state.redis_client
    if not redis_client:
        raise RuntimeError("Redis client is not initialized!")
    return redis_client
