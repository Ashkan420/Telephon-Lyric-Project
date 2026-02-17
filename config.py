import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TELETHON_SESSION = os.getenv("TELETHON_SESSION")

SONG_BOT = "@deezload2bot"
TELEGRAPH_BOT = "@TeleUpBot"