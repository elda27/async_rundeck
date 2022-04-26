# DON'T CHANGE MANUALLY THIS FILE.
# This file is generated from https://github.com/rundeck/rundeck-api-specs
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, parse_obj_as
from async_rundeck.proto.json_types import Integer, Number, String, Boolean, Object
from async_rundeck.client import RundeckClient
from async_rundeck.exceptions import RundeckError, VersionError


class ProjectCreateRequest(BaseModel):
    name: Optional[String] = Field(alias="name")
    config: Optional[Object] = Field(alias="config")


class ProjectConfigKeyGetResponse(BaseModel):
    key: Optional[String] = Field(alias="key")
    value: Optional[String] = Field(alias="value")


class ProjectConfigKeySetResponse(BaseModel):
    key: Optional[String] = Field(alias="key")
    value: Optional[String] = Field(alias="value")


class ProjectConfigKeySetRequest(BaseModel):
    value: Optional[String] = Field(alias="value")


class ProjectReadmeGetResponse(BaseModel):
    contents: Optional[String] = Field(alias="contents")


class ReadmeUpdateRequest(BaseModel):
    contents: Optional[String] = Field(alias="contents")


class ProjectMotdGetResponse(BaseModel):
    contents: Optional[String] = Field(alias="contents")


class MotdUpdateRequest(BaseModel):
    contents: Optional[String] = Field(alias="contents")


async def project_list(
    session: RundeckClient, entrypoint: str, version: int
) -> List[Object]:
    """List projects"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/projects".format(version=version)
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": List[Object]}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_create(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project_create_request: ProjectCreateRequest,
) -> Union[Object, None]:
    """Create a new project"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/projects".format(version=version)
    async with session.request(
        "POST", url, data=dict(**project_create_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"201": Object, "409": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_get(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> Union[Project, None]:
    """Get information about a project"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}".format(
        version=version, project=project
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": Project, "404": None}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_delete(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> None:
    """Delete project"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}".format(
        version=version, project=project
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_config_get(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> Union[Object, None]:
    """Get project config"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/config".format(
        version=version, project=project
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_config_update(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    project_config_update_request: Object,
) -> None:
    """Update project config"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/config".format(
        version=version, project=project
    )
    async with session.request(
        "PUT", url, data=dict(**project_config_update_request.dict()), params=dict()
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


async def project_config_key_get(
    session: RundeckClient, entrypoint: str, version: int, project: String, key: String
) -> ProjectConfigKeyGetResponse:
    """Get project config key"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/config/{key}".format(
        version=version, project=project, key=key
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ProjectConfigKeyGetResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_config_key_set(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    key: String,
    project_config_key_set_request: ProjectConfigKeySetRequest,
) -> ProjectConfigKeySetResponse:
    """Get project config key"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/config/{key}".format(
        version=version, project=project, key=key
    )
    async with session.request(
        "PUT", url, data=dict(**project_config_key_set_request.dict()), params=dict()
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ProjectConfigKeySetResponse}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_config_key_delete(
    session: RundeckClient, entrypoint: str, version: int, project: String, key: String
) -> None:
    """Delete project config key"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/config/{key}".format(
        version=version, project=project, key=key
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_jobs_export(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    *,
    format: Optional[String] = "xml",
    idlist: Optional[String] = None,
    group_path: Optional[String] = None,
    job_filter: Optional[String] = None,
) -> String:
    """Export the job definitions in XML or YAML formats."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/jobs/export".format(
        version=version, project=project
    )
    async with session.request(
        "GET",
        url,
        data=dict(),
        params=dict(
            format=format, idlist=idlist, group_path=group_path, job_filter=job_filter
        ),
    ) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": String}[response.status]
                if issubclass(response_type, BaseModel):
                    return parse_obj_as(response_type, obj)
                else:
                    return response_type(obj)
            except KeyError:
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_jobs_import(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    file: Object,
    *,
    content_type: Optional[String] = "application/xml",
    accept: Optional[String] = "application/xml",
    file_format: Optional[String] = "xml",
    dupe_option: Optional[String] = "create",
    uuid_option: Optional[String] = "preserve",
) -> Object:
    """Import job definitions in XML or YAML formats."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/jobs/import".format(
        version=version, project=project
    )
    async with session.request(
        "POST",
        url,
        data=dict(**file.dict()),
        params=dict(
            file_format=file_format, dupe_option=dupe_option, uuid_option=uuid_option
        ),
    ) as response:
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


async def project_archive_import(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    file: Object,
    *,
    job_uuid_option: Optional[String] = "remove",
    import_executions: Optional[Boolean] = None,
    import_config: Optional[Boolean] = None,
    import_a_c_l: Optional[Boolean] = None,
) -> None:
    """Import project archive."""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/import".format(
        version=version, project=project
    )
    async with session.request(
        "PUT",
        url,
        data=dict(**file.dict()),
        params=dict(
            job_uuid_option=job_uuid_option,
            import_executions=import_executions,
            import_config=import_config,
            import_a_c_l=import_a_c_l,
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


async def project_archive_export_sync(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    *,
    execution_ids: Optional[Boolean] = None,
    export_all: Optional[Boolean] = True,
    export_jobs: Optional[Boolean] = None,
    export_executions: Optional[Boolean] = None,
    export_configs: Optional[Boolean] = None,
    export_readmes: Optional[Boolean] = None,
    export_acls: Optional[Boolean] = None,
) -> Object:
    """Export archive of project synchronously"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/export".format(
        version=version, project=project
    )
    async with session.request(
        "GET",
        url,
        data=dict(),
        params=dict(
            execution_ids=execution_ids,
            export_all=export_all,
            export_jobs=export_jobs,
            export_executions=export_executions,
            export_configs=export_configs,
            export_readmes=export_readmes,
            export_acls=export_acls,
        ),
    ) as response:
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


async def project_readme_get(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> Union[ProjectReadmeGetResponse, None]:
    """Get the readme.md contents"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/readme.md".format(
        version=version, project=project
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ProjectReadmeGetResponse, "404": None}[
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


async def project_readme_put(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    readme_update_request: ReadmeUpdateRequest,
) -> None:
    """Create or modify project README.md"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/readme.md".format(
        version=version, project=project
    )
    async with session.request(
        "PUT", url, data=dict(**readme_update_request.dict()), params=dict()
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


async def project_readme_delete(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> None:
    """Delete project README.md"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/readme.md".format(
        version=version, project=project
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")


async def project_motd_get(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> Union[ProjectMotdGetResponse, None]:
    """Get the readme.md contents"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/motd.md".format(
        version=version, project=project
    )
    async with session.request("GET", url, data=dict(), params=dict()) as response:
        obj = await response.text()
        if response.ok():
            try:
                response_type = {"200": ProjectMotdGetResponse, "404": None}[
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


async def project_motd_put(
    session: RundeckClient,
    entrypoint: str,
    version: int,
    project: String,
    motd_update_request: MotdUpdateRequest,
) -> None:
    """Create or modify project MOTD.md"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/motd.md".format(
        version=version, project=project
    )
    async with session.request(
        "PUT", url, data=dict(**motd_update_request.dict()), params=dict()
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


async def project_motd_delete(
    session: RundeckClient, entrypoint: str, version: int, project: String
) -> None:
    """Delete project motd.md"""
    if version < 26:
        raise VersionError(f"Insufficient api version error, Required >26")
    url = entrypoint + "/api/{version}/project/{project}/motd.md".format(
        version=version, project=project
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
                raise RundeckError("Unknwon response code: {url}({response.status})")
        else:
            raise RundeckError(f"Connection diffused: {url}({response.status})\n{obj}")
