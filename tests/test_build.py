"""Tests for lesson-suite build helpers."""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from lesson_compiler.build import extract_challenge_pages


def _write_pdf(path: Path, page_count: int) -> None:
    """Write distinguishable blank pages for extraction tests."""
    writer = PdfWriter()
    for index in range(page_count):
        writer.add_blank_page(width=500 + index, height=700 + index)
    with path.open("wb") as stream:
        writer.write(stream)


@pytest.mark.parametrize(
    ("worksheet_pages", "expected_widths"),
    [(3, [501]), (4, [501, 502])],
)
def test_extract_challenge_pages_keeps_all_middle_pages(
    tmp_path: Path,
    worksheet_pages: int,
    expected_widths: list[int],
) -> None:
    """Three- and four-page worksheets retain every challenge page."""
    # Arrange
    worksheet = tmp_path / "worksheet.pdf"
    challenge = tmp_path / "challenge.pdf"
    _write_pdf(worksheet, worksheet_pages)

    # Act
    extract_challenge_pages(worksheet, challenge)

    # Assert
    pages = PdfReader(str(challenge)).pages
    assert [int(page.mediabox.width) for page in pages] == expected_widths


@pytest.mark.parametrize("worksheet_pages", [2, 5])
def test_extract_challenge_pages_rejects_unsupported_page_counts(
    tmp_path: Path,
    worksheet_pages: int,
) -> None:
    """Unexpected pagination fails before an incomplete PDF is packaged."""
    # Arrange
    worksheet = tmp_path / "worksheet.pdf"
    challenge = tmp_path / "challenge.pdf"
    _write_pdf(worksheet, worksheet_pages)

    # Act / Assert
    with pytest.raises(RuntimeError, match="three or four pages"):
        extract_challenge_pages(worksheet, challenge)
