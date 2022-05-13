import asyncio
from pathlib import Path
from uuid import uuid4
import pytest
from async_rundeck.rundeck import Rundeck, RundeckError
from tests.common import *


root_dir = Path(__file__).parent


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

    # Run job
    execution = await rundeck.execute_job(jobs[0].id)
    assert execution is not None

    # List executions
    executions = await rundeck.list_running_executions(project_name)
    assert executions is not None and len(executions.executions) > 0
    last_execution_id = executions.executions[0].id

    await asyncio.sleep(2)
    executions = await rundeck.list_running_executions(project_name)
    assert executions is not None and len(executions.executions) == 0

    # Get last executions
    execution = await rundeck.get_execution(last_execution_id)
    assert execution is not None and execution.id == last_execution_id

    # Remove delete executions
    await rundeck.delete_execution(last_execution_id)
