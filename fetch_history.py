import argparse
import json
import logging
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon import TelegramClient

# --- Basic Configuration ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# --- Environment Variables ---
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

# --- Constants ---
TARGET_CHAT_ID = -1002430013497
OUTPUT_FILE = "messages.json"


async def fetch_history(past_days: int) -> None:
    """Fetch historical messages from a specific chat."""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    LOGGER.info("Starting client to fetch message history...")
    await client.start()
    me = await client.get_me()
    LOGGER.info(f"Successfully logged in as {me.username}")

    try:
        target_chat = await client.get_entity(TARGET_CHAT_ID)
        LOGGER.info(
            f"Fetching messages from '{target_chat.title}' for the last"
            f" {past_days} day(s)."
        )
    except Exception as e:
        LOGGER.error(
            f"Could not find chat with ID {TARGET_CHAT_ID}. "
            f"Please check the ID. Error: {e}"
        )
        return

    # Calculate the date to start fetching from
    offset_date = datetime.now(timezone.utc) - timedelta(days=past_days)

    messages_data = []
    message_count = 0

    # Iterate through the messages
    async for message in client.iter_messages(
        target_chat, offset_date=offset_date, reverse=True
    ):
        if message.text:  # We only care about messages with text
            messages_data.append(
                {
                    "message_id": message.id,
                    "date": message.date.isoformat(),
                    "sender_id": str(message.sender_id),
                    "text": message.text,
                }
            )
            message_count += 1

    # Save the messages to a JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(messages_data, f, indent=4, ensure_ascii=False)

    LOGGER.info(
        f"Successfully fetched and saved {message_count} messages to {OUTPUT_FILE}."
    )

    await client.disconnect()
    LOGGER.info("Client disconnected.")


def main() -> None:
    """Parse command-line arguments and run the fetch_history function."""
    parser = argparse.ArgumentParser(
        description="Fetch historical messages from a Telegram chat."
    )
    parser.add_argument(
        "--past-days",
        type=int,
        default=7,
        help="The number of past days of message history to fetch. Defaults to 7.",
    )
    args = parser.parse_args()

    import asyncio

    asyncio.run(fetch_history(args.past_days))


if __name__ == "__main__":
    main()
