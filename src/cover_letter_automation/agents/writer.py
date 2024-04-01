"""An agent that writes and improves the cover letter based on assignment and feedback."""

from typing import Any

from autogen import ConversableAgent, register_function
from autogen.agentchat.contrib.capabilities.teachability import Teachability

from cover_letter_automation.tools import export_letter

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
- **Correctness**: You should only use information retrieved from the resume. Under no circumstances
  should you make anything up.
- **Completeness**: Ensure that the cover letter contains all the requirements the job description
  asks for.
- **Whimsical tone**: Be professional, but not *too* formal. Try unusual turns of phrase, but avoid
  cliches (e.g. "since the dawn of time"/"since the outset of my career"). Use few adjectives and
  no adverbs unless necessary.

Skip the header; address the cover letter to Sir/Madam unless the job description indicated
otherwise.

You should avoid hyperbole and cliches, keep things brief and to the point, and always draw a
connection between the resume and the job description requirements.

If you can no longer improve the cover letter, use the `export_letter` function to save it.
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

        # Let Writer save the cover letter to a file, too.
        register_function(
            export_letter,
            name="export_letter",
            description="Export the latest cover letter in Markdown to a file path and output that path.",
            caller=self,
            executor=self,
        )

        # Instantiate a Teachability object. Its parameters are all optional.
        teachability = Teachability(
            reset_db=True,  # Use True to force-reset the memo DB, and False to use an existing DB.
        )

        # Now add teachability to the agent.
        teachability.add_to_agent(self)
