"""An agent that extracts information from job descriptions."""

from typing import Any

from autogen import ConversableAgent

_DEFAULT_JOB_DESCRIPTION_PROMPT = """
You're responding to a job ad that's as follows:

```
{job_description}
```

Your role is to extract the key information from the job description that's relevant to the cover
letter. Specifically, that means the following:

- **Requirements**: The skills, experience, and qualifications the job is looking for.
- **Responsibilities**: The tasks and duties you'll be expected to perform.
- **Company**: The name and information about the company that's hiring.
""".strip()

# TODO: Define a Pydantic output format that summarizes the job description variables?


class JobDescriptionIngester(ConversableAgent):
    """An agent that extracts information from job descriptions."""

    def __init__(self, job_description: str, **kwargs: Any):
        """Initialize the agent."""
        super().__init__(
            name="Job_Description_Ingester",
            description="An agent that extracts information from job descriptions.",
            system_message=_DEFAULT_JOB_DESCRIPTION_PROMPT.format(job_description=job_description),
            human_input_mode="NEVER",
            **kwargs,
        )
