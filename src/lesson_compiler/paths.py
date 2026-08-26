"""Shared paths and lesson-location rules for the compiler."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_REPOSITORY_ROOT = PACKAGE_ROOT.parents[1]
CONFIG_PATH = PACKAGE_ROOT / "curriculum/suite.json"
RECORDS_ROOT = PACKAGE_ROOT / "curriculum/records"
TEMPLATE_PATH = PACKAGE_ROOT / "templates/template-starter.pptx"
DEFAULT_WORK_ROOT = DEFAULT_REPOSITORY_ROOT / ".build/lesson-compiler"
LEARNER_DIRECTORY = "Mapped Curriculum Lessons"
SUPPLEMENTAL_DIRECTORY = "Mapped Curriculum Lesson - Supplemental Material"


def grade_for_lesson(number: int) -> int:
    """Return the mapped grade for a lesson number.

    Args:
        number: Curriculum lesson number.

    Returns:
        Grade 6, 7, or 8.

    Raises:
        ValueError: If the lesson number is outside the supported sequence.
    """
    if 1 <= number <= 11:
        return 6
    if 12 <= number <= 27:
        return 7
    if 28 <= number <= 36:
        return 8
    raise ValueError(f"unsupported lesson number: {number}")


def lesson_directory(root: Path, number: int, title: str) -> Path:
    """Return a lesson directory beneath a learner or supplemental root."""
    grade = grade_for_lesson(number)
    return root / f"Grade {grade}" / f"Lesson {number:02d} - {title}"
