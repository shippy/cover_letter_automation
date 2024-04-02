"""Stand-in (& human-in-the-loop) for the cover-letter originator."""

from autogen import UserProxyAgent


class CoverLetterClient(UserProxyAgent):
    """Stand-in for human in the loop."""

    def __init__(self) -> None:
        super().__init__(
            name="Myself",
            description="Stand-in for human in the loop.",
            human_input_mode="ALWAYS",
            llm_config=False,
        )
