import argparse
import asyncio
import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Channel, MessageActionTopicCreate

# --- Basic Configuration ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

API_ID_STR = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "crypto-signal-tracker")

# --- Input Validation ---
if not API_ID_STR or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set in your .env file.")

try:
    API_ID = int(API_ID_STR)
except ValueError:
    raise ValueError("API_ID must be an integer.") from None


async def list_topics(chat_id: int) -> None:
    """Connect to Telegram and list all topics in a specific group."""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    LOGGER.info("Starting client to fetch topic IDs...")
    await client.start()
    me = await client.get_me()
    LOGGER.info(f"Successfully logged in as {me.username}")

    try:
        entity = await client.get_entity(chat_id)
        if not isinstance(entity, Channel) or not entity.forum:
            LOGGER.error(f"Chat with ID {chat_id} is not a group with Topics enabled.")
            await client.disconnect()
            return
    except Exception as e:
        LOGGER.error(f"Could not find chat with ID {chat_id}. Error: {e}")
        await client.disconnect()
        return

    LOGGER.info(f"Fetching topics for group: '{entity.title}'")
    print("\n" + "=" * 20)
    print("Topics and Their IDs")
    print("=" * 20)

    # In groups with topics, topics are created via a specific message action.
    async for message in client.iter_messages(chat_id, limit=200):
        if message.action and isinstance(message.action, MessageActionTopicCreate):
            print(f'Topic Title: "{message.action.title}" --> Topic ID: {message.id}')

    print("\n" + "=" * 20)
    print("Copy the Topic ID for the topic you want to monitor (e.g., 'A').")

    await client.disconnect()
    LOGGER.info("Client disconnected.")


def main() -> None:
    """Parse command-line arguments and run the list_topics function."""
    parser = argparse.ArgumentParser(
        description="List all topics and their IDs in a Telegram group."
    )
    parser.add_argument(
        "chat_id",
        type=int,
        help="The ID of the group to fetch topics from (e.g., -1002430013497).",
    )
    args = parser.parse_args()

    asyncio.run(list_topics(args.chat_id))


if __name__ == "__main__":
    main()
