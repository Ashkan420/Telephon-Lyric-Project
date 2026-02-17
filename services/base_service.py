import aiohttp
import asyncio

class BaseService:
    _session: aiohttp.ClientSession = None

    @classmethod
    async def get_session(cls):
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        if cls._session and not cls._session.closed:
            await cls._session.close()
            cls._session = None

# Ensure session is closed on exit
#asyncio.get_event_loop().create_task(BaseService.get_session())
