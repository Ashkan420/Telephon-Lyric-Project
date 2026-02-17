from services.base_service import BaseService

async def get_lyrics_lrclib(artist: str, title: str) -> str:
    url = f"https://lrclib.net/api/search?artist_name={artist.replace(' ', '+')}&track_name={title.replace(' ', '+')}"
    session = await BaseService.get_session()
    async with session.get(url) as resp:
        if resp.status != 200:
            raise Exception(f"LRCLIB API failed (HTTP {resp.status})")
        data = await resp.json()
        if not data:
            return "Lyrics not found."
        best = data[0]
        lyrics = best.get("plainLyrics") or best.get("syncedLyrics")
        if not lyrics:
            return "Lyrics not found."
        return f"[Lyrics]\n{lyrics.strip()}"
