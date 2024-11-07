"""CLI entrypoint for the cover letter automation tool."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

from cover_letter_automation.session import setup_and_start_session

app = typer.Typer()


@app.command()
def make_cover_letter(  # noqa: PLR0917, PLR0913
    job_description: Annotated[Path, typer.Argument(help="Path to the job description text file", exists=True)],
    resume: Annotated[Path, typer.Argument(help="Path to the JSON resume file", exists=True)],
    openai_api_key: Annotated[str, typer.Option(envvar="OPENAI_API_KEY", help="OpenAI API key", prompt=True)],
    openai_model: Annotated[
        Optional[str], typer.Option(envvar="OPENAI_MODEL_NAME", help="OpenAI model")  # noqa: UP007
    ] = "gpt-4-turbo-preview",
    bing_api_key: Annotated[Optional[str], typer.Option(envvar="BING_API_KEY", help="Bing API key")] = None,  # noqa: UP007
    motivation: Annotated[Optional[Path], typer.Option(help="Path to the motivation text file", exists=True)] = None,  # noqa: UP007
) -> None:
    """Generate a cover letter based on a resume and a job description."""
    with job_description.open("r") as f:
        jd_text = f.read()

    if motivation:
        with motivation.open("r") as f:
            motivation_text = f.read()
    else:
        motivation_text = None

    _llm_config = {"config_list": [{"model": openai_model, "api_key": openai_api_key}], "cache_seed": None}

    chat = setup_and_start_session(
        llm_config=_llm_config,
        job_description=jd_text,
        json_resume_path=resume,
        bing_config={"viewport_size": 4096, "bing_api_key": bing_api_key} if bing_api_key else None,
        motivation=motivation_text,
    )

    try:
        print(chat.cost)
    except (IndexError, KeyError):
        print("Unable to retrieve cost, see full array: ", chat.cost)
