"""Retriever of the relevant bits of resume."""

from typing import Any, Literal

# from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent  # noqa: ERA001
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

_DEFAULT_RESUME_RETRIEVER_PROMPT = """
Your role is to extract the key information from the resume that's relevant to the job description
and the cover letter. Specifically, that means the following:

- **Experience**: Relevant work experience that matches the job requirements.
- **Skills**: Key skills that are important for the job.
- **Education**: Relevant degrees or certifications.
- **Projects**: Notable projects that demonstrate said skills.
- **Achievements**: Awards or recognitions that highlight your abilities.

Reformat all retrieved information into bullet points and provide it to the Writer.
""".strip()


class ResumeRetriever(RetrieveUserProxyAgent):
    """An agent that retrieves the relevant bits of resume."""

    def __init__(self, llm_config: dict[str, Any] | Literal[False], **kwargs: Any) -> None:
        super().__init__(
            name="Resume_Retriever",
            description="An agent that retrieves the relevant bits of resume.",
            # system_message=_DEFAULT_RESUME_RETRIEVER_PROMPT,  # noqa: ERA001
            llm_config=llm_config,
            human_input_mode="NEVER",
            retrieve_config={
                "task": "qa",
                "docs_path": "resume/",
                # TODO: Define smarter chunking
            },
            **kwargs,
        )
