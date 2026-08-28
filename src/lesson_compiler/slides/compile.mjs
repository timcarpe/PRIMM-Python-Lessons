import fs from "node:fs/promises";
import path from "node:path";
import { execFile as execFileCallback } from "node:child_process";
import { promisify } from "node:util";
import { FileBlob, Presentation, PresentationFile } from "@oai/artifact-tool";
import { buildCodeVocabulary, proseParagraphs } from "./inline_code_styling.mjs";

const execFile = promisify(execFileCallback);
const root = process.argv[2];
const curriculumPath = process.argv[3];
const outputPath = process.argv[4];
const renderDir = process.argv[5];
const starterPath = process.argv[6];
const learnerOnly = process.argv.includes("--learner-only");
if (!root || !curriculumPath || !outputPath || !renderDir) {
  throw new Error("usage: compile.mjs ROOT CURRICULUM OUTPUT RENDER_DIR [STARTER_PPTX]");
}

const curriculum = JSON.parse(await fs.readFile(curriculumPath, "utf8"));
const challengeVocabulary = buildCodeVocabulary([
  curriculum.shared_program?.code,
  ...Object.values(curriculum.programs ?? {}),
]);
const templatePath = starterPath || path.join(root, "src/lesson_compiler/templates/template-starter.pptx");
const presentation = await PresentationFile.importPptx(await FileBlob.load(templatePath));
const sourceProto = presentation.toProto();
const normalize = (value) => value.replaceAll('" )', '")');

const inspection = await presentation.inspect({
  kind: "textbox,shape",
  include: "id,slide,name,textPreview,bbox",
  maxChars: 1000000,
});
const records = inspection.ndjson.split(/\r?\n/).filter(Boolean).map((line) => JSON.parse(line));
const shapeId = (slide, name, occurrence = 0) => {
  const matches = records.filter((record) => record.kind === "textbox" && record.slide === slide && record.name === name);
  if (!matches[occurrence]) throw new Error(`Missing ${name} occurrence ${occurrence} on slide ${slide}`);
  return matches[occurrence].id;
};
const target = (slide, name, occurrence = 0) => presentation.resolve(shapeId(slide, name, occurrence));
const setText = (slide, name, text, occurrence = 0) => {
  const shape = target(slide, name, occurrence);
  shape.text = text;
  if (name === "Title 1") {
    // Keep the inherited title box, but make its one-line geometry explicit.
    // This prevents long solution headings from overflowing into the next frame.
    shape.text.wrap = "none";
    shape.text.autoFit = "shrinkText";
    shape.text.verticalAlignment = "middle";
  }
};

const tokenPattern = /(#[^\n]*|"[^"\n]*"|'[^'\n]*'|\.(?:strip|title|append)\b|\b(?:print|input|int|range|len|def|return|if|elif|else|for|while|and|or|not|in|True|False)\b|(?:==|!=|<=|>=|<|>))/g;
const keywordTokens = new Set(["print", "input", "int", "range", "len", "def", "return", "if", "elif", "else", "for", "while", "and", "or", "not", "in", "True", "False"]);
function tokenColor(token) {
  if (token.startsWith("#")) return "#8C8C8C";
  if (token.startsWith("\"") || token.startsWith("'")) return "#067D17";
  if (token.startsWith(".") || keywordTokens.has(token)) return "#1750EB";
  return "#080808";
}

function codeRuns(
  code,
  { fontSize = "20pt", leadingBlankLines = 0, compactLines = false } = {},
) {
  const style = { color: "#080808", typeface: "JetBrains Mono", fontSize };
  const styledRuns = (line) => {
    const runs = [];
    let cursor = 0;
    for (const match of line.matchAll(tokenPattern)) {
      const index = match.index ?? 0;
      if (index > cursor) runs.push({ run: line.slice(cursor, index), textStyle: style });
      const token = match[0];
      runs.push({ run: token, textStyle: { color: tokenColor(token), typeface: /^(==|!=|<=|>=|<|>)$/.test(token) ? "Consolas" : "JetBrains Mono", fontSize } });
      cursor = index + token.length;
    }
    if (cursor < line.length) runs.push({ run: line.slice(cursor), textStyle: style });
    return runs;
  };
  const lines = normalize(code).split("\n");
  if (compactLines) {
    const runs = [];
    for (const [index, line] of lines.entries()) {
      if (index > 0) runs.push({ run: "\n", textStyle: style });
      runs.push(...styledRuns(line));
    }
    return [{
      runs: runs.length ? runs : [{ run: " ", textStyle: style }],
      bulletCharacter: "",
      marginLeft: 0,
      indent: 0,
      spaceAfter: 0,
      lineSpacingPercent: 90000,
    }];
  }
  const paragraphs = Array.from({ length: leadingBlankLines }, () => ({
    runs: [{ run: " ", textStyle: style }],
    bulletCharacter: "",
    marginLeft: 0,
    indent: 0,
    spaceAfter: 0,
  }));
  for (const line of lines) {
    const runs = styledRuns(line);
    paragraphs.push({ runs: runs.length ? runs : [{ run: " ", textStyle: style }], bulletCharacter: "", marginLeft: 0, indent: 0, spaceAfter: 0 });
  }
  return paragraphs;
}

const setCode = (slide, name, code, occurrence = 0, options = {}) => {
  const shape = target(slide, name, occurrence);
  shape.text.set(codeRuns(code, options));
  if (options.verticalAlignment) shape.text.verticalAlignment = options.verticalAlignment;
  if (options.autoFit) shape.text.autoFit = options.autoFit;
};

const setPlainLines = (slide, name, text, occurrence = 0) => {
  const paragraphs = text.split("\n").map((line, index) => ({
    runs: [{ run: line, textStyle: index === 0 ? { bold: true, fontSize: "26pt" } : { fontSize: "20pt" } }],
    bulletCharacter: "",
    marginLeft: 0,
    indent: 0,
    spaceAfter: index === 0 ? 16 : 8,
  }));
  target(slide, name, occurrence).text.set(paragraphs);
};

const setChallengeText = (slide, name, text, occurrence = 0) => {
  const shape = target(slide, name, occurrence);
  shape.text.set(proseParagraphs(text, challengeVocabulary, { fontSize: "24pt", typeface: "Calibri" }));
};

const setDebug = (slide, name, body, code, occurrence = 0) => {
  const prefix = "This code has errors!";
  const remainder = body.startsWith(prefix) ? body.slice(prefix.length) : ` ${body}`;
  const paragraphs = [{
    runs: [
      { run: prefix, textStyle: { bold: true, color: "#FF0000", fontSize: "28pt" } },
      { run: remainder, textStyle: { bold: true, color: "#080808", fontSize: "28pt" } },
    ],
    bulletCharacter: "",
    marginLeft: 0,
    indent: 0,
    spaceAfter: 0,
  }, {
    runs: [{ run: " ", textStyle: { typeface: "JetBrains Mono", fontSize: "18pt" } }],
    bulletCharacter: "",
    marginLeft: 0,
    indent: 0,
    spaceAfter: 0,
  }, ...codeRuns(code, { fontSize: "18pt" })];
  target(slide, name, occurrence).text.set(paragraphs);
};

const shared = curriculum.shared_program.code;
const sharedLineCount = normalize(shared).split("\n").length;
const compactSharedFontSize = sharedLineCount > 10
  ? "11pt"
  : sharedLineCount > 8
    ? "12pt"
    : sharedLineCount > 5
      ? "14pt"
      : "16pt";
const programs = curriculum.programs;
const slides = curriculum.slides;
setText(1, "Title 1", slides[0].title);
setText(1, "Subtitle 2", slides[0].subtitle);
setCode(2, "Rectangle 1", shared, 0, { fontSize: "24pt", verticalAlignment: "top", autoFit: "shrinkText" });
setText(3, "Title 1", slides[2].title);
setCode(3, "Rectangle 1", shared, 0, { fontSize: "24pt", verticalAlignment: "top", autoFit: "shrinkText" });
setText(4, "Title 1", slides[3].title);
setCode(4, "Rectangle 1", shared, 0, { fontSize: "24pt", verticalAlignment: "top", autoFit: "shrinkText" });
setText(5, "Title 1", slides[4].title);
setPlainLines(5, "Rectangle 1", slides[4].body, 0);
setCode(5, "Rectangle 1", shared, 1, { fontSize: compactSharedFontSize, verticalAlignment: "top", autoFit: "shrinkText", compactLines: true });

for (const slideNumber of [6, 8, 10]) {
  const spec = slides[slideNumber - 1];
  const starter = spec.starter_ref === "shared_program"
    ? shared
    : programs[spec.starter_ref];
  if (typeof starter !== "string") {
    throw new Error(`Unsupported starter_ref on slide ${slideNumber}: ${spec.starter_ref}`);
  }
  setText(slideNumber, "Title 1", spec.title);
  setChallengeText(slideNumber, "Content Placeholder 2", spec.body);
  const labelName = slideNumber === 10 ? "TextBox 4" : "TextBox 7";
  setText(slideNumber, labelName, "Starter Code:");
  setCode(slideNumber, "Rectangle 1", starter, 0, { fontSize: compactSharedFontSize, verticalAlignment: "top", autoFit: "shrinkText", compactLines: true });
}

setText(7, "Title 1", slides[6].title);
setCode(7, "Content Placeholder 2", programs.challenge1, 0, { fontSize: "20pt" });
setText(9, "Title 1", slides[8].title);
setCode(9, "Rectangle 2", programs.challenge2, 0, { fontSize: "20pt", leadingBlankLines: 3 });
setText(11, "Title 1", slides[10].title);
// The inherited solution-C title box is tall enough for one line, but its
// middle alignment leaves the ink too close to the first code line. Keep the
// same frame, font, and one-line geometry while using the existing top inset.
target(11, "Title 1").text.verticalAlignment = "top";
setCode(11, "Rectangle 2", programs.challenge3, 0, { fontSize: "20pt", leadingBlankLines: 3 });
setText(12, "Title 1", slides[11].title);
setDebug(12, "Content Placeholder 2", slides[11].body, programs.broken);
setText(13, "Title 1", slides[12].title);
setCode(13, "Content Placeholder 2", programs.fixed, 0, { fontSize: "18pt", leadingBlankLines: 2 });

// One canonical artwork must be used in title/non-title layouts and the
// worksheet.  Replace inherited bytes first, then relocate the faint master
// image into non-title layouts so the title slide cannot double-render it.
const canonicalBytes = new Uint8Array(await fs.readFile(path.join(root, curriculum.assets.master)));
const masterIds = new Set(presentation.masters.items.map((master) => master.id));
for (const master of presentation.masters.items) {
  for (const image of master.images.items) {
    const frame = image.frame;
    image.replace({ blob: canonicalBytes, contentType: "image/png", alt: `${curriculum.lesson.title} graphite pencil illustration`, fit: "contain" });
    image.frame = frame;
    image.crop = { left: 0, top: 0, right: 0, bottom: 0 };
    image.fit = "contain";
    image.lockAspectRatio = true;
  }
}
for (const layout of presentation.layouts.items) {
  if (masterIds.has(layout.id)) continue;
  for (const image of layout.images.items) {
    const frame = image.frame;
    image.replace({ blob: canonicalBytes, contentType: "image/png", alt: `${curriculum.lesson.title} graphite pencil illustration`, fit: "contain" });
    image.frame = frame;
    image.crop = { left: 0, top: 0, right: 0, bottom: 0 };
    image.fit = "contain";
    image.lockAspectRatio = true;
  }
}

const editedProto = presentation.toProto();
const protoMaster = editedProto.layouts.find((layout) => layout.id.startsWith("/ppt/slideMasters/"));
if (!protoMaster) throw new Error("one imported slide master is required");
const masterPictures = protoMaster.elements.filter((element) => element.type === 7);
let translucentPicture;
let masterFrame;
if (masterPictures.length === 1) {
  masterFrame = structuredClone(masterPictures[0].bbox);
  protoMaster.elements = protoMaster.elements.filter((element) => element.type !== 7);
} else if (masterPictures.length === 0) {
  const seededLayout = editedProto.layouts.find((layout) => layout.id !== protoMaster.id && layout.name !== "Title Slide" && layout.elements.some((element) => element.type === 7));
  if (!seededLayout) throw new Error("migrated template has no non-title illustration seed");
  masterFrame = structuredClone(seededLayout.elements.find((element) => element.type === 7).bbox);
} else {
  throw new Error(`expected zero or one master picture, found ${masterPictures.length}`);
}
const titleLayout = editedProto.layouts.find((layout) => layout.id !== protoMaster.id && layout.name === "Title Slide");
const titlePicture = titleLayout?.elements.find((element) => element.type === 7);
if (!titlePicture) throw new Error("migrated template has no title-layout illustration seed");
translucentPicture = structuredClone(titlePicture);

for (const layout of editedProto.layouts) {
  if (layout.id === protoMaster.id) continue;
  const pictures = layout.elements.filter((element) => element.type === 7);
  if (layout.name === "Title Slide") {
    if (pictures.length !== 1) throw new Error(`expected one title-layout picture, found ${pictures.length}`);
    continue;
  }
  layout.elements = layout.elements.filter((element) => element.type !== 7);
  const clone = structuredClone(translucentPicture);
  clone.bbox = structuredClone(masterFrame);
  clone.fill.pictureEffects = [{ type: 1, alphaModFix: 28000 }];
  const numericIds = layout.elements.map((element) => Number.parseInt(element.id, 10)).filter(Number.isFinite);
  clone.id = String(Math.max(20, ...numericIds) + 1);
  clone.creationId = `{00000000-0000-0000-0000-${String(layout.id).replace(/\D/g, "").padStart(12, "0").slice(-12)}}`;
  layout.elements.push(clone);
}
const sourceSlides = new Map(sourceProto.slides.map((slide) => [slide.id, slide]));
for (const slide of editedProto.slides) {
  const sourceSlide = sourceSlides.get(slide.id);
  if (!sourceSlide) continue;
  const sourceElements = new Map(sourceSlide.elements.map((element) => [element.id, element]));
  for (const element of slide.elements) {
    const sourceElement = sourceElements.get(element.id);
    if (sourceElement?.bbox) element.bbox = structuredClone(sourceElement.bbox);
  }
}

const EMU_PER_INCH = 914400;
const inchesToEmu = (inches) => Math.round(inches * EMU_PER_INCH);
const protoElement = (slideNumber, name, occurrence = 0) => {
  const matches = editedProto.slides[slideNumber - 1].elements.filter(
    (element) => element.name === name,
  );
  if (!matches[occurrence]) {
    throw new Error(
      `Missing proto element ${name} occurrence ${occurrence} on slide ${slideNumber}`,
    );
  }
  return matches[occurrence];
};

// Give the shared starter code enough horizontal room to avoid unnecessary
// wrapping on every challenge slide. Move the label with the code frame so the
// repeated top-right block retains one alignment edge.
for (const slideNumber of [6, 8, 10]) {
  const labelName = slideNumber === 10 ? "TextBox 4" : "TextBox 7";
  const label = protoElement(slideNumber, labelName);
  const code = protoElement(slideNumber, "Rectangle 1");
  label.bbox = {
    ...label.bbox,
    xEmu: inchesToEmu(6.55),
    widthEmu: inchesToEmu(2),
  };
  code.bbox = {
    ...code.bbox,
    xEmu: inchesToEmu(6.55),
    widthEmu: inchesToEmu(6.45),
    heightEmu: inchesToEmu(1.75),
  };
}

// The Investigate slide has two Rectangle 1 shapes: the questions first and
// the example code second. Lift only the example code so it begins directly
// below the inherited title while leaving the question area unchanged.
const investigateCode = protoElement(5, "Rectangle 1", 1);
investigateCode.bbox = {
  ...investigateCode.bbox,
  yEmu: inchesToEmu(1.4),
  heightEmu: inchesToEmu(1.8),
};

if (learnerOnly) {
  // Keep the established learner sequence while physically excluding all
  // four answer slides. The retained source indices are title, shared code,
  // retrieve, predict, investigate, three challenges, and debug.
  const keepSourceIndices = new Set([0, 1, 2, 3, 4, 5, 7, 9, 11]);
  editedProto.slides = editedProto.slides.filter((_slide, index) => keepSourceIndices.has(index));
}
const finalPresentation = Presentation.load(editedProto);
for (const [index, slide] of finalPresentation.slides.items.entries()) {
  const pageNumber = slide.shapes.items.find((shape) => shape.name?.startsWith("Slide Number Placeholder"));
  if (pageNumber) pageNumber.text = String(index + 1);
}

async function restoreHiddenSlides(pptxPath, slideNumbers) {
  const workDir = await fs.mkdtemp(path.join(path.dirname(pptxPath), ".hidden-slides-"));
  const slideFiles = slideNumbers.map((number) => `ppt/slides/slide${number}.xml`);
  try {
    await execFile("unzip", ["-qq", pptxPath, ...slideFiles, "-d", workDir]);
    for (const slideFile of slideFiles) {
      const filePath = path.join(workDir, slideFile);
      let xml = await fs.readFile(filePath, "utf8");
      if (/<p:sld\b[^>]*\bshow=/.test(xml)) {
        xml = xml.replace(/(<p:sld\b[^>]*\bshow=")[^"]*(")/, (_match, start, end) => `${start}0${end}`);
      } else {
        xml = xml.replace(/<p:sld\b/, '<p:sld show="0"');
      }
      await fs.writeFile(filePath, xml);
    }
    await execFile("zip", ["-q", pptxPath, ...slideFiles], { cwd: workDir });
  } finally {
    await fs.rm(workDir, { recursive: true, force: true });
  }
}

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(renderDir, { recursive: true });
const pptx = await PresentationFile.exportPptx(finalPresentation);
await pptx.save(outputPath);
await restoreHiddenSlides(outputPath, learnerOnly ? [2] : curriculum.contracts.presentation.hidden_slides);
for (const [index, slide] of finalPresentation.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  const preview = await finalPresentation.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(renderDir, `${stem}.png`), new Uint8Array(await preview.arrayBuffer()));
  await fs.writeFile(path.join(renderDir, `${stem}.layout.json`), await (await slide.export({ format: "layout" })).text());
}
const montage = await finalPresentation.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(path.join(renderDir, "deck-montage.webp"), new Uint8Array(await montage.arrayBuffer()));
