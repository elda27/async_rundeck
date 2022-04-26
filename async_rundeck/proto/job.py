# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError


class JobBulkDeleteRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobExecutionEnableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobExecutionDisableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobScheduleEnableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobScheduleDisableResponse(BaseModel):
    success: Optional[Boolean] = Field(alias="success")


class JobExecutionBulkEnableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobExecutionBulkDisableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobScheduleBulkEnableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobScheduleBulkDisableRequest(BaseModel):
    ids: List[String] = Field(alias="ids")


class JobWorkflowGetResponse(BaseModel):
    workflow: List[WorkflowStep] = Field(alias="workflow")


async def job_list(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    *,
    id_list: Optional[String] = None,
    group_path: Optional[String] = "*",
    job_filter: Optional[String] = None,
    job_exact_filter: Optional[String] = None,
    group_path_exact: Optional[String] = None,
    scheduled_filter: Optional[Boolean] = None,
    server_node_uuid_filter: Optional[String] = None,
) -> List[Job]:
    """List the jobs that exist for a project"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/jobs".format(
        version=version, project=project
    )
    async with session.request(
        "GET",
        url,
        data=dict(),
        params=dict(
            id_list=id_list,
            group_path=group_path,
            job_filter=job_filter,
            job_exact_filter=job_exact_filter,
            group_path_exact=group_path_exact,
            scheduled_filter=scheduled_filter,
            server_node_uuid_filter=server_node_uuid_filter,
        ),
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": List[Job]}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_execution_list(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> ExecutionList:
    """List job executions"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/executions".format(
        version=version, id=id
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


async def job_execution_run(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    id: String,
    *,
    request: Optional[ExecuteJobRequest] = None,
) -> Execution:
    """Run the specified job"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/executions".format(
        version=version, id=id
    )
    async with session.request(
        "POST", url, data=dict(**request.dict()), params=dict()
    ) as response:
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


async def job_execution_delete(
    session: RundeckClient, entrypoint: str, version: int, id: Integer
) -> JobExecutionDelete:
    """Delete all job executions"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/executions".format(
        version=version, id=id
    )
    async with session.request("DELETE", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"204": JobExecutionDelete}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_retry_execution(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    job_i_d: String,
    execution_i_d: Integer,
    *,
    request: Optional[RetryExecutionRequest] = None,
) -> ExecutionList:
    """Retry a failed job execution on failed nodes only or on the same as the execution. This is the same functionality as the `Retry Failed Nodes ...` button on the execution page."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{jobID}/retry/{executionID}".format(
        version=version, job_i_d=job_i_d, execution_i_d=execution_i_d
    )
    async with session.request(
        "POST", url, data=dict(**request.dict()), params=dict()
    ) as response:
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


async def job_get(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    id: String,
    *,
    format: Optional[String] = "xml",
) -> Union[Object, None]:
    """Export a single job definition in XML or YAML formats."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}".format(version=version, id=id)
    async with session.request(
        "GET", url, data=dict(), params=dict(format=format)
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": Object, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_delete(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> Union[None, None]:
    """Delete a single job definition."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}".format(version=version, id=id)
    async with session.request("DELETE", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"204": None, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_info_get(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobMetadata:
    """Get metadata about a specific job."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/info".format(version=version, id=id)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobMetadata}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_bulk_delete(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    job_bulk_delete_request: JobBulkDeleteRequest,
) -> JobBulkOperationResponse:
    """Delete multiple job definitions at once"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/jobs/delete".format(version=version)
    async with session.request(
        "POST", url, data=dict(**job_bulk_delete_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobBulkOperationResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_execution_enable(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobExecutionEnableResponse:
    """Enable executions for a job. (ACL requires toggle_execution action for a job.)"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/execution/enable".format(
        version=version, id=id
    )
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobExecutionEnableResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_execution_disable(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobExecutionDisableResponse:
    """Disable all executions for a job (scheduled or manual). (ACL requires toggle_execution action for a job.)"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/execution/disable".format(
        version=version, id=id
    )
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobExecutionDisableResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_schedule_enable(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobScheduleEnableResponse:
    """Enable the schedule for a job. (ACL requires toggle_schedule action for a job.)"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/schedule/enable".format(
        version=version, id=id
    )
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobScheduleEnableResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_schedule_disable(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobScheduleDisableResponse:
    """Disable the schedule for a job. (ACL requires toggle_schedule action for a job.)"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/schedule/disable".format(
        version=version, id=id
    )
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobScheduleDisableResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_execution_bulk_enable(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    job_execution_bulk_enable_request: JobExecutionBulkEnableRequest,
) -> JobBulkOperationResponse:
    """Bulk enable job executions"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/jobs/execution/enable".format(version=version)
    async with session.request(
        "POST",
        url,
        data=dict(**job_execution_bulk_enable_request.dict()),
        params=dict(),
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobBulkOperationResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_execution_bulk_disable(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    job_execution_bulk_disable_request: JobExecutionBulkDisableRequest,
) -> JobBulkOperationResponse:
    """Bulk disable job executions"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/jobs/execution/disable".format(version=version)
    async with session.request(
        "POST",
        url,
        data=dict(**job_execution_bulk_disable_request.dict()),
        params=dict(),
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobBulkOperationResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_schedule_bulk_enable(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    job_schedule_bulk_enable_request: JobScheduleBulkEnableRequest,
) -> JobBulkOperationResponse:
    """Bulk enable job schedule"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/jobs/schedule/enable".format(version=version)
    async with session.request(
        "POST", url, data=dict(**job_schedule_bulk_enable_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobBulkOperationResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_schedule_bulk_disable(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    job_schedule_bulk_disable_request: JobScheduleBulkDisableRequest,
) -> JobBulkOperationResponse:
    """Bulk disable job schedule"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/jobs/schedule/disable".format(version=version)
    async with session.request(
        "POST",
        url,
        data=dict(**job_schedule_bulk_disable_request.dict()),
        params=dict(),
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobBulkOperationResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_input_file_upload(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    id: String,
    option_name: String,
    file_name: String,
    file: Object,
) -> None:
    """Upload file as job option"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/input/file".format(
        version=version, id=id
    )
    async with session.request(
        "POST",
        url,
        data=dict(**file.dict()),
        params=dict(option_name=option_name, file_name=file_name),
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


async def job_input_file_upload(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobInputFileListResponse:
    """List uploaded input files for job"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/job/{id}/input/files".format(
        version=version, id=id
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobInputFileListResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_input_file_info_get(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobInputFileInfo:
    """Get job input file info"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/jobs/file/{id}".format(version=version, id=id)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobInputFileInfo}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def job_workflow_get(
    session: RundeckClient, entrypoint: str, version: int, id: String
) -> JobWorkflowGetResponse:
    """Get job workflow tree."""
    if version < 34:
        raise VersionError(f"Insufficient api version error, Required >34")
    url = entrypoint + "/api/{version}/job/{id}/workflow".format(version=version, id=id)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": JobWorkflowGetResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")
