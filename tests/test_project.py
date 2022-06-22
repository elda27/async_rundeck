from uuid import uuid4
import pytest
from async_rundeck.rundeck import Rundeck, RundeckError
from tests.common import *


@pytest.mark.asyncio
async def test_create_project(rundeck: Rundeck):
    name = uuid4().hex
    project = await rundeck.create_project(name)
    assert project is not None and project.name == name


@pytest.mark.asyncio
async def test_get_project(rundeck: Rundeck):
    name = uuid4().hex
    project = await rundeck.create_project(name)
    project_get = await rundeck.get_project(project.name)

    assert project_get == project

    with pytest.raises(RundeckError):
        await rundeck.get_project("emptry-" + name)


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


@pytest.mark.asyncio
async def test_update_project_config_item(rundeck: Rundeck):
    name = uuid4().hex
    new_value = "new_value"
    assert await rundeck.create_project(name) is not None

    config = {
        "project.globals.param1": "value",
        "project.globals.param2": "10",
        "project.globals.param3": "False",
    }
    await rundeck.update_project_config(name, config)
    await rundeck.update_project_config_item(name, "project.globals.param1", new_value)
    new_config = await rundeck.get_project_config(name)
    for k in config.keys():
        if k == "project.globals.param1":
            assert new_config[k] != config[k] and new_config[k] == new_value
        else:
            assert new_config[k] == config[k]


@pytest.mark.asyncio
async def test_delete_project_config_item(rundeck: Rundeck):
    name = uuid4().hex
    new_value = "new_value"
    assert await rundeck.create_project(name) is not None

    config = {
        "project.globals.param1": "value",
        "project.globals.param2": "10",
        "project.globals.param3": "False",
    }
    await rundeck.update_project_config(name, config)
    await rundeck.delete_project_config_item(name, "project.globals.param1")
    new_config = await rundeck.get_project_config(name)
    assert "project.globals.param1" not in new_config
    for k in config.keys():
        if k == "project.globals.param1":
            continue
        assert new_config[k] == config[k]
