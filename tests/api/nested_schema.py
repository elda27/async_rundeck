from enum import Enum
from typing import List, Optional, Union
from pydantic import parse_obj_as, BaseModel, Field
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError
from async_rundeck.proto.definitions import JobInputFileInfo


class ExecutionInputFilesListResponse(BaseModel):
    files: List["JobInputFileInfo"] = Field(alias='files')


async def execution_input_files_list(session: RundeckClient, entrypoint:
    str, version: int, id: String) ->ExecutionInputFilesListResponse:
    """List input files for an execution"""
    if version < 26:
        raise VersionError(f'Insufficient api version error, Required >26')
    url = entrypoint + '/api/{version}/execution/{id}/input/files'.format(
        version=version, id=id)
    async with session.request('GET', url, data=dict(), params=dict()
        ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {'200': ExecutionInputFilesListResponse}[
                    response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError(
                    f'Unknwon response code: {url}({response.status})')
        else:
            raise RundeckError(
                f'Connection diffused: {url}({response.status})\n{obj}')
