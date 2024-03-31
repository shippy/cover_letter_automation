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
    parser.add_argument(
        "--resume",
        "-r",
        type=Path,
        default=Path("resume/resume.json"),
        help="The JSON resume to extract information from.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Drop into PDB after the multi-agent chat concludes.",
    )
    return parser.parse_args()


def main() -> ChatResult:
    """Set up the group chat session."""
    _ = load_dotenv()

    args = parse_args()

    mistral_spec = {  # noqa: F841
        "model": "mistral",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }
    openai_4_spec = {
        "model": "gpt-4-turbo-preview",
        "api_key": os.environ["OPENAI_API_KEY"],
    }
    openai_3_5_spec = {  # noqa: F841
        "model": "gpt-3.5-turbo-preview",
        "api_key": str(os.environ["OPENAI_API_KEY"]),
    }

    config_list = {
        "config_list": [openai_4_spec],
        "temperature": 0.7,
        "cache_seed": None,
    }

    bing_config = None
    bing_api_key = os.environ.get("BING_API_KEY")
    if bing_api_key:
        bing_config = {"viewport_size": 4096, "bing_api_key": bing_api_key}

    with args.job_description.open("r") as f:
        # Read all lines of the job description into a single string
        job_description = f.read()

    chat = setup_and_start_session(
        llm_config=config_list,
        bing_config=bing_config,
        job_description=job_description,
        json_resume_path=args.resume,
    )
    try:
        print("Cost: $", round(chat.cost[0]["total_cost"], 2))  # noqa: T201
    except (IndexError, KeyError):
        print("Unable to retrieve cost, see full array: ", chat.cost)  # noqa: T201

    if args.debug:
        import pdb  # noqa: T100, PLC0415

        pdb.set_trace()  # noqa: T100

    return chat


if __name__ == "__main__":
    logger = logging.getLogger("autogen")
    logger.setLevel(logging.ERROR)

    _ = main()
