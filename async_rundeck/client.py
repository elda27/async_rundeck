from functools import lru_cache
import os
from typing import Any, Dict, Generic, Literal, Type, TypeVar
from aiohttp import ClientSession, ClientResponse
from pydantic import BaseModel
from async_rundeck.exceptions import RundeckError


class RundeckClient:
    def __init__(
        self,
        url: str = None,
        token: str = None,
        username: str = None,
        password: str = None,
        api_version: int = None,
    ) -> None:
        self.url = url or os.getenv("RUNDECK_URL", "http://localhost:4440")
        self.url = self.url.rstrip("/")
        self.token = token or os.getenv("RUNDECK_TOKEN")
        self.username = username or os.getenv("RUNDECK_USERNAME")
        self.password = password or os.getenv("RUNDECK_PASSWORD")
        self.api_version = api_version or int(os.getenv("RUNDECK_API_VERSION", "32"))
        if self.token is None and (self.password is None or self.password is None):
            raise ValueError("Cannot authenticate without a token or username/password")
        self.session_id: str = None
        self._session: ClientSession = None

    @property
    def options(self) -> Dict[str, Dict[str, Any]]:
        return {
            "headers": {"Accept": "application/json"},
            "params": {},
        }

    async def __aenter__(self) -> "RundeckClient":
        if self._session is None:
            self._session = await ClientSession().__aenter__()
        if self.token is None and self.session_id is None:
            with ClientSession() as session:
                self.session_id = await self.auth(session)
            self._session = await ClientSession(
                cookie=dict(JSESSIONID=self.session_id)
            ).__aenter__()
        return self

    async def __aexit__(self, *args) -> "RundeckClient":
        await self._session.__aexit__(*args)
        self._session = None

    async def request(self, method: str, url: str, **kwargs) -> ClientResponse:
        options = self.options
        for k, v in kwargs.items():
            options[k].update(v)
        if self.token:
            options["headers"]["X-Rundeck-Auth-Token"] = self.token

        return await self._session.request(method, url, **self.options)

    async def auth(self) -> str:
        url = self.url + "/j_security_check"
        p = {"j_username": self.username, "j_password": self.password}
        with await self._session.post(
            url,
            data=p,
        ) as r:
            session_id = r.cookies.get("JSESSIONID")
            if session_id is None:
                with r.history[-1] as r:
                    session_id = r.cookies.get("JSESSIONID")
        if session_id is None:
            raise RundeckError("Authrorization failed")
        return session_id.value
