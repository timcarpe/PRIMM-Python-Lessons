// Fill a capstone deck from canonical capstone data.
// Usage: node capstones.mjs <capstone.json> <template.pptx> <output.pptx> <render-dir>
import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, Presentation, PresentationFile } from "@oai/artifact-tool";
import { buildCodeVocabulary, proseRuns } from "./inline_code_styling.mjs";

const [specPath, templatePath, outputPath, renderDir] = process.argv.slice(2);
const capstone = JSON.parse(await fs.readFile(specPath, "utf8"));
const presentation = await PresentationFile.importPptx(await FileBlob.load(templatePath));

const inspection = await presentation.inspect({ kind: "textbox,shape", include: "id,slide,name", maxChars: 1000000 });
const records = inspection.ndjson.split(/\r?\n/).filter(Boolean).map((line) => JSON.parse(line));
const find = (slide, name) => records.find((record) => record.slide === slide && record.name === name);
const target = (slide, name) => {
  const record = find(slide, name);
  if (!record) throw new Error(`Missing ${name} on slide ${slide}`);
  return presentation.resolve(record.id);
};

const paragraph = (runs, spaceAfter) => ({ runs, bulletCharacter: "", marginLeft: 0, indent: 0, spaceAfter });

target(1, "Title 1").text = capstone.title;
if (find(1, "Subtitle 2")) target(1, "Subtitle 2").text = "Capstone";

target(2, "Title 1").text = "How the finished program works";
target(2, "Rectangle 1").text.set(capstone.overview.map((line) => paragraph(
  [{ run: line, textStyle: { color: "#080808", typeface: "Calibri", fontSize: "24pt" } }], 12,
)));

for (const [index, challenge] of capstone.challenges.entries()) {
  const slide = index + 3;
  const vocabulary = buildCodeVocabulary([challenge.solution]);
  const style = { fontSize: "18pt", typeface: "Calibri" };
  const goal = proseRuns(challenge.goal, vocabulary, { ...style, bold: true });
  const steps = challenge.steps.map((step, stepIndex) => paragraph(proseRuns(`${stepIndex + 1}. ${step}`, vocabulary, style), 6));
  const save = paragraph(proseRuns(`Save as challenge${index + 1}.py.`, vocabulary, style), 0);
  target(slide, "Title 1").text = `Challenge ${index + 1}`;
  const body = target(slide, "Content Placeholder 2");
  body.text.set([paragraph(goal, 10), ...steps, save]);
  body.text.autoFit = "shrinkText";
}

const final = Presentation.load(presentation.toProto());
for (const [index, slide] of final.slides.items.entries()) {
  const number = slide.shapes.items.find((shape) => shape.name?.startsWith("Slide Number Placeholder"));
  if (number) number.text = String(index + 1);
}

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(renderDir, { recursive: true });
await (await PresentationFile.exportPptx(final)).save(outputPath);
for (const [index, slide] of final.slides.items.entries()) {
  const preview = await final.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(renderDir, `slide-${index + 1}.png`), new Uint8Array(await preview.arrayBuffer()));
}
