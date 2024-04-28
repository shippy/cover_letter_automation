"""Test the generally-available tools outside of the Agents."""

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from cover_letter_automation.tools import export_letter


def test_export_letter(tmp_path: Path) -> None:
    """Test that a cover letter is exported to a file."""
    cover_letter = "Dear Sir/Madam,\n\nI am writing to apply for the position of Data Scientist at your company."
    filename = "company_lowercase__surname.md"
    target_filename = f"{datetime(2022, 1, 1, tzinfo=UTC).strftime('%Y-%m-%d')}__{filename}"
    path = tmp_path
    target = path / target_filename
    target.touch()

    with patch("cover_letter_automation.tools.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2022, 1, 1, tzinfo=UTC)
        result = export_letter(cover_letter, filename, str(path))

    assert result == str(target.absolute())
    assert target.read_text() == cover_letter
