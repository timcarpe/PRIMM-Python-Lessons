from __future__ import annotations

import hashlib
import json
from pathlib import Path

from lesson_compiler.docx import (
    page2_code_display,
    page2_code_size,
    read_drawing_placement,
    recolor_keyword_runs,
    replace_drawing_placement,
    set_challenge_prompt,
    set_code,
    set_plain,
    set_spacer_height,
    write_docx,
)
from lesson_compiler.paths import LEARNER_DIRECTORY, SUPPLEMENTAL_DIRECTORY


def patch_standard_record(
    record: dict,
    changes: dict[tuple[int, int], str],
    config: dict,
) -> dict:
    number = record["lesson"]["number"]
    for challenge in range(1, 4):
        replacement = changes.get((number, challenge))
        if not replacement:
            continue
        record["primm"][challenge + 3]["prompt"] = replacement
        record["worksheet"]["page2"]["challenges"][challenge - 1]["prompt"] = (
            replacement
        )
        record["slides"][5 + (challenge - 1) * 2]["body"] = replacement
        if record.get("challenge_contracts"):
            record["challenge_contracts"][challenge - 1]["test_cases"] = [replacement]
            record["challenge_contracts"][challenge - 1]["observable_outcome"] = (
                replacement
            )

    starter = config.get("starter_overrides", {}).get(str(number))
    if starter:
        record["shared_program"]["code"] = starter
        record["worksheet"]["page2"]["reference"] = starter

    for key, code in config.get("program_overrides", {}).get(str(number), {}).items():
        record["programs"][key] = code.replace('" )', '")')

    if number == 18:
        questions = list(record["worksheet"]["page1"]["investigate_questions"])
        questions[1] = (
            "Which variable stores the generated whole number before it is displayed?"
        )
        record["worksheet"]["page1"]["investigate_questions"] = questions
        record["slides"][4]["body"] = "Answer the questions:\n" + "\n".join(
            f"{index}. {text}" for index, text in enumerate(questions, 1)
        )
    return record


def write_programs(record: dict, destination: Path) -> None:
    solutions = destination / "Solutions"
    solutions.mkdir(parents=True, exist_ok=True)
    files = {
        destination / record["shared_program"]["filename"]: record["shared_program"][
            "code"
        ],
        solutions / "challenge1.py": record["programs"]["challenge1"],
        solutions / "challenge2.py": record["programs"]["challenge2"],
        solutions / "challenge3.py": record["programs"]["challenge3"],
        solutions / "fixTheCode.py": record["programs"]["broken"],
        solutions / "fixTheCode - solution.py": record["programs"]["fixed"],
    }
    for path, code in files.items():
        path.write_text(code.replace('" )', '")').rstrip() + "\n", encoding="utf-8")


def patch_reference_worksheet(
    source: Path,
    destination: Path,
    starter: str,
    prompts: list[str],
    code_context: str,
    question_replacements: dict[str, str] | None = None,
    replace_starter: bool = True,
    media_replacements: dict[str, bytes] | None = None,
    illustration_width_inches: float | None = None,
    illustration_placement_authority: Path | None = None,
) -> None:
    placement = (
        read_drawing_placement(illustration_placement_authority)
        if illustration_placement_authority is not None
        else None
    )

    def patch(root) -> None:
        recolor_keyword_runs(root)
        body = root.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body"
        )
        children = list(body)
        visible = ["".join(node.itertext()).strip() for node in children]
        look_indices = [
            index for index, text in enumerate(visible) if text == "Look at this code:"
        ]
        if not look_indices:
            raise ValueError(f"challenge-page code heading not found in {source}")
        if replace_starter:
            for occurrence, look_index in enumerate(look_indices):
                code_index = next(
                    index
                    for index in range(look_index + 1, len(children))
                    if visible[index]
                )
                display = starter if occurrence == 0 else page2_code_display(starter)
                set_code(
                    children[code_index],
                    display,
                    page2_code_size(starter) if occurrence else None,
                )

        instruction_candidates = [
            index
            for index, text in enumerate(visible)
            if text.startswith("Use the code above")
        ]
        if len(instruction_candidates) != 1:
            raise ValueError(
                "expected one inherited challenge instruction in "
                f"{source}; got {instruction_candidates}"
            )

        prompt_indices = []
        for heading in ("Challenge 1", "Challenge 2", "Challenge 3"):
            heading_index = next(
                (index for index, text in enumerate(visible) if text == heading), None
            )
            if heading_index is None:
                raise ValueError(f"{heading} not found in {source}")
            prompt_index = next(
                index
                for index in range(heading_index + 1, len(children))
                if visible[index]
            )
            prompt_indices.append(prompt_index)
        for prompt_index, prompt in zip(prompt_indices, prompts, strict=True):
            set_challenge_prompt(children[prompt_index], prompt, code_context)

        if placement is not None:
            replace_drawing_placement(root, placement)

        if illustration_width_inches is not None:
            if illustration_width_inches <= 0:
                raise ValueError("illustration width must be positive")
            drawing_namespaces = {
                "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
                "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
                "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
                "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
            }
            drawings = root.xpath(".//w:drawing", namespaces=drawing_namespaces)
            if len(drawings) != 1:
                raise ValueError(
                    f"expected one worksheet drawing in {source}; found {len(drawings)}"
                )
            placement_extents = drawings[0].xpath(
                "./wp:inline/wp:extent | ./wp:anchor/wp:extent",
                namespaces=drawing_namespaces,
            )
            transform_extents = drawings[0].xpath(
                ".//pic:spPr/a:xfrm/a:ext", namespaces=drawing_namespaces
            )
            if len(placement_extents) != 1 or len(transform_extents) != 1:
                raise ValueError(f"worksheet drawing extents are invalid in {source}")
            old_cx = int(placement_extents[0].get("cx"))
            old_cy = int(placement_extents[0].get("cy"))
            target_cx = round(illustration_width_inches * 914_400)
            target_cy = round(old_cy * target_cx / old_cx)
            for extent in (*placement_extents, *transform_extents):
                extent.set("cx", str(target_cx))
                extent.set("cy", str(target_cy))

        page2_code_index = next(
            index
            for index in range(look_indices[-1] + 1, len(children))
            if visible[index]
        )
        instruction_index = instruction_candidates[0]
        challenges_heading_index = next(
            index
            for index, text in enumerate(visible)
            if text == "Programming Challenges"
        )
        spacer_specs = {
            page2_code_index + 1: 24,
            instruction_index + 1: 2,
            challenges_heading_index + 1: 2,
            prompt_indices[0] + 1: 6,
            prompt_indices[1] + 1: 6,
            prompt_indices[2] + 1: 4,
        }
        for index, points in spacer_specs.items():
            if index >= len(children) or visible[index]:
                continue
            if children[index].xpath(
                ".//w:drawing",
                namespaces={
                    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                },
            ):
                continue
            set_spacer_height(children[index], points)

        for paragraph in root.xpath(
            ".//w:p",
            namespaces={
                "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            },
        ):
            old = "".join(paragraph.itertext()).strip()
            if old in (question_replacements or {}):
                set_plain(paragraph, question_replacements[old])

    write_docx(source, destination, patch, media_replacements)


def write_manifest(output: Path, config: dict) -> None:
    files = []
    ignored_names = {".DS_Store", "MANIFEST.json"}
    for directory in (LEARNER_DIRECTORY, SUPPLEMENTAL_DIRECTORY):
        root = output / directory
        for path in sorted(
            item
            for item in root.rglob("*")
            if item.is_file() and item.name not in ignored_names
        ):
            files.append(
                {
                    "path": path.relative_to(output).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
    manifest = {
        "status": "reproducible_build",
        "run_id": config["run_id"],
        "build_mode": "full_non_capstone",
        "learner_slides_only": True,
        "lesson_count": len(config["lesson_numbers"]),
        "challenge_change_count": len(config["challenge_changes"]),
        "approved_challenge_change_count": config.get(
            "approved_challenge_change_count",
            len(config["challenge_changes"]),
        ),
        "structural_prompt_overrides": config.get(
            "structural_prompt_overrides",
            [],
        ),
        "proposal_source": config.get("proposal_source"),
        "preserved_original_lessons": config["preserved_original_lessons"],
        "excluded_capstones": config["excluded_capstones"],
        "file_count": len(files),
        "files": files,
    }
    (output / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
