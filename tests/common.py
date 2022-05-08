import pytest
import pytest_docker
from async_rundeck.rundeck import Rundeck
import requests
import asyncio
import os


def is_responsive(url):
    try:
        response = requests.get(url + "/api/41/metrics/ping")
        if response.status_code == 403:
            return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


rundeck_url = os.getenv("RUNDECK_URL")
if rundeck_url is None:

    @pytest.fixture(scope="session")
    async def rundeck_service(docker_ip, docker_services) -> str:
        """Ensure that HTTP service is up and responsive."""

        # `port_for` takes a container port and returns the corresponding host port
        port = docker_services.port_for("rundeck", 4440)
        url = "http://{}:{}".format(docker_ip, port)
        docker_services.wait_until_responsive(
            timeout=60.0, pause=1.0, check=lambda: is_responsive(url)
        )
        return url

else:

    @pytest.fixture(scope="session")
    async def rundeck_service() -> str:
        for i in range(60):
            if is_responsive(rundeck_url):
                return rundeck_url
            await asyncio.sleep(1)
            asyncio.sleep(1.0)
        raise TimeoutError(
            "Rundeck service is not responsive. Wrong configurated variable RUNDECK_URL"
        )


@pytest.fixture()
async def rundeck(rundeck_service: str) -> Rundeck:
    async with Rundeck(
        url=rundeck_service, username="admin", password="admin", api_version=41
    ) as rundeck:
        yield rundeck


__all__ = [
    "event_loop",
    "rundeck",
    "rundeck_service",
]
