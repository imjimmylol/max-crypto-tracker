import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient

# --- Basic Configuration ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

# Load environment variables from your .env file
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "crypto-signal-tracker")

if not API_ID or not API_HASH:
    raise ValueError(
        "API_ID and API_HASH must be set in your .env file before running this."
    )


# --- Main Logic ---
async def list_my_chats() -> None:
    """Connect to Telegram and list all chats (dialogs) with their IDs."""
    # We are creating a new client instance here to avoid any conflicts
    # with the main app's session if it were running.
    assert API_ID is not None, "API_ID must be set in your .env file"
    client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

    LOGGER.info("Starting client to fetch chat IDs...")
    await client.start()

    me = await client.get_me()
    LOGGER.info(f"Successfully logged in as {me.username}")

    print("\n" + "=" * 20)
    print("Your Chats and Their IDs")
    print("=" * 20)
    print("Find your target group in this list, then copy its ID.")
    print("The ID for a group/channel usually starts with -100.\n")

    # The `get_dialogs` method fetches all your chats.
    async for dialog in client.iter_dialogs():
        # We only care about groups and channels, not individual users.
        if dialog.is_group or dialog.is_channel:
            print(f'Title: "{dialog.name}" --> ID: {dialog.id}')

    print("\n" + "=" * 20)
    print("Once you have the ID, paste it into main.py and you can delete this script.")

    await client.disconnect()
    LOGGER.info("Client disconnected.")


if __name__ == "__main__":
    import asyncio

    # If you are on Windows, you might need to add this line:
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(list_my_chats())
