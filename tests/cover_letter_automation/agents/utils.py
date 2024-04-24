"""General utilities for evals."""

from autogen import Agent, UserProxyAgent


def get_chat_outcome(user_proxy: UserProxyAgent, agent_under_test: Agent, message: str) -> str:
    """Get the outcome of a two-agent chat."""
    result = user_proxy.initiate_chat(
        recipient=agent_under_test, message=message, clear_history=True, max_turns=1, summary_method="last_msg"
    )

    return str(result.summary)
