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

for dialog in client.iter_dialogs():
    print(f"Name: {dialog.name}")
    print(f"ID: {dialog.id}")
    print(f"Username: {getattr(dialog.entity, 'username', None)}")
    print(f"Type: {type(dialog.entity).__name__}")
    print("-" * 50)
