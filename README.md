# Python Programming Lessons K–12

This repository contains the source lessons and compiler inputs for the accepted 20 August 2026 non-capstone curriculum build. It produces the same two folder trees used under OneDrive `Lesson Plans/Resources`:

- `Mapped Curriculum Lessons` — learner PowerPoint, one-page challenge PDF, and starter Python file.
- `Mapped Curriculum Lesson - Supplemental Material` — concept sheet, worksheet, and five solution/debug Python files.

The build contains 33 lessons: 01–10, 12–26, and 28–35. Capstones 11, 27, and 36 are intentionally excluded. Existing Lesson 0 Review and capstone folders in OneDrive are not compilation targets and must remain unchanged.

## Preserved Lesson 01

Lesson 01 is copied byte-for-byte from the pre-run 2024 `Programming Lessons/Lesson Suite/Lesson 01 - Hello Python!` source retained in this repository. It is not passed through the challenge-language compiler. This preserves its original 13-slide deck and companion files.

Lessons 02–35, excluding capstones, are recompiled from the retained source artifacts. The accepted challenge wording, starter-code changes, and solution-code changes are recorded in `lesson_compiler/curriculum/recompilation_run_2026-08-20.json`. This is canonical build data, not an audit archive.

## Requirements

- Python 3.11 or later and the packages in `requirements.txt`.
- Node.js and `@oai/artifact-tool` 2.8.48 (`npm install` inside `lesson_compiler`).
- LibreOffice plus the Codex DOCX renderer. The compiler discovers the bundled renderer automatically. Outside Codex, pass its path with `--doc-renderer` or set `LESSON_DOCX_RENDERER`.

Suggested setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd lesson_compiler
npm install
cd ..
```

## Compile and verify

Run from the repository root. `build/` must not already exist.

```bash
python3 lesson_compiler/src/compile_non_capstone_suite.py
python3 lesson_compiler/src/verify_non_capstone_suite.py
```

The output is written to `build/Recompiled Lesson Suite - Non-Capstone`, with intermediate records and document renders in `build/work`. Verification expects:

- 33 PowerPoint files and 33 one-page challenge PDFs;
- 66 DOCX files and 198 Python files;
- 301 total slide pages: the preserved 13-slide Lesson 01 deck plus 32 nine-slide learner decks;
- no solution slides in recompiled Lessons 02–35;
- exact accepted challenge text across slides, worksheets, and PDFs;
- quoted green string literals and blue code references in recompiled challenge text;
- three-page worksheet render sources before page 2 is extracted as each challenge PDF.

Do not deploy by replacing either Grade folder wholesale. Copy only the compiled lesson directories 01–10, 12–26, and 28–35 into their matching Grade 6–8 locations in both OneDrive trees. This leaves Lesson 0 Review and capstones 11, 27, and 36 untouched.

## Manual inspection note

The compilation and structural checks pass. The only known visual follow-up is manual resizing of unusually long code text boxes, most visibly in Lessons 06, 07, 20, 31, 34, and 35. No capstone compilation is included.
