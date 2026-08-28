"""Tests for lesson-suite verification helpers."""

from lesson_compiler.verify import plain, strip_pdf_page_furniture


def test_strip_pdf_page_furniture_preserves_cross_page_prompt_text() -> None:
    """Page numbers and copyright lines do not interrupt prompt comparison."""
    # Arrange
    first_page = 'Display "Return the\n'
    second_page = '3\n© Tim Carpenter 2024\noverdue book first."'

    # Act
    text = "\n".join(
        strip_pdf_page_furniture(page) for page in (first_page, second_page)
    )

    # Assert
    assert plain(text) == 'Display "Return the overdue book first."'
