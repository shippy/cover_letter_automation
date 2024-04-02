"""Set up all agents for the package."""

from cover_letter_automation.agents.client import CoverLetterClient
from cover_letter_automation.agents.company_researcher import CompanyResearcher
from cover_letter_automation.agents.critic import Critic
from cover_letter_automation.agents.job_description_ingester import JobDescriptionIngester
from cover_letter_automation.agents.resume_retriever import ResumeRetriever
from cover_letter_automation.agents.writer import Writer

__all__ = [
    "CompanyResearcher",
    "CoverLetterClient",
    "Critic",
    "JobDescriptionIngester",
    "ResumeRetriever",
    "Writer",
]
