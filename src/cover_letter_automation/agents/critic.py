"""A Cover Letter Critic Agent."""

from typing import Any, Literal

from autogen import ConversableAgent, register_function

from cover_letter_automation.tools import export_letter

_DEFAULT_CRITIC_PROMPT = """
Your role is to make the cover letter better. In particular, you should focus on the following
aspects:

- **Clarity**: Is the cover letter easy to read and understand?
- **Relevance**: Does the cover letter address the job requirements and company needs?
- **Engagement**: Does the cover letter grab the reader's attention and make them want to learn
  more?
- **Tone**: Does the cover letter have a unique voice? Can you suggest an unusual turn of phrase?
- **Completeness**: Does the cover letter provide all the information required by the job
  description?
- **Within-paragraph coherence**: Does each paragraph have a clear focus and purpose?
- **Between-paragraph coherence**: Does the cover letter flow smoothly from one paragraph to the
  next?
- **Grammar and spelling**: Are there any errors in grammar, punctuation, or spelling? If so, give
  specific examples and instructions on correcting them.

You should provide constructive feedback on how to improve the cover letter in these areas. Provide
a bullet-point list of suggestions for the writer to consider. You don't need to address every area
- feel free to omit any that cannot be improved any further.

You should *not* require the letter writer to go beyond the information in the resume.

Feel free to repeat the critique if it continues to apply, or come up with a new one. You're allowed
to deliver multiple rounds of critique.

If there are no substantial issues with the cover letter, or if the Cover_Letter_Writer refuses to
make any more versions, you should use the `export_letter` tool to save the last draft of the cover
letter and terminate the group chat. You should also terminate if the Cover_Letter_Writer has
already exported the cover letter.

If you're asking questions that don't yet have answers in the current context, pass them along to
Client.
""".strip()


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
