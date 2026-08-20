from __future__ import annotations

import hashlib
import json
from pathlib import Path

from range_docx_compiler import (
    page2_code_display,
    page2_code_size,
    set_challenge_prompt,
    set_code,
    set_plain,
    write_docx,
)


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
        record["worksheet"]["page2"]["challenges"][challenge - 1]["prompt"] = replacement
        record["slides"][5 + (challenge - 1) * 2]["body"] = replacement
        if record.get("challenge_contracts"):
            record["challenge_contracts"][challenge - 1]["test_cases"] = [replacement]
            record["challenge_contracts"][challenge - 1]["observable_outcome"] = replacement

    starter = config.get("starter_overrides", {}).get(str(number))
    if starter:
        record["shared_program"]["code"] = starter
        record["worksheet"]["page2"]["reference"] = starter

    for key, code in config.get("program_overrides", {}).get(str(number), {}).items():
        record["programs"][key] = code.replace('" )', '")')

    if number == 18:
        questions = list(record["worksheet"]["page1"]["investigate_questions"])
        questions[1] = "Which variable stores the generated whole number before it is displayed?"
        record["worksheet"]["page1"]["investigate_questions"] = questions
        record["slides"][4]["body"] = "Answer the questions:\n" + "\n".join(
            f"{index}. {text}" for index, text in enumerate(questions, 1)
        )
    return record


def write_programs(record: dict, destination: Path) -> None:
    solutions = destination / "Solutions"
    solutions.mkdir(parents=True, exist_ok=True)
    files = {
        destination / record["shared_program"]["filename"]: record["shared_program"]["code"],
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
) -> None:
    def patch(root) -> None:
        body = root.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body")
        children = list(body)
        visible = ["".join(node.itertext()).strip() for node in children]
        look_indices = [index for index, text in enumerate(visible) if text == "Look at this code:"]
        if not look_indices:
            raise ValueError(f"challenge-page code heading not found in {source}")
        if replace_starter:
            for occurrence, look_index in enumerate(look_indices):
                code_index = next(index for index in range(look_index + 1, len(children)) if visible[index])
                display = starter if occurrence == 0 else page2_code_display(starter)
                set_code(children[code_index], display, page2_code_size(starter) if occurrence else None)

        instruction_candidates = [
            index for index, text in enumerate(visible) if text.startswith("Use the code above")
        ]
        if len(instruction_candidates) != 1:
            raise ValueError(
                f"expected the inherited challenge instruction in {source}; got {instruction_candidates}"
            )

        prompt_nodes = []
        for heading in ("Challenge 1", "Challenge 2", "Challenge 3"):
            heading_index = next((index for index, text in enumerate(visible) if text == heading), None)
            if heading_index is None:
                raise ValueError(f"{heading} not found in {source}")
            prompt_index = next(index for index in range(heading_index + 1, len(children)) if visible[index])
            prompt_nodes.append(children[prompt_index])
        for node, prompt in zip(prompt_nodes, prompts, strict=True):
            set_challenge_prompt(node, prompt, code_context)

        for paragraph in root.xpath(
            ".//w:p", namespaces={"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        ):
            old = "".join(paragraph.itertext()).strip()
            if old in (question_replacements or {}):
                set_plain(paragraph, question_replacements[old])

    write_docx(source, destination, patch)


def write_manifest(output: Path, config: dict) -> None:
    files = []
    for path in sorted(item for item in output.rglob("*") if item.is_file() and item.name != "MANIFEST.json"):
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
        "lesson_count": len(config["lesson_numbers"]),
        "preserved_original_lessons": config["preserved_original_lessons"],
        "excluded_capstones": config["excluded_capstones"],
        "files": files,
    }
    (output / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
