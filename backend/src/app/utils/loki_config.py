# import logging
# from logging_loki import LokiHandler

# # Loki Server URL
# LOKI_URL =  "http://loki:3100/loki/api/v1/push"

# # Create Loki Handler
# loki_handler = LokiHandler(
#     url=LOKI_URL,
#     version="1",
#     tags={"app": "fastapi-websockets"},
# )

# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# loki_handler.setFormatter(formatter)

# # Configure the root logger
# root_logger = logging.getLogger()
# if not root_logger.hasHandlers():  # Avoid adding multiple handlers
#     root_logger.setLevel(logging.INFO)
#     root_logger.addHandler(loki_handler)

# uvicorn_logger = logging.getLogger("uvicorn")
# uvicorn_logger.setLevel(logging.INFO)
# uvicorn_logger.propagate = False  # Prevent duplicate logs
# if not uvicorn_logger.hasHandlers():
#     uvicorn_logger.addHandler(loki_handler)

# ws_logger = logging.getLogger("websocket")
# ws_logger.setLevel(logging.INFO)
# if not ws_logger.hasHandlers():
#     ws_logger.addHandler(loki_handler)


# #  Output Example
# # 2024-03-04T12:10:15Z - websocket - INFO - WebSocket CONNECTED: User 123
# # 2024-03-04T12:10:20Z - websocket - INFO - MESSAGE RECEIVED: User 123 → Hello!
