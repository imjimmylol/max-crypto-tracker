import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

# --- Basic Configuration ---
# Set up logging to see telethon's activity
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

# --- Environment Variables ---
# IMPORTANT: These are loaded from your .env file.
# See .env.example for the format.
API_ID_STR = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "crypto-signal-tracker")

# --- Input Validation ---
# Ensure that the required environment variables are set.
if not API_ID_STR or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set in your .env file.")

# Convert API_ID to integer
try:
    API_ID = int(API_ID_STR)
except ValueError:
    raise ValueError("API_ID must be an integer.") from None


# --- Main Application Logic ---
# Initialize the Telegram client
# The session file (SESSION_NAME.session) stores your authorization,
# so you don't have to log in every time.
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# --- Topic Configuration ---
# Replace this with the ID of the topic you want to monitor
TARGET_TOPIC_ID = 5


@client.on(
    events.NewMessage(
        chats=[-1002430013497],
        func=lambda e: e.message.reply_to is not None
        and e.message.reply_to.reply_to_msg_id == TARGET_TOPIC_ID,
    )
)  # type: ignore[misc]
async def handle_new_message(event: events.NewMessage.Event) -> None:
    """Handle new messages in the specified chat.

    This function is an event handler that gets called every time a new
    message arrives.
    """
    chat = await event.get_chat()
    sender = await event.get_sender()

    LOGGER.info(f"New message from '{sender.username}' in chat '{chat.title}':")
    LOGGER.info(f"-> {event.message.text}\n")

    # TODO: In the next step, we will parse this text and save it.


async def main() -> None:
    """Run the main application entry point."""
    LOGGER.info("Starting client...")
    await client.start()

    # The first time you run this, Telethon will prompt you in the terminal
    # for your phone number, a login code, and your 2FA password (if you have one).
    # After that, the .session file will handle authentication automatically.

    me = await client.get_me()
    LOGGER.info(f"Successfully logged in as {me.username}")

    LOGGER.info("Client is running and listening for new messages...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    # This block allows the script to be run directly.
    # The client is started and will run until you stop it (e.g., with Ctrl+C).
    with client:
        client.loop.run_until_complete(main())
