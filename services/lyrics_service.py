from services.base_service import BaseService
import asyncio
import aiohttp

async def get_lyrics_lrclib(artist: str, title: str) -> str:
    url = (
        f"https://lrclib.net/api/search"
        f"?artist_name={artist.replace(' ', '+')}"
        f"&track_name={title.replace(' ', '+')}"
    )

    session = await BaseService.get_session()

    retries = 5  # number of attempts
    delay = 2    # initial delay in seconds between retries

    for attempt in range(retries):
        try:
            timeout = aiohttp.ClientTimeout(total=15)  # 15s timeout per request
            async with session.get(url, timeout=timeout) as resp:
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

        except (aiohttp.ClientConnectorError, aiohttp.ClientOSError, asyncio.TimeoutError) as e:
            if attempt == retries - 1:
                # Last attempt, raise error
                raise Exception(f"LRCLIB connection failed after {retries} tries: {e}")
            # Wait before retrying
            await asyncio.sleep(delay)
            delay += 1  # gradually increase delay between retries
