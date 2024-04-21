"""Run evals for the resume retriever agent."""

import json
from copy import deepcopy
from typing import Any

import pytest
from autogen import Agent, UserProxyAgent
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from cover_letter_automation.agents.resume_retriever import ResumeRetriever


def get_chat_outcome(user_proxy: UserProxyAgent, agent_under_test: Agent, message: str) -> str:
    """Get the outcome of a two-agent chat."""
    result = user_proxy.initiate_chat(
        recipient=agent_under_test, message=message, clear_history=True, max_turns=1, summary_method="last_msg"
    )

    return str(result.summary)


@pytest.fixture()
def resume_retriever_agent(llm_config: dict[str, Any]) -> ResumeRetriever:
    """Create a resume retriever agent for test-case uses."""
    json_resume = {
        "basics": {
            "name": "Test Person",
            "label": "Data/LLM Generalist",
        },
        "work": [
            {
                "company": "OpenAI",
                "position": "Senior Data/LLM Generalist",
                "startDate": "2020-01-01",
                "endDate": "2022-01-01",
                "summary": "I did machine learning and nothing else.",
            },
            {
                "company": "ČEZ",
                "position": "Janitor",
                "startDate": "2019-01-01",
                "endDate": "2020-01-01",
                "summary": "I cleaned many offices and nothing else.",
            },
        ],
    }
    stringified_json_resume = json.dumps(json_resume, separators=(",", ":"))
    return ResumeRetriever(
        stringified_json_resume=stringified_json_resume,
        llm_config=deepcopy(llm_config),
    )


@pytest.mark.parametrize(
    ("job_description", "company"),
    [
        ("We are looking for a Senior Data/LLM Generalist to join our team.", "OpenAI"),
        ("We are looking for a Janitor to join our team.", "ČEZ"),
    ],
)
def test_relevant_content_retrieved(
    user_proxy: UserProxyAgent, resume_retriever_agent: ResumeRetriever, job_description: str, company: str
) -> None:
    """Test that the resume retriever agent retrieves the relevant content."""
    message = "Here is the job description: " + job_description
    chat_outcome = get_chat_outcome(user_proxy, resume_retriever_agent, message)

    assert_test(
        LLMTestCase(input=message, actual_output=chat_outcome, context=[company]),
        [
            GEval(
                name="Inclusion",
                evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
                threshold=0.7,
                evaluation_steps=[
                    f"Check that the output contains the company name '{company}'",
                    f"Check that the output does not contain any company name other than '{company}'",
                ],
            )
        ],
    )
