"""An agent that writes and improves the cover letter based on assignment and feedback."""

from typing import Any

from autogen import ConversableAgent
from autogen.agentchat.contrib.capabilities.teachability import Teachability

# from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent  # noqa: ERA001


# - Attempt to retrieve relevant pieces of the resumé in response to either the requirements or the
#   feedback.
_DEFAULT_WRITER_PROMPT = """
Write a cover letter for the job description requirements provided by Job_Description_Ingester using
information from the Resume_Retriever and, if applicable, responsive to the feedback provided by
Critic. You should aim to address especially the following points:

- **Introduction**: A brief introduction that explains who you are and why you're interested in the
    position.
- **Relevance**: A discussion of how your skills and experience align with the job requirements.
- **Engagement**: A compelling argument for why you're the best candidate for the position.
- **Closing**: A conclusion that summarizes your interest and availability for the role.
- **Completeness**: Ensure that the cover letter contains all the requirements the job description
  asks for.
""".strip()


class Writer(ConversableAgent):
    """An agent that writes and improves the cover letter based on assignment and feedback."""

    def __init__(self, llm_config: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(
            name="Cover_Letter_Writer",
            description="An agent that writes and improves the cover letter based on assignment and feedback.",
            system_message=_DEFAULT_WRITER_PROMPT,
            human_input_mode="TERMINATE",
            llm_config=llm_config,
            **kwargs,
        )

        # Instantiate a Teachability object. Its parameters are all optional.
        teachability = Teachability(
            reset_db=False,  # Use True to force-reset the memo DB, and False to use an existing DB.
        )

        # Now add teachability to the agent.
        teachability.add_to_agent(self)
