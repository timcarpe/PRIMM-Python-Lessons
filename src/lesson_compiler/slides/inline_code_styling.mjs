const GREEN = "#067D17";
const BLUE = "#1750EB";
const BLACK = "#080808";
const UNAMBIGUOUS_KEYWORDS = new Set(["def", "return", "elif", "else", "break", "continue"]);
const INLINE_TYPES = new Set(["integer", "integers", "string", "strings", "list", "lists", "dictionary", "dictionaries", "boolean", "booleans"]);

export function buildCodeVocabulary(codeBlobs = []) {
  const functions = new Set(["print", "input", "int", "str", "float", "bool", "range", "len", "list", "dict", "set", "tuple", "sum", "max", "min"]);
  for (const value of codeBlobs.filter(Boolean)) {
    const code = String(value);
    for (const match of code.matchAll(/\bdef\s+([A-Za-z_]\w*)\s*\(/g)) functions.add(match[1]);
    for (const match of code.matchAll(/\b((?:[A-Za-z_]\w*\.)+[A-Za-z_]\w*)\s*\(/g)) functions.add(match[1]);
  }
  return { functions };
}

function candidates(text, vocabulary) {
  const found = [];
  const add = (start, end, color) => {
    if (start >= 0 && end > start) found.push({ start, end, color });
  };
  for (const match of text.matchAll(/("[^"\n]*"|(?<![A-Za-z0-9_])'[^'\n]*'(?![A-Za-z0-9_]))/g)) add(match.index, match.index + match[0].length, GREEN);
  for (const match of text.matchAll(/\b(?:[A-Za-z_]\w*\.)*[A-Za-z_]\w*\s*\(\s*\)/g)) add(match.index, match.index + match[0].length, BLUE);
  for (const match of text.matchAll(/\b(?:[A-Za-z_]\w*\.)*[A-Za-z_]\w*(?=\s*\()/g)) {
    const name = match[0];
    if (vocabulary.functions?.has(name) || vocabulary.functions?.has(name.split(".").at(-1))) add(match.index, match.index + name.length, BLUE);
  }
  for (const match of text.matchAll(/\b[A-Za-z_]\w*\.py\b/g)) add(match.index, match.index + match[0].length, BLUE);
  for (const match of text.matchAll(/\b[A-Za-z_]\w*\b/g)) {
    if (UNAMBIGUOUS_KEYWORDS.has(match[0]) || INLINE_TYPES.has(match[0].toLowerCase())) add(match.index, match.index + match[0].length, BLUE);
  }
  for (const match of text.matchAll(/\b(?:use|using|add|write|include|with|a|an)\s+(if|for|while)\b/gi)) {
    const token = match[1];
    const start = match.index + match[0].lastIndexOf(token);
    add(start, start + token.length, BLUE);
  }
  for (const match of text.matchAll(/\b(?:if|for|while)\b(?=\s+(?:statement|condition|loop|keyword|branch))/g)) add(match.index, match.index + match[0].length, BLUE);
  for (const match of text.matchAll(/\b(?:and|or|not|in)\b(?=\s+(?:operator|condition|keyword))/g)) add(match.index, match.index + match[0].length, BLUE);
  return found.sort((a, b) => a.start - b.start || (b.end - b.start) - (a.end - a.start));
}

export function proseRuns(text, vocabulary, { fontSize = "18pt", typeface = "Arial", bold = false } = {}) {
  text = String(text);
  const base = { color: BLACK, typeface, fontSize, bold };
  const selected = [];
  let occupiedUntil = -1;
  for (const item of candidates(text, vocabulary)) {
    if (item.start < occupiedUntil) continue;
    selected.push(item);
    occupiedUntil = item.end;
  }
  const runs = [];
  let cursor = 0;
  for (const item of selected) {
    if (item.start > cursor) runs.push({ run: text.slice(cursor, item.start), textStyle: base });
    runs.push({ run: text.slice(item.start, item.end), textStyle: { ...base, color: item.color, typeface: "JetBrains Mono" } });
    cursor = item.end;
  }
  if (cursor < text.length) runs.push({ run: text.slice(cursor), textStyle: base });
  return runs.length ? runs : [{ run: " ", textStyle: base }];
}

export function proseParagraphs(text, vocabulary, options = {}) {
  const { spaceAfter = 0, ...runOptions } = options;
  return String(text).split("\n").map((line) => ({
    runs: proseRuns(line, vocabulary, runOptions),
    bulletCharacter: "",
    marginLeft: 0,
    indent: 0,
    spaceAfter,
  }));
}
