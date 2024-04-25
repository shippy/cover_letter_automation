"""Evals for the Critic agent."""

from pathlib import Path
from typing import Any

import pytest
from autogen import UserProxyAgent
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from tests.cover_letter_automation.agents.utils import LLMTestCaseInput, get_chat_outcome

from cover_letter_automation.agents import Critic


@pytest.fixture()
def critic_agent(llm_config: dict[str, Any]) -> Critic:
    """Instantiate the Critic agent for test purposes."""
    return Critic(llm_config)


@pytest.fixture()
def normal_cases(user_proxy: UserProxyAgent, critic_agent: Critic) -> list[LLMTestCase]:
    """Convert the loaded case files int LLMTestCases."""
    _normal_cases = LLMTestCaseInput.load_from_file(Path(__file__).parent / "inputs/critic/normal_inputs.yaml")
    return [
        LLMTestCase(input=case.get_input(), actual_output=get_chat_outcome(user_proxy, critic_agent, case.get_input()))
        for case in _normal_cases
    ]


@pytest.fixture()
def normal_cases_dataset(normal_cases: list[LLMTestCase]) -> EvaluationDataset:
    """Convert the loaded LLMTestCases into an EvaluationDataset."""
    return EvaluationDataset(test_cases=normal_cases)


@pytest.fixture()
def language_errors(user_proxy: UserProxyAgent, critic_agent: Critic) -> list[LLMTestCase]:
    """Convert the loaded case files int LLMTestCases."""
    _language_cases = LLMTestCaseInput.load_from_file(Path(__file__).parent / "inputs/critic/language_errors.yaml")
    return [
        LLMTestCase(input=case.get_input(), actual_output=get_chat_outcome(user_proxy, critic_agent, case.get_input()))
        for case in _language_cases
    ]


@pytest.fixture()
def language_error_dataset(language_errors: list[LLMTestCase]) -> EvaluationDataset:
    """Convert the loaded LLMTestCases into an EvaluationDataset."""
    return EvaluationDataset(test_cases=language_errors)


def test_critic_catches_language_errors(language_error_dataset: EvaluationDataset) -> None:
    """When given a cover letter with errors in language and grammar, the Critic should note these."""
    g_eval_metric = GEval(
        name="Language criticism present",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=["Feedback from the actual output points out the spelling and/or grammar errors."],
    )
    for test_case in language_error_dataset:
        assert_test(test_case, metrics=[g_eval_metric])


def test_critic_writes_good_critique(normal_cases_dataset: EvaluationDataset) -> None:
    """Evaluate that output makes sense."""
    g_eval_metric = GEval(
        name="Good criticism present",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "Feedback is structured into several points.",
            "Each point is meaningful, constructive, and well-made.",
        ],
    )
    for test_case in normal_cases_dataset.test_cases:
        assert_test(test_case, metrics=[g_eval_metric])


# def test_critic_catches_conceptual_errors(
#     user_proxy: UserProxyAgent, critic_agent: Critic, test_case: LLMTestCase
# ) -> None:
#     """When given a cover letter that over-focuses on a particular step, the Critic should note this."""
