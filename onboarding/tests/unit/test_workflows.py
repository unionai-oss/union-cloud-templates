"""Unit tests for Flyte workflows."""

from typing import Any, Callable, Dict, NamedTuple, Tuple, Type

import pytest
from sklearn.linear_model import LogisticRegression

from workflows import (
    example_00_intro,
    example_01_dynamic,
    example_02_map_task,
    example_03_plugins,
    example_04_type_system,
    example_05_pandera_types,
    example_06_reproducibility,
    example_07_caching,
    example_08_recover_executions,
    example_09_checkpointing,
    example_10_flyte_decks,
    example_11_extend_flyte_decks,
)


class WorkflowCase(NamedTuple):
    workflow: Callable
    inputs: Dict[str, Any]
    expected_output_types: Tuple[Type, ...]


@pytest.mark.parametrize(
    "wf_case",
    [
        WorkflowCase(
            workflow=example_00_intro.training_workflow,
            inputs={"hyperparameters": example_00_intro.Hyperparameters(C=0.1, max_iter=5000)},
            expected_output_types=(LogisticRegression, float, float),
        ),
    ]
)
def test_workflow(wf_case: WorkflowCase):
    output = wf_case.workflow(**wf_case.inputs)
    for output, expected_type in zip(output, wf_case.expected_output_types):
        assert isinstance(output, expected_type)
