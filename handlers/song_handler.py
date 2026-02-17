from telethon import events
from clients.telegram_client import client
from services.deezer_service import get_deezer_track
from services.deezload_service import forward_deezload_messages
from services.lyrics_service import get_lyrics_lrclib
from services.telegraph_service import send_to_telegraph

@client.on(events.NewMessage(pattern=r"^/song (.+)"))
async def song_handler(event):
    query = event.pattern_match.group(1)

    # Check for -noimg flag
    no_img = False
    if "-noimg" in query:
        no_img = True
        query = query.replace("-noimg", "").strip()

    status_msg = await event.reply(f"🎧 Searching Deezer for: {query}")

    # Step 1: Deezer search
    try:
        track = await get_deezer_track(query)
        deezer_link = track["link"]
        title = track["title"]
        artist = track["artist"]

        await status_msg.edit(
            f"🔗 Found Deezer track:\n{artist} - {title}\n{deezer_link}"
        )

    except Exception as e:
        await status_msg.edit(f"❌ Deezer search failed: {e}")
        return

    # Step 2: Deezload
    try:
        await status_msg.edit("⬇️ Downloading from Deezload...")
        album_msg, audio_msg = await forward_deezload_messages(deezer_link)
    except Exception as e:
        await status_msg.edit(f"❌ Deezload failed: {e}")
        return

    # Step 3: Lyrics
    try:
        await status_msg.edit(
            f"📜 Getting lyrics from LRCLIB...\n🎤 {artist}\n🎵 {title}"
        )
        lyrics = await get_lyrics_lrclib(artist, title)
    except Exception as e:
        await status_msg.edit(f"❌ LRCLIB failed: {e}")
        return

    # Step 4: Telegraph upload
    try:
        await status_msg.edit("📝 Uploading to Telegraph...")

        # If -noimg, skip the photo but keep the caption text
        tele_caption = album_msg.message if album_msg else f"{artist} - {title}"

        telegraph_link = await send_to_telegraph(
            album_msg if not no_img else None,  # None = skip photo
            lyrics,
            event.chat_id,
            caption=tele_caption  # pass the caption explicitly
        )

    except Exception as e:
        await status_msg.edit(f"❌ Telegraph failed: {e}")
        return

    # Step 5: Forward audio
    try:
        await client.forward_messages(event.chat_id, audio_msg)
    except Exception as e:
        await event.reply(f"❌ Failed to send audio file: {e}")

    # Step 6: Delete status and send final message
    await status_msg.delete()
    final_msg = (
        f"{title} — {artist}\n\n"
        f"{telegraph_link}"
    )
    await event.reply(final_msg)
