"""Script to run all the workflows on a remote Flyte cluster.

NOTE: This script assumes that:
1. You have the appropriate configuration to run executions on the remote cluster.
2. The workflows are registered in the cluster.
"""

import logging
import time

from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
from pathlib import Path

import pytest

from tests.common import WorkflowCase, WORKFLOW_CASES


logger = logging.getLogger(__name__)


SUCCEED_STATUS = 4


remote = FlyteRemote(
    config=Config.auto(config_file=str(Path.home() / ".uctl" / "config.yaml")),
    default_project="onboarding",
    default_domain="development",
)


@pytest.mark.parametrize("wf_case", WORKFLOW_CASES)
def test_workflow_remote(wf_case: WorkflowCase):
    for _ in range(60):
        # bypass issue where multiple remote objects are authenticating at the
        # same time.
        try:
            flyte_wf = remote.fetch_workflow(name=wf_case.workflow.name)
            break
        except OSError:
            time.sleep(1)

    execution = remote.execute(flyte_wf, inputs=wf_case.inputs)
    url = remote.generate_console_url(execution)
    logger.info(f"Running workflow {wf_case.workflow.name} at: {url}")
    execution = remote.wait(execution)
    assert execution.closure.phase == SUCCEED_STATUS
