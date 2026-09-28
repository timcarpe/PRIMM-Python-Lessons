"""Build the Python lesson suite.

Purpose:
    Compile the canonical curriculum records into learner and teacher files.
Key Components:
    Lesson compilation, Word-to-PDF conversion, and output packaging.
Dependencies:
    Node.js, pypdf, and the existing DOCX renderer.
Used By:
    The ``lesson-compiler build`` command.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from pypdf import PdfReader, PdfWriter

from lesson_compiler.capstones import compile_capstones
from lesson_compiler.paths import (
    CONFIG_PATH,
    DEFAULT_REPOSITORY_ROOT,
    DEFAULT_WORK_ROOT,
    LEARNER_DIRECTORY,
    PACKAGE_ROOT,
    RECORDS_ROOT,
    SUPPLEMENTAL_DIRECTORY,
    TEMPLATE_PATH,
    grade_for_lesson,
    lesson_directory,
)
from lesson_compiler.support import (
    patch_reference_worksheet,
    patch_standard_record,
    write_manifest,
    write_programs,
)


def resolve_node(explicit: Path | None) -> Path:
    """Resolve the Node.js executable used by the slide compiler."""
    configured = os.environ.get("LESSON_COMPILER_NODE")
    discovered = shutil.which("node")
    candidates = (
        explicit,
        Path(configured) if configured else None,
        Path(discovered) if discovered else None,
    )
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(
        "Node.js was not found. Install Node.js, set LESSON_COMPILER_NODE, "
        "or pass --node."
    )


def resolve_doc_renderer(explicit: Path | None) -> Path:
    """Resolve the established DOCX renderer used by the compiler."""
    configured = os.environ.get("LESSON_DOCX_RENDERER")
    candidates = (
        explicit,
        Path(configured) if configured else None,
        *sorted(
            Path.home().glob(
                ".codex/plugins/cache/openai-primary-runtime/documents/"
                "*/skills/documents/render_docx.py"
            ),
            reverse=True,
        ),
    )
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(
        "The DOCX renderer was not found. Set LESSON_DOCX_RENDERER or pass "
        "--doc-renderer."
    )


def run(command: list[str], cwd: Path | None = None) -> None:
    """Run one compiler subprocess and fail on a non-zero result."""
    subprocess.run(command, cwd=cwd, check=True)


def extract_challenge_pages(worksheet_pdf: Path, challenge_pdf: Path) -> None:
    """Extract all worksheet challenge pages into the learner challenge PDF.

    A worksheet contains a first activity page, one or two challenge pages, and
    a final debugging page. Keeping the middle pages together prevents longer
    challenge text from being discarded when a worksheet requires four pages.

    Args:
        worksheet_pdf: Rendered three- or four-page worksheet.
        challenge_pdf: Destination for the extracted challenge pages.

    Raises:
        RuntimeError: If the worksheet does not contain three or four pages.
    """
    reader = PdfReader(str(worksheet_pdf))
    page_count = len(reader.pages)
    if page_count not in {3, 4}:
        raise RuntimeError(
            "worksheet must render to three or four pages: "
            f"{worksheet_pdf} ({page_count} pages)"
        )
    writer = PdfWriter()
    for page in reader.pages[1:-1]:
        writer.add_page(page)
    with challenge_pdf.open("wb") as stream:
        writer.write(stream)


def learner_lesson(repository_root: Path, number: int, title: str) -> Path:
    """Return the canonical learner directory for one lesson."""
    return lesson_directory(
        repository_root / LEARNER_DIRECTORY,
        number,
        title,
    )


def supplemental_lesson(repository_root: Path, number: int, title: str) -> Path:
    """Return the canonical teacher-resource directory for one lesson."""
    return lesson_directory(
        repository_root / SUPPLEMENTAL_DIRECTORY,
        number,
        title,
    )


def compile_lesson(
    record: dict,
    repository_root: Path,
    work_root: Path,
    node: Path,
    doc_renderer: Path,
) -> None:
    """Compile all learner and teacher artifacts for one lesson."""
    number = record["lesson"]["number"]
    title = record["lesson"]["title"]
    learner_source = learner_lesson(repository_root, number, title)
    supplemental_source = supplemental_lesson(repository_root, number, title)
    lesson_root = work_root / "combined" / f"Lesson {number:02d} - {title}"
    lesson_root.mkdir(parents=True)

    concept_source = supplemental_source / f"{title} - Concept Sheet.docx"
    worksheet_source = supplemental_source / f"{title} - Worksheet.docx"
    starter_source = learner_source / f"{title} - Starter Code.py"
    for source in (concept_source, worksheet_source, starter_source):
        if not source.exists():
            raise FileNotFoundError(f"canonical lesson resource is missing: {source}")
    shutil.copy2(concept_source, lesson_root / concept_source.name)

    starter = record["shared_program"]["code"]
    source_starter = starter_source.read_text(encoding="utf-8").strip()
    question_replacements: dict[str, str] | None = None
    if number == 2:
        question_replacements = {
            "After num1 is multiplied by num2, which number is stored with the "
            "name total?": "After num1 is added to num2, which number is stored "
            "with the name total?"
        }
    elif number == 18:
        question_replacements = {
            "What value is stored in roll when the starter program uses seed 7, "
            "and why does the same value appear on another run?": "Which variable "
            "stores the generated whole number before it is displayed?"
        }
    prompts = [item["prompt"] for item in record["worksheet"]["page2"]["challenges"]]
    code_context = "\n".join([starter, *record["programs"].values()])
    with ZipFile(worksheet_source) as archive:
        worksheet_images = [
            name
            for name in archive.namelist()
            if (name.startswith("media/") or "/media/" in name)
            and Path(name).suffix.lower() in {".png", ".jpg", ".jpeg"}
        ]
    if len(worksheet_images) != 1:
        raise RuntimeError(
            f"expected one worksheet illustration in {worksheet_source}; "
            f"found {worksheet_images}"
        )
    worksheet_asset = repository_root / record["assets"]["worksheet"]
    if not worksheet_asset.exists():
        raise FileNotFoundError(worksheet_asset)
    placement_value = record["contracts"]["worksheet"].get(
        "illustration_placement_authority"
    )
    placement_authority = repository_root / placement_value if placement_value else None
    if placement_authority is not None and not placement_authority.exists():
        raise FileNotFoundError(placement_authority)
    patch_reference_worksheet(
        worksheet_source,
        lesson_root / worksheet_source.name,
        starter,
        prompts,
        code_context,
        question_replacements,
        source_starter != starter.strip(),
        {worksheet_images[0]: worksheet_asset.read_bytes()},
        record["assets"].get("worksheet_width_inches"),
        placement_authority,
    )
    write_programs(record, lesson_root)

    record_path = work_root / "records" / f"lesson{number:02d}.json"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    run(
        [
            str(node),
            str(PACKAGE_ROOT / "slides/compile.mjs"),
            str(repository_root),
            str(record_path),
            str(lesson_root / f"{title} - Slides.pptx"),
            str(work_root / f"renders/slides/lesson{number:02d}"),
            str(TEMPLATE_PATH),
            "--learner-only",
        ],
        repository_root,
    )

    document_render = work_root / f"renders/documents/lesson{number:02d}"
    run(
        [
            sys.executable,
            str(doc_renderer),
            str(lesson_root / worksheet_source.name),
            "--output_dir",
            str(document_render),
            "--emit_pdf",
        ]
    )
    extract_challenge_pages(
        document_render / f"{worksheet_source.stem}.pdf",
        lesson_root / f"{title} - Challenges.pdf",
    )
    print(f"compiled Lesson {number:02d} - {title}", flush=True)


def package_lessons(work_root: Path, output_root: Path) -> None:
    """Copy compiled files into the two standard output trees."""
    learner_root = output_root / LEARNER_DIRECTORY
    supplemental_root = output_root / SUPPLEMENTAL_DIRECTORY
    for compiled_lesson in sorted((work_root / "combined").glob("Lesson *")):
        number = int(compiled_lesson.name.split()[1])
        grade = grade_for_lesson(number)
        learner = learner_root / f"Grade {grade}" / compiled_lesson.name
        supplemental = supplemental_root / f"Grade {grade}" / compiled_lesson.name
        learner.mkdir(parents=True, exist_ok=True)
        supplemental.mkdir(parents=True, exist_ok=True)
        for item in compiled_lesson.iterdir():
            if item.name == "Solutions":
                shutil.copytree(
                    item,
                    supplemental / item.name,
                    dirs_exist_ok=True,
                )
            elif item.suffix.lower() in {".pptx", ".pdf"} or item.name.endswith(
                "Starter Code.py"
            ):
                shutil.copy2(item, learner / item.name)
            elif item.suffix.lower() == ".docx":
                shutil.copy2(item, supplemental / item.name)


def build_suite(
    repository_root: Path = DEFAULT_REPOSITORY_ROOT,
    output_root: Path | None = None,
    work_root: Path = DEFAULT_WORK_ROOT,
    node: Path | None = None,
    doc_renderer: Path | None = None,
) -> dict:
    """Compile the regular lesson suite, then the three capstones."""
    repository_root = repository_root.resolve()
    output_root = (output_root or repository_root).resolve()
    work_root = work_root.resolve()
    if work_root.exists():
        raise FileExistsError(
            f"temporary compiler workspace already exists: {work_root}"
        )
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(TEMPLATE_PATH)

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    expected = set(config["lesson_numbers"])
    excluded = set(config["excluded_capstones"])
    if expected & excluded:
        raise RuntimeError("compiled lessons and excluded capstones overlap")
    record_numbers = {
        int(item.stem.removeprefix("lesson"))
        for item in RECORDS_ROOT.glob("lesson*.json")
    }
    if record_numbers != expected:
        raise RuntimeError(
            "canonical record set mismatch: "
            f"expected {sorted(expected)}, found {sorted(record_numbers)}"
        )
    changes = {
        tuple(int(value) for value in key.split(".")): text
        for key, text in config["challenge_changes"].items()
    }
    if len(changes) != config["expected_challenge_change_count"]:
        raise RuntimeError(
            "canonical challenge-change count mismatch: "
            f"expected {config['expected_challenge_change_count']}, "
            f"found {len(changes)}"
        )

    resolved_node = resolve_node(node)
    resolved_doc_renderer = resolve_doc_renderer(doc_renderer)
    work_root.mkdir(parents=True)
    (work_root / "combined").mkdir()

    for number in sorted(expected):
        record_path = RECORDS_ROOT / f"lesson{number:02d}.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record = patch_standard_record(record, changes, config)
        compile_lesson(
            record,
            repository_root,
            work_root,
            resolved_node,
            resolved_doc_renderer,
        )

    output_root.mkdir(parents=True, exist_ok=True)
    package_lessons(work_root, output_root)
    # Capstones borrow a compiled regular worksheet as their style template,
    # so they are compiled after the regular lessons are packaged.
    compile_capstones(
        repository_root,
        output_root,
        work_root,
        resolved_node,
        resolved_doc_renderer,
    )
    write_manifest(output_root, config)
    return config


def main() -> None:
    """Run the build module directly with its standard defaults."""
    build_suite()


if __name__ == "__main__":
    main()
