from uuid import uuid4
import pytest
from async_rundeck.rundeck import Rundeck
from tests.common import *


@pytest.mark.asyncio
async def test_create_project(rundeck: Rundeck):
    name = uuid4().hex
    project = await rundeck.create_project(name)
    assert project is not None and project.name == name


@pytest.mark.asyncio
async def test_list_project(rundeck: Rundeck):
    name = uuid4().hex
    project = await rundeck.create_project(name)
    await rundeck.delete_project(project.name)


@pytest.mark.asyncio
async def test_delete_project(rundeck: Rundeck):
    name = uuid4().hex
    assert await rundeck.create_project(name) is not None
    old_projects = await rundeck.list_project()
    await rundeck.delete_project(name)
    new_projects = await rundeck.list_project()
    assert len(new_projects) == (len(old_projects) - 1)


@pytest.mark.asyncio
async def test_get_project_config(rundeck: Rundeck):
    name = uuid4().hex
    config = {
        "param1": "value",
        "param2": "10",
        "param3": "False",
    }
    assert await rundeck.create_project(name, config=config) is not None
    fetch_config = await rundeck.get_project_config(name)
    for k in config.keys():
        assert config[k] == fetch_config[k]


@pytest.mark.asyncio
async def test_get_project_config_item(rundeck: Rundeck):
    name = uuid4().hex
    config = {
        "param1": "value",
        "param2": "10",
        "param3": "False",
    }
    assert await rundeck.create_project(name, config=config) is not None
    for k in config.keys():
        kv = await rundeck.get_project_config_item(name, k)
        assert kv[0] == k
        assert kv[1] == config[k]


@pytest.mark.asyncio
async def test_update_project_config(rundeck: Rundeck):
    name = uuid4().hex
    new_name = uuid4().hex
    assert await rundeck.create_project(name) is not None

    config = {
        "param1": "value",
        "param2": "10",
        "param3": "False",
    }
    await rundeck.update_project_config(name, config)
    new_config = await rundeck.get_project_config(name)
    for k in config.keys():
        assert new_config[k] == config[k]
