"""Common fixtures for the agents module evals."""

import os
from typing import Any

import pytest
from autogen import UserProxyAgent


@pytest.fixture()
def llm_config(model: str | None = os.environ.get("OPENAI_API_MODEL")) -> dict[str, Any]:
    """Shared config for the LLMs."""
    return {
        "config_list": [
            {
                "model": model or "gpt-3.5-turbo",
                "api_key": os.environ["OPENAI_API_KEY"],
            }
        ],
        "cache_seed": None,
    }


@pytest.fixture()
def user_proxy(llm_config: dict[str, Any]) -> UserProxyAgent:
    """Create a user proxy agent for test-case uses."""
    return UserProxyAgent(
        name="Agent",
        description="Generic question-asker.",
        system_message="You ask questions",
        human_input_mode="NEVER",
        llm_config=llm_config,
    )
