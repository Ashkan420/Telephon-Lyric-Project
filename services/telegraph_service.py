import asyncio
from clients.telegram_client import client
from config import TELEGRAPH_BOT
from utils.text_utils import split_text_by_line_breaks

async def send_to_telegraph(album_msg, lyrics, chat_id, caption=None):
    """
    Sends album + lyrics to Telegraph.
    
    Parameters:
        album_msg: The original album message with photo (optional if -noimg)
        lyrics: Lyrics text
        chat_id: Telegram chat ID
        caption: Text caption to send if album_msg is None (-noimg mode)
    """
    last_msg = await client.get_messages(TELEGRAPH_BOT, limit=1)
    last_id = last_msg[0].id if last_msg else 0

    # Forward album photo if it exists
    if album_msg:
        await client.forward_messages(TELEGRAPH_BOT, album_msg)
    # If no album photo but caption is provided, send caption as first message
    elif caption:
        await client.send_message(TELEGRAPH_BOT, caption)
        await asyncio.sleep(0.5)

    # Split lyrics into chunks using line breaks
    lyrics_chunks = split_text_by_line_breaks(lyrics, limit=3425)
    for chunk in lyrics_chunks:
        # Add <br> at the start of each chunk
        chunk = "<br>" + chunk
        await client.send_message(TELEGRAPH_BOT, chunk)
        await asyncio.sleep(0.5)  # small delay to avoid flooding

    await asyncio.sleep(1)

    # Find the Done button message
    done_msg = None
    async for msg in client.iter_messages(TELEGRAPH_BOT, min_id=last_id, limit=15):
        if msg.buttons:
            for row in msg.buttons:
                for btn in row:
                    if btn.text and "done" in btn.text.lower():
                        done_msg = msg
                        break
        if done_msg:
            break

    if not done_msg:
        raise Exception("Could not find Done button message from Telegraph bot")

    # Click Done button
    await done_msg.click(text="Done")
    await asyncio.sleep(2)

    # Wait for the Telegraph link
    for _ in range(30):
        await asyncio.sleep(1)
        refreshed_msg = await client.get_messages(TELEGRAPH_BOT, ids=done_msg.id)
        if refreshed_msg.text and "http" in refreshed_msg.text.lower():
            return refreshed_msg.text

    raise Exception("Telegraph link not received after clicking Done")
