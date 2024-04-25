"""Set up the group chat session."""

from copy import deepcopy
from pathlib import Path
from typing import Any

from autogen import ChatResult, GroupChat, GroupChatManager

from cover_letter_automation.agents import (
    CompanyResearcher,
    CoverLetterClient,
    Critic,
    JobDescriptionIngester,
    ResumeRetriever,
    Writer,
)


def setup_and_start_session(
    *,
    llm_config: dict[str, Any],
    job_description: str,
    json_resume_path: Path,
    bing_config: dict[str, Any] | None = None,
) -> ChatResult:
    """Set up and start the group chat session."""
    client = CoverLetterClient()
    jd_ingester = JobDescriptionIngester(job_description=job_description, llm_config=deepcopy(llm_config))
    if bing_config is not None:
        researcher = CompanyResearcher(llm_config=deepcopy(llm_config), bing_config=bing_config)
    resume_reader = ResumeRetriever(
        llm_config=deepcopy(llm_config), stringified_json_resume=ResumeRetriever.read_json_resume(json_resume_path)
    )
    writer = Writer(llm_config=deepcopy(llm_config))
    critic = Critic(llm_config=deepcopy(llm_config))

    if bing_config is None:
        speaker_transitions = {
            client: [jd_ingester, critic],  # go straight to `critic` if chat closed without saving
            jd_ingester: [resume_reader],
            resume_reader: [writer],
            writer: [critic],
            critic: [writer, client],
        }
    else:
        speaker_transitions = {
            client: [jd_ingester, critic],  # go straight to `critic` if chat closed without saving
            jd_ingester: [researcher],
            researcher: [researcher, resume_reader],
            resume_reader: [writer],
            writer: [critic],
            critic: [writer, client],
        }

    group_chat = GroupChat(
        agents=list(speaker_transitions.keys()),
        messages=[],
        send_introductions=True,
        allowed_or_disallowed_speaker_transitions=speaker_transitions,
        speaker_transitions_type="allowed",
    )

    group_manager = GroupChatManager(
        groupchat=group_chat,
        name="Cover_Letter_Automation",
        llm_config=deepcopy(llm_config),
    )

    conversation = client.initiate_chat(
        recipient=group_manager,
        message="Please start the extraction from the job description, then write a cover letter based on a resume.",
        summary_method="last_msg",  # Avoid a reflection price tag.
        clear_history=True,
        max_turns=22,
    )

    return conversation
