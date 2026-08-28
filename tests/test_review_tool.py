"""Tests for the browser-based lesson manifest review tool."""

from __future__ import annotations

import json
import re

from lesson_compiler.review_tool.build import build_review_tool, load_effective_lessons


def test_effective_lessons_include_suite_overrides() -> None:
    """The review source matches the effective records used by compilation."""
    # Arrange
    expected_lesson_count = 33

    # Act
    lessons = load_effective_lessons()
    lesson_one = next(lesson for lesson in lessons if lesson["number"] == 1)
    challenge_one = next(
        item for item in lesson_one["items"] if item["field"] == "challenge_1"
    )

    # Assert
    assert len(lessons) == expected_lesson_count
    assert len(lesson_one["items"]) == 4
    assert challenge_one["value"].startswith("Store a greeting")
    assert "[greeting]" in challenge_one["value"]
    assert "".join(segment["text"] for segment in challenge_one["segments"]) == (
        challenge_one["value"]
    )
    assert {"text": '"Xin chao"', "role": "literal"} in challenge_one["segments"]
    assert {"text": "print()", "role": "call"} in challenge_one["segments"]


def test_build_review_tool_embeds_all_review_items(tmp_path) -> None:
    """The generated page is self-contained and has traceability metadata."""
    # Arrange
    output = tmp_path / "review.html"

    # Act
    report = build_review_tool(output)
    html = output.read_text(encoding="utf-8")
    metadata = json.loads(
        output.with_suffix(".metadata.json").read_text(encoding="utf-8")
    )
    match = re.search(
        r'<script id="lesson-data" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )

    # Assert
    assert report["passed"] is True
    assert metadata["lesson_count"] == 33
    assert metadata["review_item_count"] == 132
    assert match is not None
    payload = json.loads(match.group(1))
    assert len(payload["lessons"]) == 33
    assert "__LESSON_REVIEW_DATA__" not in html
    assert "lesson_manifest_issue_report" in html
    assert "lesson_manifest_change_proposal" in html


def test_embedded_manifest_text_cannot_close_data_script(tmp_path) -> None:
    """Embedded curriculum text cannot inject an extra HTML script element."""
    # Arrange
    output = tmp_path / "review.html"

    # Act
    build_review_tool(output)
    html = output.read_text(encoding="utf-8")

    # Assert
    assert html.count('<script id="lesson-data"') == 1
    assert "\\u003c" in html
