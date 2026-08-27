"""Tests for challenge-prose semantic formatting."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from lesson_compiler.docx import challenge_semantic_segments
from lesson_compiler.verify import plain


def test_pdf_line_break_hyphens_normalize_without_losing_quotes() -> None:
    """PDF wrapping is ignored while punctuation remains significant."""
    # Arrange
    extracted = 'Use a two-\nletter code and display "Ready".'

    # Act
    normalized = plain(extracted)

    # Assert
    assert normalized == 'Use a two-letter code and display "Ready".'


def test_python_formatter_preserves_prose_and_colours_explicit_code() -> None:
    """The DOCX formatter styles explicit code without rewriting prose."""
    # Arrange
    text = (
        'Use if with a string, an integer and int(). Keep ordinary and black. '
        'Display "Ready". '
        "The user's input and a friend's name remain prose. Words such as stored "
        "and predict must remain unchanged."
    )
    code_context = 'print("and", "red")'

    # Act
    segments = challenge_semantic_segments(text, code_context)

    # Assert
    assert "".join(part for part, _role in segments) == text
    assert ("if", "call") in segments
    assert ("string", "call") in segments
    assert ("integer", "call") in segments
    assert ("int()", "call") in segments
    assert ('"Ready"', "literal") in segments
    assert all(part not in {'"and"', '"red"'} for part, _role in segments)
    assert all(not part.startswith("'") for part, role in segments if role == "literal")


def test_javascript_formatter_preserves_prose_and_colours_explicit_code() -> None:
    """The slide formatter follows the same non-mutating colour contract."""
    # Arrange
    configured_node = os.environ.get("LESSON_COMPILER_NODE")
    node = configured_node or shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not available in this test environment")
    module = (
        Path(__file__).parents[1]
        / "src/lesson_compiler/slides/inline_code_styling.mjs"
    )
    text = (
        'Use if with a string, an integer and int(). Keep ordinary and black. '
        'Display "Ready". '
        "The user's input and a friend's name remain prose. Words such as stored "
        "and predict must remain unchanged."
    )
    script = """
const { buildCodeVocabulary, proseRuns } = await import(process.argv[1]);
const text = process.argv[2];
const vocabulary = buildCodeVocabulary(['print("and", "red")']);
const runs = proseRuns(text, vocabulary);
console.log(JSON.stringify(runs));
"""

    # Act
    completed = subprocess.run(
        [node, "--input-type=module", "-e", script, module.as_uri(), text],
        check=True,
        capture_output=True,
        text=True,
    )
    runs = json.loads(completed.stdout)
    styles = {item["run"]: item["textStyle"] for item in runs}

    # Assert
    assert "".join(item["run"] for item in runs) == text
    assert styles["if"]["color"] == "#1750EB"
    assert styles["string"]["color"] == "#1750EB"
    assert styles["integer"]["color"] == "#1750EB"
    assert styles["int()"]["color"] == "#1750EB"
    assert styles['"Ready"']["color"] == "#067D17"
    assert all(item["run"] not in {'"and"', '"red"'} for item in runs)
    assert all(
        not item["run"].startswith("'")
        for item in runs
        if item["textStyle"]["color"] == "#067D17"
    )
