import os
import logging

from reactioner_client import ReActionerClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    client = ReActionerClient(
        token=os.environ.get("discord-token")
    )
    client.run(client.token)
