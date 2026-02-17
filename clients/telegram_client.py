from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, TELETHON_SESSION

if not TELETHON_SESSION:
    raise Exception("❌ TELETHON_SESSION is missing!")

client = TelegramClient(StringSession(TELETHON_SESSION), API_ID, API_HASH)