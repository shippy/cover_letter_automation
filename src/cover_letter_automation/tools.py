"""Tools for agents to call."""

from pathlib import Path
from typing import Annotated


def export_letter(
    cover_letter: Annotated[str, "Full text of the cover letter, formatted in Markdown"],
    filename: Annotated[
        str,
        "Name of the file to save the cover letter to, preferably in the format `YY MM company_lowercase__surname.md`",
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
