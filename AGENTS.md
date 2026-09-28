# Lesson compiler workflow

The repository root contains the only current compiled lesson set:

- `Mapped Curriculum Lessons`
- `Mapped Curriculum Lesson - Supplemental Material`

Compiler code, curriculum records, assets, and templates live under
`src/lesson_compiler`.

## Set up

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
npm install
```

The existing compiler also needs its established `render_docx.py` renderer.
Set `LESSON_DOCX_RENDERER` when it cannot be discovered automatically.

## Build

```bash
.venv/bin/lesson-compiler build
```

This compiles and verifies all 33 regular lessons and then the three capstones
(Lessons 11, 27 and 36). By default it writes
the generated files into the two root lesson folders. Use `--output PATH` only
when a separate build is explicitly requested.

Temporary files use `.build/lesson-compiler` and are removed after a passing
build. Failed builds retain this directory for diagnosis.

## Verify without rebuilding

```bash
.venv/bin/lesson-compiler verify
```

## Editing lessons

1. Change canonical lesson content in `src/lesson_compiler/curriculum`. Capstone
   challenges live in `curriculum/capstones.json`; their decks start from
   `templates/capstones`. In challenge prose, write variables as `[name]`; they
   render as shaded variable chips.
2. Change shared formatting behavior in the Python or JavaScript compiler code.
3. Do not hand-edit generated PowerPoint, PDF, Word, or Python outputs unless a
   manual exception is explicitly requested.
4. Run the full build once after changes, then inspect the reported verification.
5. Do not create dated or alternate lesson-suite folders in this repository.
