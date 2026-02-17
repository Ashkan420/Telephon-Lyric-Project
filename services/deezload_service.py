import asyncio
from clients.telegram_client import client
from config import SONG_BOT

async def forward_deezload_messages(deezer_link: str):
    async with client.conversation(SONG_BOT, timeout=60) as conv:
        sent_msg = await conv.send_message(deezer_link)

    await asyncio.sleep(5)

    msgs = [msg async for msg in client.iter_messages(
        SONG_BOT, min_id=sent_msg.id, limit=8
    )]
    msgs = list(reversed(msgs))

    album_msg = None
    audio_msg = None

    for msg in msgs:
        if not album_msg and msg.photo:
            album_msg = msg
        elif not audio_msg and (msg.audio or (msg.document and msg.file.mime_type and "audio" in msg.file.mime_type)):
            audio_msg = msg
        if album_msg and audio_msg:
            break

    if not audio_msg:
        raise Exception("Did not receive audio from Deezload bot")

    return album_msg, audio_msg
