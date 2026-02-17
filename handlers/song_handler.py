from telethon import events
from clients.telegram_client import client
from services.deezer_service import get_deezer_track
from services.deezload_service import forward_deezload_messages
from services.lyrics_service import get_lyrics_lrclib
from services.telegraph_service import send_to_telegraph

@client.on(events.NewMessage(pattern=r"^/song (.+)"))
async def song_handler(event):
    query = event.pattern_match.group(1)

    status_msg = await event.reply(f"🎧 Searching Deezer for: {query}")

    try:
        track = await get_deezer_track(query)
        deezer_link = track["link"]
        title = track["title"]
        artist = track["artist"]

        await status_msg.edit(
            f"🔗 Found Deezer track:\n"
            f"{artist} - {title}\n"
            f"{deezer_link}"
        )

    except Exception as e:
        await status_msg.edit(f"❌ Deezer search failed: {e}")
        return

    try:
        await status_msg.edit("⬇️ Downloading from Deezload...")
        album_msg, audio_msg = await forward_deezload_messages(deezer_link)

    except Exception as e:
        await status_msg.edit(f"❌ Deezload failed: {e}")
        return

    try:
        await status_msg.edit(
            f"📜 Getting lyrics from LRCLIB...\n"
            f"🎤 {artist}\n"
            f"🎵 {title}"
        )
        lyrics = await get_lyrics_lrclib(artist, title)

    except Exception as e:
        await status_msg.edit(f"❌ LRCLIB failed: {e}")
        return

    try:
        await status_msg.edit("📝 Uploading album + lyrics to Telegraph...")
        telegraph_link = await send_to_telegraph(album_msg, lyrics, event.chat_id)

    except Exception as e:
        await status_msg.edit(f"❌ Telegraph failed: {e}")
        return

    # Forward audio separately
    try:
        await client.forward_messages(event.chat_id, audio_msg)
    except Exception as e:
        await event.reply(f"❌ Failed to send audio file: {e}")

    # Delete the status message so chat stays clean
    try:
        await status_msg.delete()
    except:
        pass

    # Send final message fresh so preview works
    final_msg = (
        f"{title} — {artist}"
        f"{telegraph_link}"
    )

    await event.reply(final_msg)
