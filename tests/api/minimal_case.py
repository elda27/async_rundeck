import json
from enum import Enum
from typing import List, Optional, Union
from pydantic import parse_raw_as, BaseModel, Field
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object, File
from async_rundeck.client import RundeckClient
from async_rundeck.misc import filter_none
from async_rundeck.exceptions import RundeckError, VersionError
from async_rundeck.proto.definitions import ExecutionList


async def job_execution_list(session: RundeckClient, id: String
    ) ->ExecutionList:
    """List job executions"""
    if session.version < 26:
        raise VersionError(
            f'Insufficient api version error, Required >{session.version}')
    url = session.format_url('/api/{version}/job/{id}/executions', version=
        session.version, id=id)
    async with session.request('GET', url, data=None, params=filter_none(
        dict())) as response:
        obj = await response.text()
        if response.ok:
            try:
                response_type = {(200): ExecutionList}[response.status]
                if response_type is None:
                    return None
                elif response_type is String:
                    return obj
                else:
                    return parse_raw_as(response_type, obj)
            except KeyError:
                raise RundeckError(
                    f'Unknwon response code: {session.url}({response.status})')
        else:
            raise RundeckError(
                f'Connection diffused: {session.url}({response.status})\n{obj}'
                )
