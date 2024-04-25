"""Evals for the Critic agent."""

from pathlib import Path

import pytest
from autogen import UserProxyAgent
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from tests.cover_letter_automation.agents.utils import LLMTestCaseInput, get_chat_outcome, make_agent

from cover_letter_automation.agents import Critic

_user_proxy = make_agent(UserProxyAgent, description="Generic question-asker.", human_input_mode="NEVER")
_critic_agent = make_agent(Critic)


def _make_critic_dataset(file_name: str) -> EvaluationDataset:
    fpath = Path(__file__).parent / f"inputs/critic/{file_name}"
    return EvaluationDataset(
        test_cases=[
            LLMTestCase(
                input=case.get_input(),
                actual_output=get_chat_outcome(_user_proxy, _critic_agent, case.get_input()),
            )
            for case in LLMTestCaseInput.load_from_file(fpath)
        ],
    )


_normal_cases_dataset = _make_critic_dataset("normal_inputs.yaml")
_language_error_dataset = _make_critic_dataset("language_errors.yaml")


@pytest.mark.parametrize("test_case", _normal_cases_dataset)
def test_critic_writes_good_critique(test_case: LLMTestCase) -> None:
    """Evaluate that output makes sense."""
    g_eval_metric = GEval(
        name="Good criticism present",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "Feedback in the actual output relates to the cover letter in the input."
            "Feedback is structured into several points.",
            "Each point in the critique is meaningful, constructive, and well-made.",
        ],
    )
    assert_test(test_case, metrics=[g_eval_metric])


@pytest.mark.parametrize("test_case", _language_error_dataset)
def test_critic_catches_language_errors(test_case: LLMTestCase) -> None:
    """When given a cover letter with errors in language and grammar, the Critic should note these."""
    g_eval_metric = GEval(
        name="Language criticism present",
        # Skip LLMTestCaseParams.INPUT since the presence of issues there seems to confuse GEval.
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "Feedback in the actual output indicates the presence of spelling and/or grammar errors in the "
            "inputted cover letter (among other problems)."
        ],
    )
    assert_test(test_case, metrics=[g_eval_metric])
