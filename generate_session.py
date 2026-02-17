from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

API_ID = int(input("Enter API_ID: "))
API_HASH = input("Enter API_HASH: ")

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("\n✅ Your TELETHON_SESSION string:\n")
    print(client.session.save())