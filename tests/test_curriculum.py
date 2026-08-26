"""Tests for the canonical curriculum and compiled lesson inventory."""

from __future__ import annotations

import json
from pathlib import Path

from lesson_compiler.paths import (
    CONFIG_PATH,
    DEFAULT_REPOSITORY_ROOT,
    LEARNER_DIRECTORY,
    RECORDS_ROOT,
    SUPPLEMENTAL_DIRECTORY,
    grade_for_lesson,
)


def test_curriculum_has_one_record_per_compiled_lesson() -> None:
    """The canonical suite and record directory describe the same lessons."""
    # Arrange
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    # Act
    configured = set(config["lesson_numbers"])
    recorded = {
        int(path.stem.removeprefix("lesson"))
        for path in RECORDS_ROOT.glob("lesson*.json")
    }

    # Assert
    assert recorded == configured
    assert configured.isdisjoint(config["excluded_capstones"])


def test_root_contains_one_complete_compiled_suite() -> None:
    """Every configured lesson has the standard learner and teacher files."""
    # Arrange
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    learner_root = DEFAULT_REPOSITORY_ROOT / LEARNER_DIRECTORY
    supplemental_root = DEFAULT_REPOSITORY_ROOT / SUPPLEMENTAL_DIRECTORY

    # Act / Assert
    for number in config["lesson_numbers"]:
        record = json.loads(
            (RECORDS_ROOT / f"lesson{number:02d}.json").read_text(encoding="utf-8")
        )
        title = record["lesson"]["title"]
        grade = grade_for_lesson(number)
        lesson_name = f"Lesson {number:02d} - {title}"
        learner = learner_root / f"Grade {grade}" / lesson_name
        supplemental = supplemental_root / f"Grade {grade}" / lesson_name
        assert len(list(learner.glob("* - Slides.pptx"))) == 1
        assert len(list(learner.glob("* - Challenges.pdf"))) == 1
        assert len(list(learner.glob("* - Starter Code.py"))) == 1
        assert len(list(supplemental.glob("*.docx"))) == 2
        assert len(list((supplemental / "Solutions").glob("*.py"))) == 5


def test_no_alternate_lesson_suite_directories_remain() -> None:
    """The two root folders are the repository's only compiled lesson trees."""
    # Arrange
    excluded_roots = {LEARNER_DIRECTORY, SUPPLEMENTAL_DIRECTORY}

    # Act
    alternates = [
        path
        for path in DEFAULT_REPOSITORY_ROOT.iterdir()
        if path.is_dir()
        and path.name not in excluded_roots
        and (
            "Example Output" in path.name
            or "Recompiled Lesson Suite" in path.name
            or path.name == "Lesson Suite"
        )
    ]

    # Assert
    assert alternates == []


def test_repository_root_is_the_default_output_location() -> None:
    """The compiler's package paths resolve to the repository root."""
    # Arrange / Act
    root = Path(__file__).resolve().parents[1]

    # Assert
    assert DEFAULT_REPOSITORY_ROOT == root
