from async_rundeck.client import RundeckClient
from async_rundeck.proto.definitions import Project


class Rundeck:
    def __init__(
        self,
        url: str = None,
        token: str = None,
        username: str = None,
        password: str = None,
        api_version: int = None,
    ) -> None:
        self.client = RundeckClient(url, token, username, password, api_version)

    async def __aenter__(self):
        await self.client.__aenter__()

    async def __aexit__(self, *args):
        await self.client.__aexit__(*args)

    async def create_project(self) -> Project:
        raise NotImplementedError()
