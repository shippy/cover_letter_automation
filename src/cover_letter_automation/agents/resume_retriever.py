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
and the cover letter. Specifically, that means the following:

- **Experience**: Relevant work experience that matches the job requirements.
- **Skills**: Key skills that are important for the job.
- **Education**: Relevant degrees or certifications.
- **Projects**: Notable projects that demonstrate said skills.
- **Achievements**: Awards or recognitions that highlight your abilities.

Reformat all retrieved information into bullet points and provide it to the Writer.
""".strip()


class ResumeRetriever(ConversableAgent):
    """An agent that retrieves the relevant bits of resume."""

    def __init__(self, json_resume_path: Path, llm_config: dict[str, Any] | Literal[False], **kwargs: Any) -> None:
        with json_resume_path.open("r") as f:
            json_resume = json.load(f)
            minified_resume = json.dumps(json_resume, separators=(",", ":"))

        super().__init__(
            name="Resume_Retriever",
            description="An agent that retrieves the relevant bits of resume.",
            system_message=_DEFAULT_RESUME_RETRIEVER_PROMPT.format(json_resume=minified_resume),
            llm_config=llm_config,
            human_input_mode="NEVER",
            # retrieve_config={"task": "qa", "docs_path": "resume/", }  # noqa: ERA001
            # TODO: Define smarter chunking
            **kwargs,
        )
