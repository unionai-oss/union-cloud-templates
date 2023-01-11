"""Script to run all the workflows on a remote Flyte cluster.

NOTE: This script assumes that:
1. You have the appropriate configuration to run executions on the remote cluster.
2. The workflows are registered in the cluster.
"""

from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
from pathlib import Path

from workflows.example_00_intro import Hyperparameters


remote = FlyteRemote(
    config=Config.auto(config_file=str(Path.home() / ".uctl" / "config.yaml")),
    default_project="onboarding",
    default_domain="development",
)

WORKFLOWS = [
    (
        "workflows.example_00_intro.training_workflow",
        {"hyperparameters": Hyperparameters(C=0.1, max_iter=5000)},
    )
]


def run_workflow(wf_name: str, inputs: dict):
    flyte_wf = remote.fetch_workflow(name=wf_name)
    execution = remote.execute(flyte_wf, inputs=inputs)
    url = remote.generate_console_url(execution)
    print(f"Running workflow execution in: {url}")


def run_all():
    for wf_name, inputs in WORKFLOWS:
        run_workflow(wf_name, inputs)


if __name__ == "__main__":
    run_all()
