from services.base_service import BaseService

async def get_deezer_track(query: str) -> dict:
    url = f"https://api.deezer.com/search?q={query.replace(' ', '+')}"
    session = await BaseService.get_session()
    async with session.get(url) as resp:
        data = await resp.json()
        if data.get("data"):
            track = data["data"][0]
            return {
                "link": track["link"],
                "title": track["title"],
                "artist": track["artist"]["name"]
            }
    raise Exception("No track found on Deezer")
