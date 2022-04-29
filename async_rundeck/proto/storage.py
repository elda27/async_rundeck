# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError
from async_rundeck.proto.definitions import StorageKeyListResponse, Object


async def storage_key_get_material(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    key_path: String,
    accept: String,
) -> Union[Object, None]:
    """Get key material at the specified PATH"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/storage/keys/{keyPath}".format(
        version=version, key_path=key_path
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": Object, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError(f"Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def storage_key_get_metadata(
    session: RundeckClient, entrypoint: str, version: int, path: String, accept: String
) -> Union[StorageKeyListResponse, None]:
    """List resources at the specified PATH"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/storage/keys/{path}".format(
        version=version, path=path
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": StorageKeyListResponse, "404": None}[
                    response.status
                ]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError(f"Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def storage_key_create(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    path: String,
    file: Object,
    *,
    content_type: Optional[String] = "application/pgp-keys",
) -> Union[None, None]:
    """Set storage key contents"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/storage/keys/{path}".format(
        version=version, path=path
    )
    async with session.request(
        "POST", url, data=dict(**file.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"201": None, "409": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError(f"Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def storage_key_update(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    path: String,
    file: Object,
    *,
    content_type: Optional[String] = "application/pgp-keys",
) -> None:
    """Set storage key contents"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/storage/keys/{path}".format(
        version=version, path=path
    )
    async with session.request(
        "PUT", url, data=dict(**file.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError(f"Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def storage_key_delete(
    session: RundeckClient, entrypoint: str, version: int, path: String
) -> None:
    """Deletes the file if it exists and returns 204 response."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/storage/keys/{path}".format(
        version=version, path=path
    )
    async with session.request("DELETE", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"204": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError(f"Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")
