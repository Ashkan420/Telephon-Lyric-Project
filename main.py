import asyncio
from clients.telegram_client import client
import handlers.song_handler  # registers /song command
from services.base_service import BaseService

async def main():
    await client.start()
    print("🚀 Mega Telethon bridge running...")

    try:
        await client.run_until_disconnected()
    finally:
        await BaseService.close_session()
        print("🛑 HTTP session closed")

asyncio.run(main())
