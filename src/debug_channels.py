import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
SESSION_NAME = os.getenv("SESSION_NAME")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
client.start(phone=PHONE_NUMBER)

print("\n===== YOUR TELEGRAM DIALOGS =====\n")

search_terms = [
    "CHEMED",
    "LOBELIA",
    "TIKVAH"
]

print("\nSearching for target channels...\n")

found = False

for dialog in client.iter_dialogs():

    name = (dialog.name or "").upper()
    username = (getattr(dialog.entity, "username", "") or "").upper()

    for term in search_terms:
        if term in name or term in username:
            found = True
            print("=" * 60)
            print("Name:", dialog.name)
            print("Username:", getattr(dialog.entity, "username", None))
            print("Type:", type(dialog.entity).__name__)
            print("ID:", dialog.id)

if not found:
    print("No matching channels were found.")
