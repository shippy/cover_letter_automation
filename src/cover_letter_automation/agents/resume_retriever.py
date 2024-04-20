"""Retriever of the relevant bits of resume."""

import json
from pathlib import Path
from typing import Any, Literal

# from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent  # noqa: ERA001
# from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent  # noqa: ERA001
from autogen import ConversableAgent

_DEFAULT_RESUME_RETRIEVER_PROMPT = """
The applicant's JSON resume follows:

```json
{json_resume}
```

Your role is to extract the key information from the resume that's relevant to the job description
(and later usable in the cover letter). Specifically, that means the following:

- **Name**: The applicant's name.
- **Experience**: Relevant work experience that matches the job requirements. Prefer more recent.
- **Skills**: Key skills that are also important for the job.
- **Education**: Relevant degrees or certifications.
- **Projects**: Notable projects that demonstrate said skills.

Don't retrieve experiences that aren't at least tangentially related to any of the job description
requirements.

Reformat all retrieved information into bullet points and provide it to the Writer.
""".strip()


class ResumeRetriever(ConversableAgent):
    """An agent that retrieves the relevant bits of resume."""

    def __init__(
        self, stringified_json_resume: str, llm_config: dict[str, Any] | Literal[False], **kwargs: Any
    ) -> None:
        """Create a resume retriever agent."""
        super().__init__(
            name="Resume_Retriever",
            description="An agent that retrieves the relevant bits of resume.",
            system_message=_DEFAULT_RESUME_RETRIEVER_PROMPT.format(json_resume=stringified_json_resume),
            llm_config=llm_config,
            human_input_mode="NEVER",
            **kwargs,
        )

    @staticmethod
    def read_json_resume(json_resume_path: Path) -> str:
        """Read the JSON resume from the given path."""
        with json_resume_path.open("r") as f:
            content = json.load(f)
            minified_content = json.dumps(content, separators=(",", ":"))

        return minified_content
