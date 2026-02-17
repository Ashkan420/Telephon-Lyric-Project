from telethon import events
from clients.telegram_client import client
from services.deezer_service import get_deezer_track
from services.deezload_service import forward_deezload_messages
from services.lyrics_service import get_lyrics_lrclib
from services.telegraph_service import send_to_telegraph

@client.on(events.NewMessage(pattern=r"^/song (.+)"))
async def song_handler(event):
    query = event.pattern_match.group(1)
    await event.reply(f"🎧 Searching Deezer for: {query}")

    try:
        track = await get_deezer_track(query)
        deezer_link = track["link"]
        title = track["title"]
        artist = track["artist"]
        await event.reply(f"🔗 Found Deezer track:\n{artist} - {title}\n{deezer_link}")
    except Exception as e:
        await event.reply(f"❌ Deezer search failed: {e}")
        return

    try:
        album_msg, audio_msg = await forward_deezload_messages(deezer_link)
    except Exception as e:
        await event.reply(f"❌ Deezload failed: {e}")
        return

    await event.reply(f"📜 Getting lyrics from LRCLIB...\n🎤 {artist}\n🎵 {title}")
    try:
        lyrics = await get_lyrics_lrclib(artist, title)
    except Exception as e:
        await event.reply(f"❌ LRCLIB failed: {e}")
        return

    await event.reply("📝 Uploading album + lyrics to Telegraph...")
    try:
        telegraph_link = await send_to_telegraph(album_msg, lyrics, event.chat_id)
    except Exception as e:
        await event.reply(f"❌ Telegraph failed: {e}")
        return

    try:
        await client.forward_messages(event.chat_id, audio_msg)
    except Exception as e:
        await event.reply(f"❌ Failed to send audio file: {e}")

    final_msg = f"✅ Done!\n\n🎤 Artist: {artist}\n🎵 Title: {title}\n\n🔗 Telegraph:\n{telegraph_link}"
    await event.reply(final_msg)
