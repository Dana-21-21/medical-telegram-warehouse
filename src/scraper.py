import os
import json
import logging
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from telethon.sync import TelegramClient

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
SESSION_NAME = os.getenv("SESSION_NAME")

# =====================================================
# TELEGRAM CHANNELS TO SCRAPE
# =====================================================
CHANNELS = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahethiopia"
]

# Number of messages to scrape from each channel
MESSAGE_LIMIT = 200

# =====================================================
# CREATE DATA LAKE FOLDERS
# =====================================================
today = datetime.now().strftime("%Y-%m-%d")

json_root = Path("data/raw/telegram_messages") / today
image_root = Path("data/raw/images")
log_root = Path("logs")

json_root.mkdir(parents=True, exist_ok=True)
image_root.mkdir(parents=True, exist_ok=True)
log_root.mkdir(parents=True, exist_ok=True)

# =====================================================
# LOGGING CONFIGURATION
# =====================================================
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("=" * 70)
logging.info("Telegram scraping started")

# =====================================================
# CREATE TELEGRAM CLIENT
# =====================================================
client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)

client.start(phone=PHONE_NUMBER)

print("\n======================================")
print(" Connected to Telegram Successfully")
print("======================================\n")

logging.info("Connected to Telegram")

# =====================================================
# SCRAPE EACH CHANNEL
# =====================================================
for channel_username in CHANNELS:

    print("=" * 60)
    print(f"Scraping Channel: {channel_username}")
    print("=" * 60)

    logging.info(f"Starting channel: {channel_username}")

    try:
        channel = client.get_entity(channel_username)

        print(f"Channel Name : {channel.title}")
        print(f"Channel ID   : {channel.id}")

    except Exception as e:

        print(f"Could not access {channel_username}")
        print(e)

        logging.error(f"{channel_username}: {e}")

        continue

    # -----------------------------------------
    # Create image folder
    # -----------------------------------------
    channel_image_folder = image_root / channel_username
    channel_image_folder.mkdir(parents=True, exist_ok=True)

    messages = []

    # -----------------------------------------
    # Read messages
    # -----------------------------------------
    for message in client.iter_messages(channel, limit=MESSAGE_LIMIT):

        try:

            image_path = None

            # Download photo if it exists
            if message.photo:

                image_file = channel_image_folder / f"{message.id}.jpg"

                client.download_media(
                    message,
                    file=str(image_file)
                )

                image_path = str(image_file)

            record = {

                "message_id": message.id,

                "channel_name": channel.title,

                "channel_username": channel_username,

                "message_date": (
                    message.date.isoformat()
                    if message.date
                    else None
                ),

                "message_text": (
                    message.message
                    if message.message
                    else ""
                ),

                "views": (
                    message.views
                    if message.views is not None
                    else 0
                ),

                "forwards": (
                    message.forwards
                    if message.forwards is not None
                    else 0
                ),

                "has_media": message.photo is not None,

                "image_path": image_path

            }

            messages.append(record)

            print(f"Collected Message {message.id}")

        except Exception as e:

            logging.error(
                f"{channel_username} Message {message.id}: {e}"
            )

    # -----------------------------------------
    # Save JSON
    # -----------------------------------------
    output_file = json_root / f"{channel_username}.json"

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nSaved {len(messages)} messages")
    print(f"JSON -> {output_file}\n")

    logging.info(
        f"{channel_username}: {len(messages)} messages saved"
    )

print("=" * 70)
print("SCRAPING COMPLETED SUCCESSFULLY")
print("=" * 70)

logging.info("Telegram scraping finished")
client.disconnect()
