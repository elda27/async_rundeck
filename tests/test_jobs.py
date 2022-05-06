from pathlib import Path
from uuid import uuid4
import pytest
from async_rundeck.rundeck import Rundeck
from tests.common import *

root_dir = Path(__file__).parent


@pytest.mark.asyncio
async def test_list_jobs(rundeck: Rundeck):
    project_name = uuid4().hex
    await rundeck.create_project(project_name)
    assert len(await rundeck.list_jobs(project_name)) == 0


@pytest.mark.asyncio
async def test_import_job_by_xml(rundeck: Rundeck):
    project_name = uuid4().hex
    await rundeck.create_project(project_name)
    status = await rundeck.import_jobs(
        project_name,
        (root_dir / "resource" / "Test_job.xml").read_text(),
        content_type="application/xml",
        uuid_option="remove",
    )
    assert len(status["succeeded"]) == 1


@pytest.mark.asyncio
async def test_import_job_by_yaml(rundeck: Rundeck):
    project_name = uuid4().hex
    await rundeck.create_project(project_name)
    status = await rundeck.import_jobs(
        project_name,
        (root_dir / "resource" / "Test_job.yaml").read_text(),
        content_type="application/yaml",
        uuid_option="remove",
    )
    assert len(status["succeeded"]) == 1


# @pytest.mark.asyncio
# async def test_import_job_by_multipart_form_data(rundeck: Rundeck):
#     project_name = uuid4().hex
#     await rundeck.create_project(project_name)
#     status = await rundeck.import_jobs(
#         project_name,
#         (root_dir / "resource" / "Test_job.xml").read_text(),
#         content_type="multipart/form-data",
#         uuid_option="remove",
#     )
#     assert len(status["succeeded"]) == 1


@pytest.mark.asyncio
async def test_export_job(rundeck: Rundeck):
    import xmltodict

    project_name = uuid4().hex
    await rundeck.create_project(project_name)
    job_content = (root_dir / "resource" / "Test_job.xml").read_text()
    status = await rundeck.import_jobs(
        project_name,
        job_content,
        content_type="application/xml",
        uuid_option="remove",
    )
    assert len(status["succeeded"]) == 1

    # Test export
    export_job = await rundeck.export_jobs(
        project_name,
    )

    import_job = xmltodict.parse(job_content)
    export_job = xmltodict.parse(export_job)

    assert len(import_job["joblist"]) == len(export_job["joblist"])


@pytest.mark.asyncio
async def test_execute_job(rundeck: Rundeck):
    project_name = uuid4().hex
    await rundeck.create_project(project_name)
    job_content = (root_dir / "resource" / "Test_job.xml").read_text()
    status = await rundeck.import_jobs(
        project_name,
        job_content,
        content_type="application/xml",
        uuid_option="remove",
    )
    assert len(status["succeeded"]) == 1

    jobs = await rundeck.list_jobs(project_name)

    # Test run job
    execution = await rundeck.run_job(jobs[0].id)
    assert execution is not None
