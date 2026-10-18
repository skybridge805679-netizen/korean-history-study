// node tools/check_question_core_notes.js
// Tests coverage, factual-source mapping, picture labels, task types and time axes.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const site = path.join(__dirname, "..", "site");
const html = fs.readFileSync(path.join(site, "index.html"), "utf8");
const questions = JSON.parse(html.match(/^const QS=(.*);$/m)[1]);
const context = { window: {} };
vm.createContext(context);
for (const filename of ["question-explanations.js", "question-figures.js", "question-core-notes.js", "question-note-timelines.js"]) {
  assert(html.includes(`src="${filename}?`), `Missing script: ${filename}`);
  vm.runInContext(fs.readFileSync(path.join(site, filename), "utf8"), context);
}
const w = context.window;
const notes = w.buildQuestionCoreNotes(questions, w.QUESTION_EXPLANATIONS, w.QUESTION_FIGURES, w.QUESTION_NOTE_TIMELINES);
assert.equal(Object.keys(notes).length, 550);
let connections = 0, photos = 0;
const chronological = new Set(["order", "interval", "timeline", "relative", "period"]);
for (const q of questions) {
  const id = `${q.r}-${q.n}`, note = notes[id], source = w.QUESTION_EXPLANATIONS[id];
  assert(note, id);
  assert.equal(note.id, id);
  assert.equal(note.round, q.r);
  assert.equal(note.era, q.era);
  assert.equal(note.connections.length, 5, id);
  assert.equal(JSON.stringify(note.anchors), JSON.stringify(source.clues), id);
  assert.equal(note.connections.filter(c => c.selected).length, 1, id);
  assert.equal(note.connections.find(c => c.selected).number, q.a, id);
  for (const c of note.connections) {
    const i = c.number - 1;
    assert.equal(c.detail, source.choices[i], `${id} choice ${c.number}: stale source`);
    assert(c.fact.length && c.detail.startsWith(c.fact), `${id}: summary drops/reorders source text`);
    assert.equal(c.cue, w.QUESTION_FIGURES[id]?.choices?.[i]?.name || q.ch[i]);
    connections++;
  }
  if (w.QUESTION_FIGURES[id]?.choices) photos++;
  if (chronological.has(note.type)) assert(note.timeline.length >= 2, `${id}: missing time axis`);
}
for (const [id, rows] of Object.entries(w.QUESTION_NOTE_TIMELINES)) {
  assert(notes[id], `Unknown timeline question: ${id}`);
  assert(rows.length >= 2);
  for (const row of rows) assert(row.length === 2 && row.every(s => typeof s === "string" && s.trim()), id);
}
assert.equal(notes["78-43"].type, "exception");
assert.equal(notes["78-2"].type, "order");
assert.equal(notes["79-6"].type, "picture");
assert.equal(notes["79-14"].timeline[1][0], "1135~1136");
assert.equal(notes["73-6"].connections[2].descriptive, true);
assert.equal(notes["76-27"].connections[1].descriptive, true);

// A decimal date must not be split as a sentence boundary.
const sample = JSON.parse(JSON.stringify(w.QUESTION_EXPLANATIONS["79-31"]));
sample.choices[0] = "1896.1에 시행되었다. 두 번째 문장이다. 세 번째 문장이다.";
const compact = w.buildQuestionCoreNotes([questions.find(q => q.r === 79 && q.n === 31)], { "79-31": sample });
assert.equal(compact["79-31"].connections[0].fact, "1896.1에 시행되었다. 두 번째 문장이다.");
console.log(`문항별 핵심노트 ${Object.keys(notes).length}개 · 보기 연결 ${connections}개 · 사진 ${photos}문항 · 시간축 ${Object.keys(w.QUESTION_NOTE_TIMELINES).length}개: 통과`);
