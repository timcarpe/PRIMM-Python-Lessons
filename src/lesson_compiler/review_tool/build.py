"""Generate the self-contained lesson manifest review page.

Purpose:
    Present effective lesson examples and challenges for structured review.
Key Components:
    Effective-record loading, safe data embedding, and artifact metadata.
Dependencies:
    Canonical curriculum JSON records and the shared override logic.
Used By:
    The ``lesson-compiler review-tool`` command.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict

from lesson_compiler.docx import (
    challenge_semantic_segments,
    challenge_vocabulary,
    code_semantic_segments,
    normalize_code,
)
from lesson_compiler.paths import (
    CONFIG_PATH,
    DEFAULT_REPOSITORY_ROOT,
    RECORDS_ROOT,
    grade_for_lesson,
)
from lesson_compiler.support import patch_standard_record

TEMPLATE_PATH = Path(__file__).with_name("template.html")
DATA_PLACEHOLDER = "__LESSON_REVIEW_DATA__"


class ReviewItem(TypedDict):
    """One reviewable manifest field."""

    field: str
    label: str
    kind: str
    value: str
    segments: list["ReviewSegment"]


class ReviewSegment(TypedDict):
    """One compiler-classified text segment."""

    text: str
    role: str


class ReviewLesson(TypedDict):
    """Effective manifest values displayed for one lesson."""

    number: int
    title: str
    grade: int
    manifest_path: str
    functions: list[str]
    items: list[ReviewItem]


def _load_json(path: Path) -> dict[str, Any]:
    """Load one JSON object from disk.

    Args:
        path: JSON file to read.

    Returns:
        Parsed JSON object.

    Raises:
        ValueError: If the JSON root is not an object.
    """
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def load_effective_lessons() -> list[ReviewLesson]:
    """Load all configured lessons after applying suite overrides.

    Returns:
        Review-ready lessons in curriculum order.
    """
    config = _load_json(CONFIG_PATH)
    changes: dict[tuple[int, int], str] = {}
    for key, text_value in config["challenge_changes"].items():
        lesson_text, challenge_text = key.split(".")
        changes[(int(lesson_text), int(challenge_text))] = str(text_value)
    lessons: list[ReviewLesson] = []
    for number_value in sorted(config["lesson_numbers"]):
        number = int(number_value)
        record_path = RECORDS_ROOT / f"lesson{number:02d}.json"
        record = patch_standard_record(_load_json(record_path), changes, config)
        code_context = "\n".join(
            [str(record["shared_program"]["code"]), *record["programs"].values()]
        )
        example_code = normalize_code(str(record["shared_program"]["code"]))
        challenge_items: list[ReviewItem] = [
            {
                "field": f"challenge_{index}",
                "label": f"Challenge {index}",
                "kind": "challenge",
                "value": str(challenge["prompt"]),
                "segments": [
                    {"text": part, "role": role}
                    for part, role in challenge_semantic_segments(
                        str(challenge["prompt"]), code_context
                    )
                ],
            }
            for index, challenge in enumerate(
                record["worksheet"]["page2"]["challenges"], 1
            )
        ]
        lessons.append(
            {
                "number": number,
                "title": str(record["lesson"]["title"]),
                "grade": grade_for_lesson(number),
                "manifest_path": str(
                    record_path.relative_to(DEFAULT_REPOSITORY_ROOT)
                ),
                "functions": sorted(challenge_vocabulary(code_context)["functions"]),
                "items": [
                    {
                        "field": "example_code",
                        "label": "Example code",
                        "kind": "code",
                        "value": example_code,
                        "segments": [
                            {"text": part, "role": role}
                            for part, role in code_semantic_segments(example_code)
                        ],
                    },
                    *challenge_items,
                ],
            }
        )
    return lessons


def _embedded_json(value: object) -> str:
    """Serialize JSON without allowing an embedded script to terminate early."""
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def build_review_tool(output: Path) -> dict[str, object]:
    """Write the self-contained review page and traceability metadata.

    Args:
        output: Destination HTML file.

    Returns:
        Machine-readable build report.

    Raises:
        ValueError: If the page template is missing its data placeholder.
    """
    lessons = load_effective_lessons()
    payload = {
        "schema_version": "1.0",
        "kind": "lesson_manifest_review_source",
        "suite_path": str(CONFIG_PATH.relative_to(DEFAULT_REPOSITORY_ROOT)),
        "lessons": lessons,
    }
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if template.count(DATA_PLACEHOLDER) != 1:
        raise ValueError(
            f"review template must contain one {DATA_PLACEHOLDER} placeholder"
        )
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        template.replace(DATA_PLACEHOLDER, _embedded_json(payload)),
        encoding="utf-8",
    )
    metadata_path = output.with_suffix(".metadata.json")
    metadata = {
        "schema_version": "1.0",
        "kind": "lesson_manifest_review_artifact",
        "artifact": output.name,
        "source_suite": payload["suite_path"],
        "lesson_count": len(lessons),
        "review_item_count": sum(len(lesson["items"]) for lesson in lessons),
        "self_contained": True,
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    return {
        "passed": True,
        "output": str(output),
        "metadata": str(metadata_path),
        "lesson_count": metadata["lesson_count"],
        "review_item_count": metadata["review_item_count"],
    }
