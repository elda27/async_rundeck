import json
from enum import Enum
from typing import List, Optional, Union
from pydantic import parse_raw_as, BaseModel, Field
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.misc import filter_none
from async_rundeck.exceptions import RundeckError, VersionError
from async_rundeck.proto.definitions import ExecutionList, RetryExecutionRequest, RetryExecutionRequest


async def job_retry_execution(session: RundeckClient, job_id: String,
    execution_id: Integer, *, request: Optional["RetryExecutionRequest"
]=None
    ) ->ExecutionList:
    """Retry a failed job execution on failed nodes only or on the same as the execution. This is the same functionality as the `Retry Failed Nodes ...` button on the execution page."""
    if session.version < 26:
        raise VersionError(
            f'Insufficient api version error, Required >{session.version}')
    url = session.format_url('/api/{version}/job/{jobID}/retry/{executionID}',
        version=session.version, jobID=job_id, executionID=execution_id)
    async with session.request('POST', url, data=json.dumps(request) if
        isinstance(request, dict) else request.json(), params=filter_none(
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
