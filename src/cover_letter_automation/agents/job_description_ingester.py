"""An agent that extracts information from job descriptions."""

from typing import Any

from autogen import ConversableAgent

_DEFAULT_JOB_DESCRIPTION_PROMPT = """
Your role is to extract the key information from the job description that's relevant to the cover
letter. Specifically, that means the following:
""".strip()


class JobDescriptionIngester(ConversableAgent):
    """An agent that extracts information from job descriptions."""

    def __init__(self, **kwargs: Any):
        """Initialize the agent."""
        super().__init__(
            name="Job_Description_Ingester",
            description="An agent that extracts information from job descriptions.",
            system_message=_DEFAULT_JOB_DESCRIPTION_PROMPT,
            human_input_mode="NEVER",
            **kwargs,
        )
