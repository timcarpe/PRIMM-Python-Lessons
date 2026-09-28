"""Tests for challenge-prose semantic formatting."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from lesson_compiler.docx import (
    challenge_semantic_segments,
    challenge_vocabulary,
    code_semantic_segments,
    display_prose,
    recolor_keyword_runs,
)
from lesson_compiler.paths import CONFIG_PATH, RECORDS_ROOT
from lesson_compiler.support import patch_standard_record
from lesson_compiler.verify import plain

REVISED_PROMPT_CALLS: dict[tuple[int, str], set[str]] = {
    (4, "challenge_1"): {"if", "print()"},
    (4, "challenge_3"): {"if"},
    (7, "challenge_3"): {"if"},
    (9, "challenge_3"): {"while"},
    (10, "challenge_3"): {"for", "while"},
    (12, "challenge_3"): {"strip()", "title()"},
    (17, "challenge_3"): {"list"},
    (25, "challenge_3"): {"for", "len"},
    (26, "challenge_3"): {"list", "for", "range()"},
    (28, "challenge_3"): {"for"},
    (30, "challenge_2"): {"for"},
    (31, "challenge_3"): {"for"},
    (34, "challenge_1"): {"triple", "return"},
    (34, "challenge_2"): {"half", "elif", "else"},
    (34, "challenge_3"): {
        "show_menu()",
        "area",
        "perimeter",
        "return",
    },
    (35, "challenge_3"): {
        "show_records",
        "find_score",
        "return",
    },
}


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
    assert ("if", "keyword") in segments
    assert ("string", "call") in segments
    assert ("integer", "call") in segments
    assert ("int()", "call") in segments
    assert ('"Ready"', "literal") in segments
    assert all(part not in {'"and"', '"red"'} for part, _role in segments)
    assert all(not part.startswith("'") for part, role in segments if role == "literal")


def test_code_segments_follow_compiler_token_colours() -> None:
    """Reviewable code segments preserve the compiler's exact token contract."""
    # Arrange
    code = 'if total > int(input("Number: ")):  # ordinary and\n    print(total)'

    # Act
    segments = code_semantic_segments(code)

    # Assert
    assert "".join(part for part, _role in segments) == code
    assert ("if", "keyword") in segments
    assert ("int", "call") in segments
    assert ("input", "call") in segments
    assert ('"Number: "', "literal") in segments
    assert ("# ordinary and", "comment") in segments


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
    assert styles["if"]["color"] == "#C45E00"
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


def effective_prompts() -> dict[tuple[int, str], tuple[str, str, list[str]]]:
    """Load each effective challenge prompt with its lesson code context.

    Returns:
        Prompt text, code context, and function names keyed by lesson number
        and ``challenge_N`` field.
    """
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    changes: dict[tuple[int, int], str] = {}
    for key, text_value in config["challenge_changes"].items():
        lesson_text, challenge_text = key.split(".")
        changes[(int(lesson_text), int(challenge_text))] = str(text_value)
    prompts: dict[tuple[int, str], tuple[str, str, list[str]]] = {}
    for number_value in config["lesson_numbers"]:
        number = int(number_value)
        record_path = RECORDS_ROOT / f"lesson{number:02d}.json"
        record = patch_standard_record(
            json.loads(record_path.read_text(encoding="utf-8")), changes, config
        )
        code_context = "\n".join(
            [str(record["shared_program"]["code"]), *record["programs"].values()]
        )
        functions = sorted(challenge_vocabulary(code_context)["functions"])
        for index, challenge in enumerate(
            record["worksheet"]["page2"]["challenges"], 1
        ):
            prompts[(number, f"challenge_{index}")] = (
                str(challenge["prompt"]),
                code_context,
                functions,
            )
    return prompts


def test_revised_prompts_colour_programming_items_without_changing_text() -> None:
    """Approved prompts retain text while calls and literals receive roles."""
    # Arrange
    prompts = effective_prompts()

    for key, expected_calls in REVISED_PROMPT_CALLS.items():
        text, code_context, _functions = prompts[key]

        # Act
        segments = challenge_semantic_segments(text, code_context)
        calls = {
            part for part, role in segments if role in {"call", "keyword"}
        }
        literals = {part for part, role in segments if role == "literal"}

        # Assert
        assert "".join(part for part, _role in segments) == text
        assert expected_calls <= calls
        assert set(re.findall(r'"[^"\n]*"', text)) <= literals


def test_javascript_formatter_matches_revised_prompt_colour_contract() -> None:
    """Slide prose applies the same roles to every approved programming item."""
    # Arrange
    configured_node = os.environ.get("LESSON_COMPILER_NODE")
    node = configured_node or shutil.which("node")
    if node is None:
        pytest.skip("Node.js is not available in this test environment")
    module = (
        Path(__file__).parents[1]
        / "src/lesson_compiler/slides/inline_code_styling.mjs"
    )
    prompts = effective_prompts()
    payload = []
    for key, expected_calls in REVISED_PROMPT_CALLS.items():
        text, _code_context, functions = prompts[key]
        payload.append(
            {
                "text": text,
                "functions": functions,
                "expected": sorted(expected_calls),
            }
        )
    script = """
const { proseRuns } = await import(process.argv[1]);
const payload = JSON.parse(process.argv[2]);
console.log(JSON.stringify(payload.map((item) => ({
  ...item,
  runs: proseRuns(item.text, { functions: new Set(item.functions) }),
}))));
"""

    # Act
    completed = subprocess.run(
        [
            node,
            "--input-type=module",
            "-e",
            script,
            module.as_uri(),
            json.dumps(payload),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    # Assert
    for item in json.loads(completed.stdout):
        chips = re.sub(r"\[([A-Za-z_]\w*)\]", "\u202f\\1\u202f", item["text"])
        assert "".join(run["run"] for run in item["runs"]) == chips
        blue = {
            run["run"]
            for run in item["runs"]
            if run["textStyle"]["color"] in {"#1750EB", "#C45E00"}
        }
        green = {
            run["run"]
            for run in item["runs"]
            if run["textStyle"]["color"] == "#067D17"
        }
        assert set(item["expected"]) <= blue
        assert set(re.findall(r'"[^"\n]*"', item["text"])) <= green


def test_english_else_is_not_coloured() -> None:
    """Only the else keyword is orange, not English such as "anything else"."""
    # Arrange
    text = 'Use if and else. For anything else, display "Invalid".'

    # Act
    segments = challenge_semantic_segments(text)

    # Assert
    keywords = [part for part, role in segments if role == "keyword"]
    assert keywords == ["if", "else"]


def test_variable_markers_become_chips_without_losing_literals() -> None:
    """Bracketed variables become chips, including inside quoted output text."""
    # Arrange
    text = 'Store it in [total]. Display "Hello, [name]" and [total].'

    # Act
    segments = challenge_semantic_segments(text)

    # Assert
    assert "".join(part for part, _role in segments) == text
    assert [part for part, role in segments if role == "variable"] == [
        "[total]",
        "[name]",
        "[total]",
    ]
    assert ('"Hello, ', "literal") in segments
    assert ('"', "literal") in segments


def test_chip_padding_matches_prompt_text_after_normalizing() -> None:
    """Verification ignores chip padding that extractors report as spaces."""
    # Arrange
    prompt = "Store 2 in [divisor]. Divide [total] by [divisor]."
    extracted = "Store 2 in  divisor  . Divide  total  by\n divisor ."

    # Act
    needle = plain(display_prose(prompt))

    # Assert
    assert needle in plain(extracted)


def test_inherited_keyword_runs_are_recoloured_orange() -> None:
    """Code keywords turn orange; keywords inside English notes turn black."""
    # Arrange
    from lxml import etree

    w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    font = '<w:rFonts w:ascii="JetBrains Mono" w:hAnsi="JetBrains Mono"/>'

    def run(text: str, color: str, fonts: str = font) -> str:
        return (
            f'<w:r><w:rPr>{fonts}<w:color w:val="{color}"/></w:rPr>'
            f'<w:t xml:space="preserve">{text}</w:t></w:r>'
        )

    root = etree.fromstring(
        f'<w:body xmlns:w="{w}">'
        f'<w:p>{run("if", "1750EB")}{run(" x == 1:", "080808")}</w:p>'
        f'<w:p>{run("print", "1750EB")}{run("(x)", "080808")}</w:p>'
        f'<w:p>{run("import random", "080808")}</w:p>'
        f'<w:p>{run("1 ", "080808", "")}{run("and", "1750EB", "")}'
        f'{run(" 6 can both be rolled", "080808", "")}</w:p>'
        f'<w:p>{run("Say what is shown", "080808")}</w:p>'
        "</w:body>"
    )

    # Act
    recolor_keyword_runs(root)

    # Assert
    runs = [
        (
            "".join(item.itertext()),
            item.find(f"{{{w}}}rPr/{{{w}}}color").get(f"{{{w}}}val"),
        )
        for item in root.iter(f"{{{w}}}r")
    ]
    assert runs == [
        ("if", "C45E00"),
        (" x == 1:", "080808"),
        ("print", "1750EB"),
        ("(x)", "080808"),
        ("import", "C45E00"),
        (" random", "080808"),
        ("1 ", "080808"),
        ("and", "080808"),
        (" 6 can both be rolled", "080808"),
        ("Say what is shown", "080808"),
    ]
