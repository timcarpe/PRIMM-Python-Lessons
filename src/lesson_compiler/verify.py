"""Verify a compiled Python lesson suite."""

from __future__ import annotations

import json
import re
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from pptx import Presentation
from pypdf import PdfReader

from lesson_compiler.paths import (
    CONFIG_PATH,
    DEFAULT_REPOSITORY_ROOT,
    LEARNER_DIRECTORY,
    SUPPLEMENTAL_DIRECTORY,
)
from lesson_compiler.support import write_manifest


def plain(text: str) -> str:
    """Normalize prose for cross-format challenge-text comparisons."""
    return re.sub(
        r"\s+",
        " ",
        text.replace('"', "").replace("“", "").replace("”", "").replace("'", ""),
    ).strip()


def verify_suite(
    output_root: Path = DEFAULT_REPOSITORY_ROOT,
    work_root: Path | None = None,
) -> dict:
    """Verify inventory, content contracts, and key formatting contracts."""
    output_root = output_root.resolve()
    work_root = work_root.resolve() if work_root is not None else None
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    expected = set(config["lesson_numbers"])
    changes = {
        tuple(int(value) for value in key.split(".")): text
        for key, text in config["challenge_changes"].items()
    }
    failures: list[str] = []
    if len(changes) != config["expected_challenge_change_count"]:
        failures.append(
            "canonical challenge-change count mismatch: "
            f"expected {config['expected_challenge_change_count']}, "
            f"found {len(changes)}"
        )

    stats = {
        "lessons": 0,
        "pptx": 0,
        "pdf": 0,
        "docx": 0,
        "python": 0,
        "slide_pages": 0,
    }
    learner = output_root / LEARNER_DIRECTORY
    supplemental = output_root / SUPPLEMENTAL_DIRECTORY
    actual = {int(path.name.split()[1]) for path in learner.glob("Grade */Lesson *")}
    if actual != expected:
        failures.append(
            f"lesson set mismatch: expected {sorted(expected)}, got {sorted(actual)}"
        )

    for number in sorted(expected):
        learner_dir = next(learner.glob(f"Grade */Lesson {number:02d} - *"), None)
        supplemental_dir = next(
            supplemental.glob(f"Grade */Lesson {number:02d} - *"),
            None,
        )
        if learner_dir is None or supplemental_dir is None:
            failures.append(f"L{number:02d}: missing learner or supplemental folder")
            continue
        stats["lessons"] += 1
        presentations = list(learner_dir.glob("* - Slides.pptx"))
        challenge_pdfs = list(learner_dir.glob("* - Challenges.pdf"))
        starters = list(learner_dir.glob("* - Starter Code.py"))
        documents = list(supplemental_dir.glob("*.docx"))
        programs = list((supplemental_dir / "Solutions").glob("*.py"))
        inventory = [
            len(presentations),
            len(challenge_pdfs),
            len(starters),
            len(documents),
            len(programs),
        ]
        if inventory != [1, 1, 1, 2, 5]:
            failures.append(f"L{number:02d}: inventory {inventory}")
            continue
        stats["pptx"] += 1
        stats["pdf"] += 1
        stats["docx"] += 2
        stats["python"] += 6

        presentation = Presentation(presentations[0])
        slide_count = len(presentation.slides)
        stats["slide_pages"] += slide_count
        if slide_count != 9:
            failures.append(f"L{number:02d}: {slide_count} slides, expected 9")
        deck_text = "\n".join(
            shape.text
            for slide in presentation.slides
            for shape in slide.shapes
            if hasattr(shape, "text")
        )
        lowered = deck_text.lower()
        if "suggested solution" in lowered:
            failures.append(f"L{number:02d}: solution slide text in learner deck")
        if len(PdfReader(str(challenge_pdfs[0])).pages) != 1:
            failures.append(f"L{number:02d}: challenge PDF is not one page")

        worksheet = next(supplemental_dir.glob("* - Worksheet.docx"))
        worksheet_text = "\n".join(
            paragraph.text for paragraph in Document(worksheet).paragraphs
        )
        pdf_text = PdfReader(str(challenge_pdfs[0])).pages[0].extract_text() or ""
        for challenge in range(1, 4):
            replacement = changes.get((number, challenge))
            if replacement is None:
                continue
            needle = plain(replacement)
            for artifact, text in (
                ("deck", deck_text),
                ("worksheet", worksheet_text),
                ("PDF", pdf_text),
            ):
                if needle not in plain(text):
                    failures.append(
                        f"L{number:02d} C{challenge}: accepted prompt absent "
                        f"from {artifact}"
                    )

        if work_root is not None:
            rendered = (
                work_root / f"renders/documents/lesson{number:02d}/{worksheet.stem}.pdf"
            )
            if not rendered.exists() or len(PdfReader(str(rendered)).pages) != 3:
                failures.append(
                    f"L{number:02d}: rendered worksheet source is not three pages"
                )

    lesson_one = next(supplemental.glob("Grade 6/Lesson 01 -*/* - Worksheet.docx"))
    with ZipFile(lesson_one) as archive:
        lesson_one_xml = archive.read("word/document.xml").decode("utf-8")
    if "<wp:anchor" not in lesson_one_xml or "<wp:inline" in lesson_one_xml:
        failures.append("L01: worksheet illustration is not anchored")
    if not re.search(r"<wp:wrap(?:Square|Tight|Through)\b", lesson_one_xml):
        failures.append("L01: worksheet illustration has no text-wrapping rule")

    lesson_two_slides = next(learner.glob("Grade 6/Lesson 02 -*/* - Slides.pptx"))
    with ZipFile(lesson_two_slides) as archive:
        slide_xml = "\n".join(
            archive.read(name).decode("utf-8")
            for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide[678]\.xml", name)
        )
    if "&quot;Total:&quot;" not in slide_xml and '"Total:"' not in slide_xml:
        failures.append('L02: quoted "Total:" absent from challenge slides')
    if "067D17" not in slide_xml:
        failures.append("L02: green literal colour absent from challenge slides")

    lesson_two_worksheet = next(
        supplemental.glob("Grade 6/Lesson 02 -*/* - Worksheet.docx")
    )
    with ZipFile(lesson_two_worksheet) as archive:
        worksheet_xml = archive.read("word/document.xml").decode("utf-8")
    if "067D17" not in worksheet_xml or "Total:" not in worksheet_xml:
        failures.append("L02: quoted green literal absent from worksheet")

    report = {
        "passed": not failures,
        "stats": stats,
        "excluded_capstones": config["excluded_capstones"],
        "failures": failures,
    }
    (output_root / "VERIFICATION.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    write_manifest(output_root, config)
    return report


def main() -> None:
    """Verify the canonical root lesson folders."""
    report = verify_suite()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
