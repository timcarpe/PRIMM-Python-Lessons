"""Compile the three capstone lessons from canonical capstone data.

Purpose:
    Produce each capstone's learner challenge PDF, slide deck and reference
    solutions from ``curriculum/capstones.json`` instead of hand-made files.
Key Components:
    Worksheet-styled challenge DOCX assembly, PDF rendering, slide filling
    and solution checks.
Dependencies:
    A compiled regular worksheet as the style template, the established DOCX
    renderer, Node.js for slides, and the shared challenge prose styling.
Used By:
    ``build_suite`` after the regular lessons, and ``verify_suite``.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from lxml import etree

from lesson_compiler.docx import (
    NS,
    W,
    set_challenge_prompt,
    set_plain,
    write_docx,
)
from lesson_compiler.paths import (
    LEARNER_DIRECTORY,
    PACKAGE_ROOT,
    SUPPLEMENTAL_DIRECTORY,
    lesson_directory,
)

CAPSTONES_PATH = PACKAGE_ROOT / "curriculum/capstones.json"
SECTION_LABELS = ("Build it", "Test it", "Talk about it")


def load_capstones() -> list[dict]:
    """Return the canonical capstone definitions in lesson order."""
    data = json.loads(CAPSTONES_PATH.read_text(encoding="utf-8"))
    return sorted(data["capstones"], key=lambda item: item["number"])


def challenge_paragraphs(challenge: dict, number: int) -> list[tuple[str, str]]:
    """Return (kind, text) pairs for one capstone challenge page."""
    items = [("h1", f"Challenge {number}"), ("prompt", challenge["goal"])]
    items.append(("h2", SECTION_LABELS[0]))
    items += [
        ("prompt", f"{index}. {step}")
        for index, step in enumerate(challenge["steps"], 1)
    ]
    items.append(("h2", SECTION_LABELS[1]))
    items += [("prompt", f"• {test}") for test in challenge["tests"]]
    items.append(("h2", SECTION_LABELS[2]))
    items.append(("prompt", challenge["talk"]))
    items.append(("spacer", ""))
    items.append(("prompt", f"Save as challenge{number}.py."))
    return items


def _prototypes(body: etree._Element) -> dict[str, etree._Element]:
    """Collect styled paragraph prototypes from a compiled regular worksheet."""

    def style(paragraph: etree._Element) -> str | None:
        node = paragraph.find("w:pPr/w:pStyle", NS)
        return node.get(W + "val") if node is not None else None

    def text(paragraph: etree._Element) -> str:
        return "".join(node.text or "" for node in paragraph.iter(W + "t"))

    paragraphs = [child for child in body if child.tag == W + "p"]
    found: dict[str, etree._Element] = {}
    for index, paragraph in enumerate(paragraphs):
        kind = style(paragraph)
        has_break = paragraph.find(".//w:br", NS) is not None
        if kind == "Title" and "title" not in found:
            found["title"] = paragraph
        elif kind == "Heading1" and text(paragraph) and "h1" not in found:
            found["h1"] = paragraph
        elif kind == "Heading2" and text(paragraph) == "Challenge 1":
            found["h2"] = paragraph
            found["prompt"] = paragraphs[index + 1]
        elif kind is None and has_break and not text(paragraph):
            found.setdefault("break", paragraph)
        elif kind is None and not text(paragraph) and not has_break:
            if paragraph.find(".//w:drawing", NS) is None:
                found.setdefault("spacer", paragraph)
    missing = {"title", "h1", "h2", "prompt", "break", "spacer"} - set(found)
    if missing:
        raise RuntimeError(f"worksheet template lacks prototypes: {sorted(missing)}")
    return found


def build_challenge_docx(capstone: dict, template: Path, destination: Path) -> None:
    """Write a three-page capstone challenge document in worksheet styling."""

    def patch(root: etree._Element) -> None:
        body = root.find("w:body", NS)
        prototypes = _prototypes(body)
        # The worksheet's final section inherits its footer from the first
        # section; the capstone has one section, so it takes the first
        # section's complete properties, including the footer.
        first_section = body.find("w:p/w:pPr/w:sectPr", NS)
        section = body.find("w:sectPr", NS)
        if first_section is not None:
            body.replace(section, deepcopy(first_section))
            section = body.find("w:sectPr", NS)
        for child in list(body):
            if child is not section:
                body.remove(child)
        position = 0

        def append(kind: str, text: str, code_context: str) -> None:
            nonlocal position
            paragraph = deepcopy(prototypes[kind])
            if kind == "prompt":
                set_challenge_prompt(paragraph, text, code_context)
            elif kind in {"title", "h1", "h2"}:
                set_plain(paragraph, text)
            body.insert(position, paragraph)
            position += 1

        for number, challenge in enumerate(capstone["challenges"], 1):
            if number > 1:
                append("break", "", "")
            append("title", capstone["title"], "")
            append("spacer", "", "")
            for kind, text in challenge_paragraphs(challenge, number):
                append(kind, text, challenge["solution"])

    write_docx(template, destination, patch)


def check_solutions(capstone: dict) -> list[str]:
    """Run each reference solution against its canonical checks."""
    failures = []
    for number, challenge in enumerate(capstone["challenges"], 1):
        for check in challenge["checks"]:
            result = subprocess.run(
                [sys.executable, "-c", challenge["solution"]],
                input="\n".join(check["input"]) + "\n",
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            missing = [text for text in check["expect"] if text not in result.stdout]
            if result.returncode or missing:
                failures.append(
                    f"L{capstone['number']:02d} C{number}: solution check "
                    f"{check['input']} missing {missing or result.stderr[-200:]}"
                )
    return failures


def compile_capstones(
    repository_root: Path,
    output_root: Path,
    work_root: Path,
    node: Path,
    doc_renderer: Path,
) -> None:
    """Compile every capstone into the learner and supplemental folders."""
    for capstone in load_capstones():
        failures = check_solutions(capstone)
        if failures:
            raise RuntimeError("; ".join(failures))
        number, title = capstone["number"], capstone["title"]
        learner = lesson_directory(output_root / LEARNER_DIRECTORY, number, title)
        supplemental = lesson_directory(
            output_root / SUPPLEMENTAL_DIRECTORY, number, title
        )
        template = next(
            (output_root / SUPPLEMENTAL_DIRECTORY).glob(
                f"Grade */Lesson {number - 1:02d} - */* - Worksheet.docx"
            )
        )
        stage = work_root / "capstones" / f"lesson{number:02d}"
        stage.mkdir(parents=True, exist_ok=True)
        document = stage / f"{title} - Challenges.docx"
        build_challenge_docx(capstone, template, document)
        subprocess.run(
            [
                sys.executable,
                str(doc_renderer),
                str(document),
                "--output_dir",
                str(stage / "render"),
                "--emit_pdf",
            ],
            check=True,
        )
        learner.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            stage / "render" / f"{document.stem}.pdf",
            learner / f"{title} - Challenges.pdf",
        )
        spec = stage / "capstone.json"
        spec.write_text(json.dumps(capstone, ensure_ascii=False), encoding="utf-8")
        subprocess.run(
            [
                str(node),
                str(PACKAGE_ROOT / "slides/capstones.mjs"),
                str(spec),
                str(repository_root / capstone["deck_template"]),
                str(stage / f"{title} - Slides.pptx"),
                str(stage / "slides"),
            ],
            cwd=repository_root,
            check=True,
        )
        shutil.copyfile(
            stage / f"{title} - Slides.pptx", learner / f"{title} - Slides.pptx"
        )
        solutions = supplemental / "Solutions"
        solutions.mkdir(parents=True, exist_ok=True)
        for index, challenge in enumerate(capstone["challenges"], 1):
            (solutions / f"challenge{index}.py").write_text(
                challenge["solution"] + "\n", encoding="utf-8"
            )
        print(f"compiled capstone Lesson {number:02d} - {title}", flush=True)
