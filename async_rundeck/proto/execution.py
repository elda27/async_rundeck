# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError


class ExecutionBulkDeleteRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class ExecutionInputFilesListResponse(BaseModel):
    files: List[JobInputFileInfo] = Field(alias="files")


async def execution_status_get(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> Execution:
    """Get the status of an execution by ID"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/execution/{id}".format(version=version, id=id)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": Execution}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_delete(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> None:
    """Delete an exeuction by ID"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/execution/{id}".format(version=version, id=id)
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_bulk_delete(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    execution_bulk_delete_request: ExecutionBulkDeleteRequest,
) -> JobExecutionDelete:
    """Bulk delete executions"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/executions/delete".format(version=version)
    async with session.request(
        "POST", url, data=dict(**execution_bulk_delete_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobExecutionDelete}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_state_get(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> ExecutionState:
    """Get detail about the node and step state of an execution by ID. The execution can be currently running or completed."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/execution/{id}/state".format(
        version=version, id=id
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ExecutionState}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_input_files_list(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> ExecutionInputFilesListResponse:
    """List input files for an execution"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/execution/{id}/input/files".format(
        version=version, id=id
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ExecutionInputFilesListResponse}[
                    response.status
                ]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_list_running(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> ExecutionList:
    """List job executions"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/executions/running".format(
        version=version, project=project
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ExecutionList}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_query(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    *,
    status_filter: Optional[String] = None,
    abortedby_filter: Optional[String] = None,
    user_filter: Optional[String] = None,
    recent_filter: Optional[String] = None,
    older_filter: Optional[String] = None,
    begin: Optional[String] = None,
    adhoc: Optional[Boolean] = None,
) -> None:
    """Query for Executions based on Job or Execution details"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/executions".format(
        version=version, project=project
    )
    async with session.request(
        "GET",
        url,
        data=dict(),
        params=dict(
            status_filter=status_filter,
            abortedby_filter=abortedby_filter,
            user_filter=user_filter,
            recent_filter=recent_filter,
            older_filter=older_filter,
            begin=begin,
            adhoc=adhoc,
        ),
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def execution_output_get(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    id: String,
    *,
    offset: Optional[String] = None,
    maxlines: Optional[Number] = 5000,
) -> ExecutionOutput:
    """List input files for an execution"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/execution/{id}/output".format(
        version=version, id=id
    )
    async with session.request(
        "GET", url, data=dict(), params=dict(offset=offset, maxlines=maxlines)
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ExecutionOutput}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")
