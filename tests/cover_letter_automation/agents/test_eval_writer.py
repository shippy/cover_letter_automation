"""Evals for the Writer agent."""

from pathlib import Path

import pytest
from autogen import UserProxyAgent
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from tests.cover_letter_automation.agents.utils import LLMTestCaseInput, get_chat_outcome, make_agent

from cover_letter_automation.agents import Writer

_user_proxy = make_agent(UserProxyAgent, description="Generic question-asker.", human_input_mode="NEVER")
_writer_agent = make_agent(Writer)


def _make_writer_dataset(file_name: str) -> EvaluationDataset:
    fpath = Path(__file__).parent / f"inputs/writer/{file_name}"
    return EvaluationDataset(
        test_cases=[
            LLMTestCase(
                input=case.get_input(),
                actual_output=get_chat_outcome(_user_proxy, _writer_agent, case.get_input()),
            )
            for case in LLMTestCaseInput.load_from_file(fpath)
        ],
    )


_uncritiqued_cases_dataset = _make_writer_dataset("normal_inputs.yaml")


@pytest.mark.eval()
@pytest.mark.parametrize("test_case", _uncritiqued_cases_dataset)
def test_writer_generates_cover_letter(test_case: LLMTestCase) -> None:
    """Test that the writer agent generates a cover letter."""
    g_eval_metric = GEval(
        name="Cover letter generated",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "The cover letter in actual output incorporates the input information.",
            "The cover letter in actual output is structured in several paragraphs.",
            "Each paragraph in the cover letter in actual output is meaningful and well-made.",
        ],
    )
    assert_test(test_case, metrics=[g_eval_metric])


_critiqued_cases_dataset = _make_writer_dataset("critiqued_inputs.yaml")


@pytest.mark.eval()
@pytest.mark.parametrize("test_case", _critiqued_cases_dataset)
def test_writer_generates_cover_letter_against_critique(test_case: LLMTestCase) -> None:
    """Test that the writer agent generates a cover letter conforming to the criticism."""
    g_eval_metric = GEval(
        name="Cover letter generated against critique",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        evaluation_steps=[
            "The cover letter in actual output is structured in several paragraphs.",
            "The cover letter in actual output incorporates the criticisms from the input.",
        ],
    )
    assert_test(test_case, metrics=[g_eval_metric])
