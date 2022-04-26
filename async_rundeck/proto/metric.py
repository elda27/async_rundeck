# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError


async def metric_list(session: RundeckClient, entrypoint: str, version: int) -> Object:
    """List links to enabled Metrics endpoints"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/metrics".format(version=version)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": Object}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")
