"""Test the generally-available tools outside of the Agents."""

from pathlib import Path

from cover_letter_automation.tools import export_letter


def test_export_letter(tmp_path: Path) -> None:
    """Test that a cover letter is exported to a file."""
    cover_letter = "Dear Sir/Madam,\n\nI am writing to apply for the position of Data Scientist at your company."
    filename = "21 09 company_lowercase__surname.md"
    path = tmp_path
    target = path / filename
    target.touch()

    result = export_letter(cover_letter, filename, str(path))

    assert result == str(target.absolute())
    assert target.read_text() == cover_letter
