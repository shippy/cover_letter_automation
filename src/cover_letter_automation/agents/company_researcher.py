"""An agent that finds information about companies."""

from typing import Any

from autogen.agentchat.contrib.web_surfer import WebSurferAgent

_DEFAULT_WEB_SURFER_PROMPT = """
Your role is to find the information outside of the job description that's pertinent to know about
the company that issued it. This could include the company's mission, values, and culture, as well
as any recent news or events that might be relevant. You can also look up the company's competitors
to gain a better understanding of the industry landscape.

If you've only just completed a search, you should pass it back to yourself and provide a brief
summary, or continue the search if you think there's more to find.

If you've already completed the search previously and found useful information, you should return a
tight summary of the information you find, along with any relevant links or sources. Pass this
summary to Resume_Retriever.
""".strip()


class CompanyResearcher(WebSurferAgent):
    """A web surfer agent that finds information about companies."""

    def __init__(self, llm_config: dict[str, Any], bing_config: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(
            name="Company_Researcher",
            description="A web surfer agent that finds information about companies.",
            system_message=_DEFAULT_WEB_SURFER_PROMPT,
            human_input_mode="NEVER",
            browser_config=bing_config,
            llm_config=llm_config,
            **kwargs,
        )
