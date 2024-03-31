"""Run the session from the installed package."""

import argparse
import logging
import os
from pathlib import Path

from autogen import ChatResult
from dotenv import load_dotenv

from cover_letter_automation.session import setup_and_start_session


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Set up a group chat session.")
    parser.add_argument(
        "--job-description",
        "-j",
        type=Path,
        required=True,
        help="The job description to respond to.",
    )
    return parser.parse_args()


def main() -> ChatResult:
    """Set up the group chat session."""
    _ = load_dotenv()

    args = parse_args()
    openai_spec = {
        "model": "gpt-4-turbo-preview",
        "api_key": os.environ["OPENAI_API_KEY"],
    }
    openai_3_5_spec = {
        "model": "gpt-3.5-turbo-preview",
        "api_key": str(os.environ["OPENAI_API_KEY"]),
    }

    config_list = {
        "config_list": [openai_spec, openai_3_5_spec],
        "temperature": 0.7,
        "cache_seed": None,
    }

    bing_config = {"viewport_size": 4096, "bing_api_key": os.environ["BING_API_KEY"]}

    with args.job_description.open("r") as f:
        # Read all lines of the job description into a single string
        job_description = f.read()

    chat = setup_and_start_session(
        llm_config=config_list,
        bing_config=bing_config,
        job_description=job_description,
    )

    import pdb  # noqa: T100, PLC0415

    pdb.set_trace()  # noqa: T100

    return chat


if __name__ == "__main__":
    logger = logging.getLogger("autogen")
    logger.setLevel(logging.ERROR)

    _ = main()
