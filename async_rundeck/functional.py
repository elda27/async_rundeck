from aiohttp import ClientSession


def bootstrap(session: ClientSession, method: str) -> None:
    async with session._request(method, url)
    pass
