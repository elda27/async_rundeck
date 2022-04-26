# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError


class SystemIncompleteLogStorageExecutionsResumeResponse(BaseModel):
    resumed: Optional[Boolean] = Field(alias="resumed")


class SystemExecutionsEnableResponse(BaseModel):
    execution_mode: Optional[String] = Field(alias="executionMode")


class SystemExecutionsDisableResponse(BaseModel):
    execution_mode: Optional[String] = Field(alias="executionMode")


class SchedulerTakeoverRequest(BaseModel):
    server: Optional[Object] = Field(alias="server")
    project: Optional[String] = Field(alias="project")
    job: Optional[Object] = Field(alias="job")


class SystemAclPolicyCreateRequest(BaseModel):
    contents: String = Field(alias="contents")


class SystemAclPolicyUpdateRequest(BaseModel):
    contents: String = Field(alias="contents")


async def system_info_get(
    session: RundeckClient, entrypoint: str, version: int
) -> SystemInfo:
    """Get Rundeck server information and stats"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/info".format(version=version)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": SystemInfo}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_log_storage_info_get(
    session: RundeckClient, entrypoint: str, version: int
) -> LogStorage:
    """Get Log Storage information and stats"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/logstorage".format(version=version)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": LogStorage}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_incomplete_log_storage_executions_get(
    session: RundeckClient, entrypoint: str, version: int
) -> IncompleteLogExecutions:
    """List all executions with incomplete log storage"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/logstorage/incomplete".format(
        version=version
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": IncompleteLogExecutions}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_incomplete_log_storage_executions_resume(
    session: RundeckClient, entrypoint: str, version: int
) -> SystemIncompleteLogStorageExecutionsResumeResponse:
    """Resume processing incomplete Log Storage uploads"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/logstorage/incomplete/resume".format(
        version=version
    )
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {
                    "200": SystemIncompleteLogStorageExecutionsResumeResponse
                }[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_executions_enable(
    session: RundeckClient, entrypoint: str, version: int
) -> SystemExecutionsEnableResponse:
    """Enables executions, allowing adhoc and manual and scheduled jobs to be run"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/executions/enable".format(version=version)
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": SystemExecutionsEnableResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_executions_disable(
    session: RundeckClient, entrypoint: str, version: int
) -> SystemExecutionsDisableResponse:
    """Disables executions, preventing adhoc and manual and scheduled jobs from running."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/executions/disable".format(
        version=version
    )
    async with session.request("POST", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": SystemExecutionsDisableResponse}[
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


async def system_scheduler_takeover(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    *,
    scheduler_takeover_request: Optional[SchedulerTakeoverRequest] = None,
) -> TakeoverScheduleResponse:
    """Tell a Rundeck server in cluster mode to claim all scheduled jobs from another cluster server"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/scheduler/takeover".format(version=version)
    async with session.request(
        "PUT", url, data=dict(**scheduler_takeover_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": TakeoverScheduleResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_scheduled_jobs_for_server(
    session: RundeckClient, entrypoint: str, version: int, uuid: String
) -> List[Job]:
    """List the scheduled Jobs with their schedule owned by the cluster server with the specified UUID"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/scheduler/server/{uuid}/jobs".format(
        version=version, uuid=uuid
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
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


async def system_scheduled_jobs_list(
    session: RundeckClient, entrypoint: str, version: int
) -> List[Job]:
    """List the scheduled Jobs with their schedule owned by the cluster server"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/scheduler/jobs".format(version=version)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
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


async def system_acl_policy_list(
    session: RundeckClient, entrypoint: str, version: int
) -> Union[AclList, None]:
    """List ACL Policies"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/acl/".format(version=version)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": AclList, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_acl_policy_get(
    session: RundeckClient, entrypoint: str, version: int, policy_name: String
) -> Union[AclPolicyResponse, None]:
    """Retrieve the YAML texas of the ACL Policy file"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/acl/{policyName}".format(
        version=version, policy_name=policy_name
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": AclPolicyResponse, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_acl_policy_create(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    policy_name: String,
    *,
    system_acl_policy_create_request: Optional[SystemAclPolicyCreateRequest] = None,
) -> Union[AclPolicyResponse, None, InvalidAclPolicyResponse]:
    """Create a policy"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/acl/{policyName}".format(
        version=version, policy_name=policy_name
    )
    async with session.request(
        "POST", url, data=dict(**system_acl_policy_create_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {
                    "201": AclPolicyResponse,
                    "409": None,
                    "400": InvalidAclPolicyResponse,
                }[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_acl_policy_update(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    policy_name: String,
    *,
    system_acl_policy_update_request: Optional[SystemAclPolicyUpdateRequest] = None,
) -> Union[AclPolicyResponse, None]:
    """Update policy"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/acl/{policyName}".format(
        version=version, policy_name=policy_name
    )
    async with session.request(
        "PUT", url, data=dict(**system_acl_policy_update_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": AclPolicyResponse, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def system_acl_policy_delete(
    session: RundeckClient, entrypoint: str, version: int, policy_name: String
) -> Union[None, None]:
    """Delete policy"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/system/acl/{policyName}".format(
        version=version, policy_name=policy_name
    )
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
