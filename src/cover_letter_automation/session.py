"""Set up the group chat session."""

from copy import deepcopy
from typing import Any

from autogen import ChatResult, GroupChat, GroupChatManager, UserProxyAgent

from cover_letter_automation.agents import CompanyResearcher, Critic, JobDescriptionIngester, ResumeRetriever, Writer


def setup_and_start_session(
    *, llm_config: dict[str, Any], bing_config: dict[str, Any], job_description: str
) -> ChatResult:
    """Set up and start the group chat session."""
    client = UserProxyAgent(name="Myself", llm_config=deepcopy(llm_config))
    jd_ingester = JobDescriptionIngester(job_description=job_description, llm_config=deepcopy(llm_config))
    researcher = CompanyResearcher(llm_config=deepcopy(llm_config), bing_config=bing_config)
    resume_reader = ResumeRetriever(llm_config=deepcopy(llm_config))
    writer = Writer(llm_config=deepcopy(llm_config))
    critic = Critic(llm_config=deepcopy(llm_config))

    speaker_transitions = {
        # jd_ingester: [researcher],
        # researcher: [resume_reader],
        client: [jd_ingester],
        jd_ingester: [resume_reader],  # FIXME: Re-integrate researcher
        resume_reader: [writer],
        writer: [critic],
        critic: [writer],
    }

    group_chat = GroupChat(
        agents=speaker_transitions.keys(),
        messages=[],
        send_introductions=False,
        allowed_or_disallowed_speaker_transitions=speaker_transitions,
        speaker_transitions_type="allowed",
    )

    group_manager = GroupChatManager(
        groupchat=group_chat,
        name="Cover_Letter_Automation",
        llm_config=deepcopy(llm_config),
    )

    conversation = client.initiate_chat(
        recipient=group_manager,  # FIXME: Should be in a separate variable?
        message="Please start the extraction from the job description.",
        # summary_method="last_msg",
        clear_history=True,
    )

    return conversation
