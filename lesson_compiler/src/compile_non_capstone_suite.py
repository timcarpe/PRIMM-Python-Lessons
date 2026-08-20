from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from compilation_support import (
    patch_reference_worksheet,
    patch_standard_record,
    write_manifest,
    write_programs,
)


ROOT = Path(__file__).resolve().parents[2]
COMPILER = ROOT / "lesson_compiler"
CONFIG_PATH = COMPILER / "curriculum/recompilation_run_2026-08-20.json"
GENERATED = COMPILER / "curriculum/records"
TEMPLATE = COMPILER / "templates/template-starter.pptx"
DEFAULT_OUTPUT = ROOT / "build/Recompiled Lesson Suite - Non-Capstone"
DEFAULT_WORK = ROOT / "build/work"


def resolve_node(explicit: Path | None) -> Path:
    candidates = [
        explicit,
        Path(os.environ["LESSON_COMPILER_NODE"]) if os.environ.get("LESSON_COMPILER_NODE") else None,
        Path(shutil.which("node")) if shutil.which("node") else None,
        Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node",
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    raise FileNotFoundError("Node.js was not found; use --node or LESSON_COMPILER_NODE")


def resolve_doc_renderer(explicit: Path | None) -> Path:
    if explicit and explicit.exists():
        return explicit
    if os.environ.get("LESSON_DOCX_RENDERER"):
        candidate = Path(os.environ["LESSON_DOCX_RENDERER"])
        if candidate.exists():
            return candidate
    candidates = sorted(
        Path.home().glob(
            ".codex/plugins/cache/openai-primary-runtime/documents/*/skills/documents/render_docx.py"
        )
    )
    if candidates:
        return candidates[-1]
    raise FileNotFoundError(
        "Codex's DOCX renderer was not found; use --doc-renderer or LESSON_DOCX_RENDERER"
    )


def run(command: list[str], cwd: Path | None = None) -> None:
    env = os.environ.copy()
    env["TMPDIR"] = "/private/tmp"
    subprocess.run(command, cwd=cwd, env=env, check=True)


def extract_page_two(worksheet_pdf: Path, challenge_pdf: Path) -> None:
    reader = PdfReader(str(worksheet_pdf))
    if len(reader.pages) != 3:
        raise RuntimeError(
            f"worksheet must render to three pages: {worksheet_pdf} ({len(reader.pages)} pages)"
        )
    # Clone first so page-level inherited resources are retained. Adding the
    # page to a blank writer caused the earlier dense-code PDF regression.
    writer = PdfWriter(clone_from=reader)
    del writer.pages[2]
    del writer.pages[0]
    with challenge_pdf.open("wb") as stream:
        writer.write(stream)


def source_lesson(number: int, title: str) -> Path:
    if number in {1, 2}:
        return ROOT / f"Example Output/Lesson Suite/Lesson {number:02d} - {title}"
    grade = 6 if number <= 11 else 7 if number <= 27 else 8
    return ROOT / f"Example Output/Mapped Curriculum Lessons/Grade {grade}/Lesson {number:02d} - {title}"


def mapped_lesson(number: int, title: str) -> Path:
    grade = 6 if number <= 11 else 7 if number <= 27 else 8
    return ROOT / f"Example Output/Mapped Curriculum Lessons/Grade {grade}/Lesson {number:02d} - {title}"


def read_programs(source: Path) -> dict[str, str]:
    solutions = source / "Solutions"
    return {
        "challenge1": (solutions / "challenge1.py").read_text(encoding="utf-8"),
        "challenge2": (solutions / "challenge2.py").read_text(encoding="utf-8"),
        "challenge3": (solutions / "challenge3.py").read_text(encoding="utf-8"),
        "broken": (solutions / "fixTheCode.py").read_text(encoding="utf-8"),
        "fixed": (solutions / "fixTheCode - solution.py").read_text(encoding="utf-8"),
    }


def reference_record(config: dict, changes: dict[tuple[int, int], str]) -> dict:
    number = 2
    title = "Operators and Integers"
    source = source_lesson(number, title)
    record = deepcopy(json.loads((GENERATED / "lesson03.json").read_text(encoding="utf-8")))
    starter = config["starter_overrides"]["2"]
    prompts = [
        changes[(2, 1)],
        changes[(2, 2)],
        "Create a program that asks for three whole numbers, subtracts the second and third from the first, and displays the total.",
    ]
    questions = [
        "If I enter 6, which number is stored with the name num2?",
        "After num1 is added to num2, which number is stored with the name total?",
        "What number appears on screen when the program finishes?",
    ]
    programs = read_programs(source)
    programs.update(config["program_overrides"]["2"])

    record["lesson"].update({"number": number, "title": title, "slug": "lesson02"})
    record["assets"].update(
        {
            "master": "lesson_compiler/assets/lesson02/raven-canonical.png",
            "title_layout": "lesson_compiler/assets/lesson02/raven-canonical.png",
            "worksheet": "lesson_compiler/assets/lesson02/raven-canonical.png",
        }
    )
    record["shared_program"].update(
        {"filename": f"{title} - Starter Code.py", "code": starter}
    )
    record["programs"] = programs
    record["slides"][0].update({"title": title, "subtitle": "Lesson 02"})
    record["slides"][2]["title"] = "Look at this code:"
    record["slides"][3]["title"] = "What do you think this code will do?"
    record["slides"][4].update(
        {
            "title": "Let’s investigate.",
            "body": "Answer the questions:\n"
            + "\n".join(f"{index}. {question}" for index, question in enumerate(questions, 1)),
        }
    )
    for challenge, slide_index in enumerate((5, 7, 9), 1):
        prompt = prompts[challenge - 1]
        record["slides"][slide_index].update(
            {"title": f"Challenge {challenge}", "body": prompt}
        )
        record["worksheet"]["page2"]["challenges"][challenge - 1].update(
            {"title": f"Challenge {challenge}", "prompt": prompt}
        )
    record["slides"][11].update(
        {
            "title": "Fix the code!",
            "body": "This code has errors! Look closely at the code to find the problems:",
        }
    )
    record["slides"][12]["title"] = "Fix the code! – Suggested Solution"
    return record


def preserve_original_lesson_one(work: Path) -> None:
    title = "Hello Python!"
    source = source_lesson(1, title)
    destination = work / "combined/Lesson 01 - Hello Python!"
    destination.mkdir(parents=True)
    for name in (
        "Hello Python! - Challenges.pdf",
        "Hello Python! - Concept Sheet.docx",
        "Hello Python! - Slides.pptx",
        "Hello Python! - Starter Code.py",
        "Hello Python! - Worksheet.docx",
    ):
        shutil.copy2(source / name, destination / name)
    shutil.copytree(source / "Solutions", destination / "Solutions")


def compile_lesson(
    record: dict,
    work: Path,
    node: Path,
    doc_renderer: Path,
) -> None:
    number = record["lesson"]["number"]
    title = record["lesson"]["title"]
    source = source_lesson(number, title)
    mapped = mapped_lesson(number, title)
    lesson_dir = work / "combined" / f"Lesson {number:02d} - {title}"
    lesson_dir.mkdir(parents=True)

    concept_source = mapped / f"{title} - Concept Sheet.docx"
    if not concept_source.exists():
        concept_source = source / f"{title} - Concept Sheet.docx"
    shutil.copy2(concept_source, lesson_dir / f"{title} - Concept Sheet.docx")

    worksheet_source = source / f"{title} - Worksheet.docx"
    starter = record["shared_program"]["code"]
    source_starter = (source / f"{title} - Starter Code.py").read_text(encoding="utf-8").strip()
    question_replacements = None
    if number == 2:
        question_replacements = {
            "After num1 is multiplied by num2, which number is stored with the name total?":
                "After num1 is added to num2, which number is stored with the name total?"
        }
    elif number == 18:
        question_replacements = {
            "What value is stored in roll when the starter program uses seed 7, and why does the same value appear on another run?":
                "Which variable stores the generated whole number before it is displayed?"
        }
    prompts = [item["prompt"] for item in record["worksheet"]["page2"]["challenges"]]
    code_context = "\n".join([starter, *record["programs"].values()])
    patch_reference_worksheet(
        worksheet_source,
        lesson_dir / f"{title} - Worksheet.docx",
        starter,
        prompts,
        code_context,
        question_replacements,
        source_starter != starter.strip(),
    )
    write_programs(record, lesson_dir)

    record_path = work / "records" / f"lesson{number:02d}.json"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    run(
        [
            str(node),
            str(COMPILER / "src/range_compile_slides.mjs"),
            str(ROOT),
            str(record_path),
            str(lesson_dir / f"{title} - Slides.pptx"),
            str(work / f"renders/slides/lesson{number:02d}"),
            str(TEMPLATE),
            "--learner-only",
        ],
        COMPILER / "src",
    )

    doc_render = work / f"renders/documents/lesson{number:02d}"
    run(
        [
            sys.executable,
            str(doc_renderer),
            str(lesson_dir / f"{title} - Worksheet.docx"),
            "--output_dir",
            str(doc_render),
            "--emit_pdf",
        ]
    )
    extract_page_two(
        doc_render / f"{title} - Worksheet.pdf",
        lesson_dir / f"{title} - Challenges.pdf",
    )
    print(f"compiled Lesson {number:02d} - {title}", flush=True)


def package(work: Path, output: Path) -> None:
    learner_root = output / "Mapped Curriculum Lessons"
    supplemental_root = output / "Mapped Curriculum Lesson - Supplemental Material"
    for lesson_dir in sorted((work / "combined").glob("Lesson *")):
        number = int(lesson_dir.name.split()[1])
        grade = 6 if number <= 11 else 7 if number <= 27 else 8
        learner = learner_root / f"Grade {grade}" / lesson_dir.name
        supplemental = supplemental_root / f"Grade {grade}" / lesson_dir.name
        learner.mkdir(parents=True)
        supplemental.mkdir(parents=True)
        for item in lesson_dir.iterdir():
            if item.name == "Solutions":
                shutil.copytree(item, supplemental / item.name)
            elif item.suffix.lower() in {".pptx", ".pdf"} or item.name.endswith("Starter Code.py"):
                shutil.copy2(item, learner / item.name)
            elif item.suffix.lower() == ".docx":
                shutil.copy2(item, supplemental / item.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Recompile the accepted non-capstone lesson suite")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--work", type=Path, default=DEFAULT_WORK)
    parser.add_argument("--node", type=Path)
    parser.add_argument("--doc-renderer", type=Path)
    args = parser.parse_args()

    output = args.output.resolve()
    work = args.work.resolve()
    if output.exists() or work.exists():
        raise FileExistsError(
            f"build destinations must not already exist; move or remove {output} and {work}"
        )
    if not TEMPLATE.exists():
        raise FileNotFoundError(TEMPLATE)
    output.parent.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True)
    (work / "combined").mkdir()

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    expected = {number for number in range(1, 37) if number not in {11, 27, 36}}
    if set(config["lesson_numbers"]) != expected:
        raise RuntimeError("canonical lesson list does not match the non-capstone suite")
    changes = {
        tuple(int(value) for value in key.split(".")): text
        for key, text in config["challenge_changes"].items()
    }
    if len(changes) != 23:
        raise RuntimeError(f"expected 23 accepted non-capstone challenge changes, found {len(changes)}")

    node = resolve_node(args.node)
    doc_renderer = resolve_doc_renderer(args.doc_renderer)
    preserve_original_lesson_one(work)

    records = [reference_record(config, changes)]
    for number in sorted(expected):
        if number <= 2:
            continue
        record_path = GENERATED / f"lesson{number:02d}.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        records.append(patch_standard_record(record, changes, config))
    for record in records:
        compile_lesson(record, work, node, doc_renderer)

    output.mkdir(parents=True)
    package(work, output)
    write_manifest(output, config)
    print(json.dumps({"output": str(output), "lessons": sorted(expected)}, indent=2))


if __name__ == "__main__":
    main()
