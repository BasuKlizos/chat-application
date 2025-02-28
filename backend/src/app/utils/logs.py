import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# example of format :
# 2024-02-28 12:34:56 - INFO - Successfully fetched chat history for users user123 and user456
# 2024-02-28 12:35:12 - ERROR - Error fetching chat history for users user789 and user101: Database connection error
