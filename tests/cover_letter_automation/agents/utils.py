"""General utilities for evals."""

import contextlib
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, TypeVar

import yaml
from autogen import Agent, UserProxyAgent
from pydantic import BaseModel, Field, ValidationError

AnyAgent = TypeVar("AnyAgent", bound=Agent)

_DEFAULT_LLM_CONFIG = {
    "config_list": [
        {
            "model": os.environ.get("OPENAI_API_MODEL") or "gpt-4-turbo-preview",
            "api_key": os.environ["OPENAI_API_KEY"],
        }
    ],
    "cache_seed": None,
}


def make_agent(agent: AnyAgent, llm_config: dict[str, Any] = _DEFAULT_LLM_CONFIG, **kwargs: Any) -> Agent:
    """Instantiate an agent for test purposes."""
    _llm_config = deepcopy(llm_config)
    return agent(_llm_config, **kwargs)


def get_chat_outcome(user_proxy: UserProxyAgent, agent_under_test: Agent, message: str) -> str:
    """Get the outcome of a two-agent chat."""
    result = user_proxy.initiate_chat(
        recipient=agent_under_test, message=message, clear_history=True, max_turns=1, summary_method="last_msg"
    )

    return str(result.summary)


class LLMTestCaseInput(BaseModel):
    """Definition of the test case ingredients pulled from a JSON."""

    jd_extract: str
    resume_extract: str
    cover_letter_draft: str | None = Field(None, description="Optional draft of a cover letter")

    def get_input(self) -> str:
        """Create a single-shot input in lieu of a longer simulated conversation."""
        result = f"""Relevant items from the job description are here: \n\n{self.jd_extract}\n
        Relevant items from the resume are here: \n\n{self.resume_extract}"""
        if self.cover_letter_draft:
            result += f"\n\nThe cover letter draft is here: \n\n{self.cover_letter_draft}"

        return result

    @staticmethod
    def load_from_file(input_path: Path) -> list["LLMTestCaseInput"]:
        """Load the test case inputs from a YAML or JSON file."""
        with input_path.open("r") as f:
            if input_path.suffix in {".yml", ".yaml"}:
                all_inputs = yaml.safe_load(f)
            elif input_path.suffix in {".json", ".jsonl"}:
                all_inputs = json.load(f)

        outputs = []
        for each in all_inputs:
            with contextlib.suppress(ValidationError):
                outputs.append(LLMTestCaseInput(**each))

        return outputs
