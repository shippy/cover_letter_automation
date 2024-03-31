"""An agent that finds information about companies."""

from typing import Any

from autogen.agentchat.contrib.web_surfer import WebSurferAgent

_DEFAULT_WEB_SURFER_PROMPT = """
Your role is to find the information outside of the job description that's pertinent to know about
the company that issued it. This could include the company's mission, values, and culture, as well as
any recent news or events that might be relevant. You can also look up the company's competitors to
gain a better understanding of the industry landscape.

You should return a summary of the information you find, along with any relevant links or sources.
""".strip()


class CompanyResearcher(WebSurferAgent):
    """A web surfer agent that finds information about companies."""

    def __init__(self, bing_config: dict[str, Any], **kwargs: Any) -> None:
        super().__init__(
            name="Company_Researcher",
            description="A web surfer agent that finds information about companies.",
            system_message=_DEFAULT_WEB_SURFER_PROMPT,
            human_input_mode="NEVER",
            browser_config=bing_config,
            **kwargs,
        )
