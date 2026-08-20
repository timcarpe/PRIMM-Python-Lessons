from __future__ import annotations

import ast
import json
import re
from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"
NS = {"w": W_NS}
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A = f"{{{A_NS}}}"
R = f"{{{R_NS}}}"

TOKEN_RE = re.compile(
    r"(#[^\n]*|\"[^\"\n]*\"|'[^'\n]*'|\.(?:strip|title|append)\b|"
    r"\b(?:print|input|int|range|len|def|return|if|elif|else|for|while|and|or|not|in|True|False)\b|"
    r"(?:==|!=|<=|>=|<|>))"
)
KEYWORDS = {"print", "input", "int", "range", "len", "def", "return", "if", "elif", "else", "for", "while", "and", "or", "not", "in", "True", "False"}
INLINE_TYPES = {"integer", "integers", "string", "strings", "list", "lists", "dictionary", "dictionaries", "boolean", "booleans"}
UNAMBIGUOUS_INLINE_KEYWORDS = {"def", "return", "elif", "else", "break", "continue"}
BUILTIN_CALLS = {"print", "input", "int", "str", "float", "bool", "range", "len", "list", "dict", "set", "tuple", "sum", "max", "min"}


def normalize_code(value: str) -> str:
    return value.replace('" )', '")')


def first_run_properties(paragraph: etree._Element) -> etree._Element | None:
    run = paragraph.find(".//w:r", NS)
    if run is None:
        return None
    rpr = run.find("w:rPr", NS)
    return deepcopy(rpr) if rpr is not None else None


def clear_paragraph_content(paragraph: etree._Element) -> None:
    for child in list(paragraph):
        if child.tag != W + "pPr":
            paragraph.remove(child)


def token_color(token: str) -> str:
    if token.startswith("#"):
        return "666666"
    if token.startswith(("\"", "'")):
        return "067D17"
    if token.startswith(".") or token in KEYWORDS:
        return "1750EB"
    return "080808"


def add_text_run(paragraph: etree._Element, text: str, rpr: etree._Element | None = None, color: str | None = None, typeface: str | None = None) -> None:
    run = etree.SubElement(paragraph, W + "r")
    if rpr is not None:
        run.append(deepcopy(rpr))
    if color:
        props = run.find(W + "rPr")
        if props is None:
            props = etree.Element(W + "rPr")
            run.insert(0, props)
        existing = props.find(W + "color")
        if existing is None:
            existing = etree.SubElement(props, W + "color")
        existing.set(W + "val", color)
    if typeface:
        props = run.find(W + "rPr")
        if props is None:
            props = etree.Element(W + "rPr")
            run.insert(0, props)
        fonts = props.find(W + "rFonts")
        if fonts is None:
            fonts = etree.SubElement(props, W + "rFonts")
        fonts.set(W + "ascii", typeface)
        fonts.set(W + "hAnsi", typeface)
    node = etree.SubElement(run, W + "t")
    if text.startswith(" ") or text.endswith(" ") or "  " in text:
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    node.text = text


def set_plain(paragraph: etree._Element, text: str) -> None:
    rpr = first_run_properties(paragraph)
    clear_paragraph_content(paragraph)
    add_text_run(paragraph, text, rpr)


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def challenge_vocabulary(code_context: str = "") -> dict[str, set[str]]:
    functions = set(BUILTIN_CALLS)
    strings: set[str] = set()
    for match in re.finditer(r'("[^"\n]*"|\'[^\'\n]*\')', code_context):
        value = match.group(0)[1:-1].strip()
        if len(value) >= 2 and not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", value):
            strings.add(value)
    for match in re.finditer(r"\bdef\s+([A-Za-z_]\w*)\s*\(", code_context):
        functions.add(match.group(1))
    for match in re.finditer(r"\b((?:[A-Za-z_]\w*\.)*[A-Za-z_]\w*)\s*\(", code_context):
        name = match.group(1)
        functions.add(name)
        functions.add(name.rsplit(".", 1)[-1])
    try:
        tree = ast.parse(normalize_code(code_context))
    except SyntaxError:
        tree = None
    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.add(node.name)
            elif isinstance(node, ast.Call):
                name = _call_name(node.func)
                if name:
                    functions.add(name)
                    functions.add(name.rsplit(".", 1)[-1])
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                value = node.value.strip()
                if len(value) >= 2 and not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", value):
                    strings.add(value)
    return {"functions": functions, "strings": strings}


def challenge_semantic_segments(text: str, code_context: str = "") -> list[tuple[str, str]]:
    """Apply the suite's narrow inline-code contract to learner prose.

    This extends the original challenge-PDF semantic pass: exact program
    string literals are green; explicit calls, types and unambiguous named
    keywords are blue; ordinary prose, variables and operators stay black.
    """
    vocabulary = challenge_vocabulary(code_context)
    spans: list[tuple[int, int, str]] = []
    for match in re.finditer(r'("[^"\n]*"|“[^”\n]*”|\'[^\'\n]*\')', text):
        spans.append((match.start(), match.end(), "literal"))
    for literal in sorted(vocabulary["strings"], key=len, reverse=True):
        cursor = 0
        while True:
            start = text.find(literal, cursor)
            if start < 0:
                break
            spans.append((start, start + len(literal), "literal"))
            cursor = start + len(literal)
    function_pattern = "|".join(re.escape(name) for name in sorted(vocabulary["functions"], key=len, reverse=True))
    if function_pattern:
        for match in re.finditer(rf"\b(?:{function_pattern})(?=\s*\()", text):
            spans.append((match.start(), match.end(), "call"))
        for match in re.finditer(rf"\b(?:{function_pattern})\s*\(\s*\)", text):
            spans.append((match.start(), match.end(), "call"))
    for match in re.finditer(r"\b[A-Za-z_]\w*\.py\b", text):
        spans.append((match.start(), match.end(), "call"))
    for match in re.finditer(r"\b[A-Za-z_]\w*\b", text):
        token = match.group(0)
        if token in UNAMBIGUOUS_INLINE_KEYWORDS or token.lower() in INLINE_TYPES:
            spans.append((match.start(), match.end(), "call"))
    for match in re.finditer(r"\b(?:use|using|add|write|include|with|a|an)\s+(if|for|while)\b", text, re.I):
        spans.append((match.start(1), match.end(1), "call"))
    for match in re.finditer(r"\b(?:if|for|while)\b(?=\s+(?:statement|condition|loop|keyword|branch))", text):
        spans.append((match.start(), match.end(), "call"))
    for match in re.finditer(r"\b(?:and|or|not|in)\b(?=\s+(?:operator|condition|keyword))", text):
        spans.append((match.start(), match.end(), "call"))
    priority = {"literal": 2, "call": 1}
    chosen: list[tuple[int, int, str]] = []
    for start, end, role in sorted(spans, key=lambda item: (item[0], -priority[item[2]], -(item[1] - item[0]))):
        if any(not (end <= other_start or start >= other_end) for other_start, other_end, _ in chosen):
            continue
        chosen.append((start, end, role))
    chosen.sort()
    parts: list[tuple[str, str]] = []
    cursor = 0
    for start, end, role in chosen:
        if start > cursor:
            parts.append((text[cursor:start], "ordinary"))
        parts.append((text[start:end], role))
        cursor = end
    if cursor < len(text):
        parts.append((text[cursor:], "ordinary"))
    return parts or [(text, "ordinary")]


def quote_exact_string_references(text: str, code_context: str = "") -> str:
    vocabulary = challenge_vocabulary(code_context)
    quoted = [(match.start(), match.end()) for match in re.finditer(r'("[^"\n]*"|\'[^\'\n]*\')', text)]
    replacements: list[tuple[int, int, str]] = []
    for literal in sorted(vocabulary["strings"], key=len, reverse=True):
        cursor = 0
        while True:
            start = text.find(literal, cursor)
            if start < 0:
                break
            end = start + len(literal)
            if not any(start >= left and end <= right for left, right in quoted):
                replacements.append((start, end, f'"{literal}"'))
            cursor = end
    for start, end, replacement in sorted(replacements, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def set_challenge_prompt(paragraph: etree._Element, text: str, code_context: str = "") -> None:
    """Write a learner prompt with the inherited readable paragraph rhythm.

    Exact-height spacing is reserved for empty cadence spacers.  Prompts can
    wrap, so their line height must remain automatic rather than compressed.
    """
    text = quote_exact_string_references(text, code_context)
    rpr = first_run_properties(paragraph)
    removable = [
        child for child in list(paragraph)
        if child.tag == W + "r" and all(grandchild.tag in {W + "rPr", W + "t"} for grandchild in child)
    ]
    if not removable:
        raise ValueError("challenge prompt has no safe text-only runs")
    insert_at = list(paragraph).index(removable[0])
    for child in removable:
        paragraph.remove(child)
    inserted = 0
    for part, role in challenge_semantic_segments(text, code_context):
        if not part:
            continue
        color = None if role == "ordinary" else ("067D17" if role == "literal" else "1750EB")
        holder = etree.Element(W + "p")
        add_text_run(holder, part, rpr, color or "080808", "Consolas" if role != "ordinary" else None)
        paragraph.insert(insert_at + inserted, holder[-1])
        inserted += 1


def set_spacer_height(paragraph: etree._Element, points: int) -> None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        ppr = etree.Element(W + "pPr")
        paragraph.insert(0, ppr)
    spacing = ppr.find("w:spacing", NS)
    if spacing is None:
        spacing = etree.SubElement(ppr, W + "spacing")
    spacing.set(W + "before", "0")
    spacing.set(W + "after", "0")
    spacing.set(W + "line", str(points * 20))
    spacing.set(W + "lineRule", "exact")


def set_code(paragraph: etree._Element, code: str, size_half_points: int | None = None) -> None:
    code = normalize_code(code)
    rpr = first_run_properties(paragraph)
    if size_half_points is not None:
        if rpr is None:
            rpr = etree.Element(W + "rPr")
        for tag in (W + "sz", W + "szCs"):
            size = rpr.find(tag)
            if size is None:
                size = etree.SubElement(rpr, tag)
            size.set(W + "val", str(size_half_points))
    clear_paragraph_content(paragraph)
    lines = code.splitlines()
    for line_index, line in enumerate(lines):
        cursor = 0
        for match in TOKEN_RE.finditer(line):
            if match.start() > cursor:
                add_text_run(paragraph, line[cursor : match.start()], rpr, "080808")
            token = match.group(0)
            add_text_run(paragraph, token, rpr, token_color(token), "Consolas" if token in {"==", "!=", "<=", ">=", "<", ">"} else None)
            cursor = match.end()
        if cursor < len(line):
            add_text_run(paragraph, line[cursor:], rpr, "080808")
        if line_index < len(lines) - 1:
            run = etree.SubElement(paragraph, W + "r")
            if rpr is not None:
                run.append(deepcopy(rpr))
            etree.SubElement(run, W + "br")


def write_docx(source: Path, destination: Path, patcher, media_replacements: dict[str, bytes] | None = None) -> None:
    with ZipFile(source) as archive:
        entries = {name: archive.read(name) for name in archive.namelist()}
    root = etree.fromstring(entries["word/document.xml"])
    patcher(root)
    entries["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")
    for name, data in (media_replacements or {}).items():
        if name not in entries:
            raise ValueError(f"template media entry is missing: {name}")
        entries[name] = data
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(entries):
            info = ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, entries[name])


def patch_concept(root: etree._Element, curriculum: dict) -> None:
    body = root.find("w:body", NS)
    assert body is not None
    children = list(body)
    content = curriculum["concept_sheet"]
    set_plain(children[0], content["title"])
    set_plain(children[2], content["intro"])
    starts = [4, 10, 16, 22, 28]
    for start, block in zip(starts, content["blocks"], strict=True):
        set_plain(children[start], block["term"])
        set_plain(children[start + 1], "Definition: ")
        set_plain(children[start + 2], block["definition"])
        set_plain(children[start + 3], "Example:")
        set_code(children[start + 4], block["example"])


def page2_code_display(shared: str) -> str:
    lines = normalize_code(shared).splitlines()
    if len(lines) == 4:
        return "\n".join([lines[0], lines[1], "", lines[2], "", lines[3]])
    if len(lines) == 3:
        return "\n".join([lines[0], lines[1], "", lines[2], " ", " "])
    if len(lines) == 5:
        return "\n".join([lines[0], lines[1], "", lines[2], lines[3], lines[4]])
    if len(lines) <= 6:
        return "\n".join(lines)
    return "\n".join(lines)


def page2_code_size(shared: str) -> int | None:
    return 20 if len(normalize_code(shared).splitlines()) >= 7 else None


def page2_spacer_heights(curriculum: dict) -> dict[int, int]:
    """Return the inherited Lesson 1/2 challenge-page spacing unchanged."""
    return {30: 3, 32: 5, 34: 6, 37: 6, 40: 6, 43: 4}


def patch_worksheet(root: etree._Element, curriculum: dict, lesson2_anchor: etree._Element) -> None:
    body = root.find("w:body", NS)
    assert body is not None
    c = list(body)
    worksheet = curriculum["worksheet"]
    shared = normalize_code(curriculum["shared_program"]["code"])
    code_context = "\n".join([shared, *curriculum.get("programs", {}).values()])
    drawing = root.find(".//w:drawing", NS)
    if drawing is None or len(drawing) != 1:
        raise ValueError("Lesson 1 worksheet must contain one replaceable drawing")
    old_blip = drawing.find(".//" + A + "blip")
    new_anchor = deepcopy(lesson2_anchor)
    new_blip = new_anchor.find(".//" + A + "blip")
    if old_blip is None or new_blip is None:
        raise ValueError("worksheet drawing relationship is missing")
    new_blip.set(R + "embed", old_blip.get(R + "embed"))
    drawing.replace(drawing[0], new_anchor)

    for index in (0, 26, 44):
        set_plain(c[index], worksheet["title"])
    set_plain(c[2], worksheet["page1"]["look_heading"])
    set_code(c[3], shared)
    set_plain(c[6], worksheet["page1"]["predict_heading"])
    set_plain(c[9], worksheet["page1"]["run_heading"])
    set_plain(c[12], worksheet["page1"]["investigate_heading"])
    for index, question in zip((13, 16, 19, 22), worksheet["page1"]["investigate_questions"], strict=True):
        set_plain(c[index], question)

    if curriculum["lesson"]["number"] == 8:
        # The dense but readable Investigation page leaves the inherited
        # manual page-break paragraph just below the page edge.  Zero only
        # the existing empty paragraph and the break paragraph so the break
        # remains on page 1 instead of producing a blank page 2.
        set_spacer_height(c[24], 0)
        set_spacer_height(c[25], 0)

    set_plain(c[28], worksheet["page2"]["reference_heading"])
    set_code(c[29], page2_code_display(shared), page2_code_size(shared))
    set_plain(c[31], worksheet["page2"]["instruction"])
    set_plain(c[33], worksheet["page2"]["heading"])
    for spacer_index, points in page2_spacer_heights(curriculum).items():
        set_spacer_height(c[spacer_index], points)
    for heading_index, prompt_index, challenge in zip((35, 38, 41), (36, 39, 42), worksheet["page2"]["challenges"], strict=True):
        set_plain(c[heading_index], challenge["title"])
        set_challenge_prompt(c[prompt_index], challenge["prompt"], code_context)

    page3 = worksheet["page3"]
    set_plain(c[46], page3["heading"])
    set_plain(c[47], page3["instruction"])
    set_code(c[49], curriculum["programs"]["broken"])
    set_plain(c[52], page3["rewrite"])
    set_plain(c[56], page3["test"])
    set_plain(c[59], page3["reflect"])


def compile_documents(root: Path, curriculum_path: Path, output_dir: Path) -> list[Path]:
    curriculum = json.loads(curriculum_path.read_text())
    title = curriculum["lesson"]["title"]
    source_dir = root / "Example Output/Lesson Suite/Lesson 01 - Hello Python!"
    concept_source = source_dir / "Hello Python! - Concept Sheet.docx"
    worksheet_source = source_dir / "Hello Python! - Worksheet.docx"
    lesson2_worksheet = root / "Example Output/Lesson Suite/Lesson 02 - Operators and Integers/Operators and Integers - Worksheet.docx"
    concept_out = output_dir / f"{title} - Concept Sheet.docx"
    worksheet_out = output_dir / f"{title} - Worksheet.docx"
    write_docx(concept_source, concept_out, lambda xml: patch_concept(xml, curriculum))
    worksheet_art = (root / curriculum["assets"]["worksheet"]).read_bytes()
    with ZipFile(lesson2_worksheet) as archive:
        lesson2_root = etree.fromstring(archive.read("word/document.xml"))
    lesson2_drawing = lesson2_root.find(".//w:drawing", NS)
    if lesson2_drawing is None or len(lesson2_drawing) != 1:
        raise ValueError("Lesson 2 worksheet must contain one placement-authority drawing")
    lesson2_anchor = deepcopy(lesson2_drawing[0])
    write_docx(
        worksheet_source,
        worksheet_out,
        lambda xml: patch_worksheet(xml, curriculum, lesson2_anchor),
        {"word/media/image3.png": worksheet_art},
    )
    return [concept_out, worksheet_out]
