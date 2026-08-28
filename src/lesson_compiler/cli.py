"""Command-line interface for building and verifying the lesson suite."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from lesson_compiler.build import build_suite
from lesson_compiler.paths import DEFAULT_REPOSITORY_ROOT, DEFAULT_REVIEW_TOOL_PATH
from lesson_compiler.review_tool import build_review_tool
from lesson_compiler.verify import verify_suite


def parser() -> argparse.ArgumentParser:
    """Create the lesson compiler argument parser."""
    command_parser = argparse.ArgumentParser(
        prog="lesson-compiler",
        description="Build and verify the mapped Python lesson suite.",
    )
    commands = command_parser.add_subparsers(dest="command", required=True)

    build = commands.add_parser("build", help="compile and verify every lesson")
    build.add_argument(
        "--repository",
        type=Path,
        default=DEFAULT_REPOSITORY_ROOT,
        help="repository containing the canonical lesson folders",
    )
    build.add_argument(
        "--output",
        type=Path,
        help="output root; defaults to the repository root",
    )
    build.add_argument("--work", type=Path, help="temporary compiler workspace")
    build.add_argument("--node", type=Path, help="Node.js executable")
    build.add_argument(
        "--doc-renderer",
        type=Path,
        help="existing render_docx.py executable",
    )
    build.add_argument(
        "--keep-work",
        action="store_true",
        help="retain temporary renders after a successful build",
    )

    verify = commands.add_parser("verify", help="verify the current lesson folders")
    verify.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REPOSITORY_ROOT,
        help="root containing the two lesson folders",
    )

    review = commands.add_parser(
        "review-tool", help="generate the browser-based manifest review tool"
    )
    review.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REVIEW_TOOL_PATH,
        help="self-contained HTML output path",
    )
    return command_parser


def run_build(args: argparse.Namespace) -> dict[str, object]:
    """Build, verify, and clean temporary compiler files."""
    repository = args.repository.resolve()
    output = (args.output or repository).resolve()
    work = (args.work or repository / ".build/lesson-compiler").resolve()
    if work.exists():
        shutil.rmtree(work)
    try:
        build_suite(
            repository_root=repository,
            output_root=output,
            work_root=work,
            node=args.node,
            doc_renderer=args.doc_renderer,
        )
        report = verify_suite(output, work)
    except Exception:
        print(f"Build workspace retained for diagnosis: {work}")
        raise
    if not report["passed"]:
        print(f"Build workspace retained for diagnosis: {work}")
        return report
    if not args.keep_work:
        shutil.rmtree(work)
        build_parent = work.parent
        if build_parent.exists() and not any(build_parent.iterdir()):
            build_parent.rmdir()
    return report


def main() -> None:
    """Run the requested compiler command."""
    arguments = parser().parse_args()
    if arguments.command == "build":
        report = run_build(arguments)
    elif arguments.command == "verify":
        report = verify_suite(arguments.output)
    else:
        report = build_review_tool(arguments.output)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed"] else 1)
