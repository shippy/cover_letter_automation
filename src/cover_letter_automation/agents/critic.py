"""A Cover Letter Critic Agent."""

from pathlib import Path
from typing import Annotated, Any, Literal

from autogen import ConversableAgent, register_function

_DEFAULT_CRITIC_PROMPT = """
Your role is to make the cover letter better. In particular, you should focus on the following
aspects:

- **Clarity**: Is the cover letter easy to read and understand?
- **Relevance**: Does the cover letter address the job requirements and company needs?
- **Engagement**: Does the cover letter grab the reader's attention and make them want to learn
  more?
- **Whimsy**: Does the cover letter have a unique voice or perspective that sets it apart?
- **Completeness**: Does the cover letter provide all the information required by the job
  description?
- **Gotcha avoidance**: Does the cover letter avoid common pitfalls and cliches? Does it contain
  everything the job description explicitly said it should?

You should provide constructive feedback on how to improve the cover letter in these areas. Provide
a bullet-point list of suggestions for the writer to consider.

Feel free to repeat the critique if it continues to apply, or come up with a new one. You're allowed
to deliver multiple rounds of critique.

If there are no substantial issues with the cover letter, or if the Cover_Letter_Writer refuses to
make any more versions, you should use the `export_letter` tool to save the last draft of the cover
letter and terminate the group chat.
""".strip()
# - **Professionalism**: Is the cover letter well-written and free of errors?


def export_letter(
    cover_letter: Annotated[str, "Full text of the cover letter, formatted in Markdown"],
    filename: Annotated[
        str,
        "Name of the file to save the cover letter to, preferably in the format `[YY MM] company_lowercase__surname.md`",
    ],
    path: Annotated[str, "Folder in which to save the file"] = "cover_letters/",
) -> str:
    """Export a cover letter to a file path and output that path."""
    target_path = Path(path)
    if not target_path.exists():
        target_path.mkdir(parents=True)
    target = target_path / filename
    target.touch()
    with target.open(mode="w") as f:
        f.write(cover_letter)
    return str(target.absolute())


class Critic(ConversableAgent):
    """A conversational agent that provides feedback on cover letters."""

    def __init__(
        self,
        llm_config: dict[str, Any] | Literal[False],
        **kwargs: Any,
    ) -> None:
        super().__init__(
            name="Cover_Letter_Critic",
            description="A conversational agent that provides feedback on cover letters.",
            system_message=_DEFAULT_CRITIC_PROMPT,
            human_input_mode="TERMINATE",
            llm_config=llm_config,
            **kwargs,
        )

        register_function(
            export_letter,
            caller=self,
            executor=self,
            name="export_letter",
            description="Export a cover letter in Markdown to a file path and output that path.",
        )
