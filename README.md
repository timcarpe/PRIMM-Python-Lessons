# Python Programming Lessons

This is a three-year sequence of introductory Python lessons for Grades 6–8.
The lessons teach programming through short, readable examples that pupils
predict, run, investigate, modify, and eventually use to make a new program.

The sequence is based on PRIMM: **Predict, Run, Investigate, Modify, Make**.
The approach is described by Sue Sentance and Jane Waite in
[“PRIMM: Exploring pedagogical approaches for teaching text-based programming
in school”](https://doi.org/10.1145/3137065.3137084).

## Where the lessons are

The repository contains one current set of lessons in two root folders:

- `Mapped Curriculum Lessons` contains the files used directly with pupils.
- `Mapped Curriculum Lesson - Supplemental Material` contains teacher and
  planning resources.

Lessons are grouped by grade and numbered as one continuous curriculum. Lesson
numbers 11, 27, and 36 are reserved for capstone work and are not included in
this non-capstone collection.

## Reviewing examples and challenges

Generate the self-contained browser review page from the same effective
manifests used by the compiler:

```bash
.venv/bin/lesson-compiler review-tool
```

Open `lesson-manifest-review.html`, flag individual example or challenge issues,
and export the issue report. The report contains identified issues only and
includes exact manifest paths, fields, original values, flags, and written
feedback for agent ingestion.

The page can also export a change-proposal template. After an agent fills its
`new_value` fields, import that JSON to compare each proposed value beside the
current effective manifest. Full revised lesson record JSON files can also be
imported. Record approval decisions in the page and export the resulting
approval report. Review progress is stored only in the browser's local storage;
the source manifests are never edited by the page.

Before drafting challenge changes, follow the
[challenge review workflow](docs/challenge-review-workflow.md). It includes the
required grounding step using relevant positive examples from the Python Review
PDFs, technical cross-checking against starter and solution code, and proposal
approval before canonical edits.

## Resources in each lesson

Every lesson has the same predictable set of resources.

| Resource | Audience | Purpose |
| --- | --- | --- |
| Slides | Whole class | Introduce the example, guide PRIMM discussion, present three challenges, and finish with debugging. |
| Starter Code | Pupils | The complete example program used for prediction, running, investigation, and modification. |
| Challenges PDF | Pupils | A printable one-page copy of the example and the three programming challenges. |
| Worksheet | Pupils and teachers | Records predictions, observations, investigation answers, challenge work, debugging, testing, and reflection. |
| Concept Sheet | Pupils and teachers | Summarises the lesson’s vocabulary, syntax, and small code examples. |
| Solutions | Teachers | Includes solutions for all three challenges, the broken debugging program, and its corrected version. |

Learner slide decks do not contain solution slides. Solutions are kept in the
supplemental lesson folder so that the same slides can be presented directly to
a class.

## How to teach a lesson with PRIMM

### 1. Predict

Show the example code without running it. Ask pupils to explain what they think
will happen and to identify any values they can already trace. A useful
prediction is specific: it names an expected value, route, repetition, or line
of output.

### 2. Run

Run the unchanged starter program. Compare its actual behaviour with the class
prediction. Treat an incorrect prediction as useful evidence about how pupils
currently understand the code.

### 3. Investigate

Use the investigation questions to read the program closely. Pupils should
trace variables, conditions, loop behaviour, indexes, inputs, and outputs from
the code in front of them. Ask them to justify answers with a particular line
or value rather than guessing from the program’s topic.

### 4. Modify

Move through Challenges 1 and 2. Challenge 1 makes a small, meaningful change
to the example’s main concept. Challenge 2 extends that change or combines it
with another familiar idea. Pupils should save each completed challenge as a
new file and test it before continuing.

### 5. Make

Challenge 3 asks pupils to create a related program with less scaffolding. The
example remains available as a pattern, but pupils must decide how to adapt its
structure. Finish with the debugging task so pupils also practise explaining,
testing, and correcting code.

## Suggested classroom routine

1. Share the lesson goal and briefly retrieve the prerequisite knowledge.
2. Open the starter code, but do not run it during prediction.
3. Collect several predictions and ask pupils to explain their reasoning.
4. Run the code with the suggested inputs and compare results.
5. Work through the investigation questions before permitting edits.
6. Model only the first change needed for Challenge 1 when support is required.
7. Have pupils save and test each challenge separately.
8. Use the fix-the-code task as a final check of understanding.
9. Review a small selection of solutions, focusing on reasoning and tests rather
   than one “perfect” program.

The concept sheet can be given before the lesson as vocabulary support, during
the Modify stage as a reference, or after the lesson for revision. The full
worksheet is useful when written evidence is needed; the challenge PDF supports
a lighter practical lesson.

## Challenge scaffolding

The three challenges deliberately increase independence:

- **Challenge 1:** change the example while keeping its recognisable structure.
- **Challenge 2:** extend the program with another input, calculation, route,
  repetition, or data change.
- **Challenge 3:** make a new but closely related program using the same core
  concept.

Instructions use short sentences and direct verbs such as *ask*, *store*,
*change*, *display*, and *test*. Bracketed names such as `[total]` identify
variables. Quoted text identifies exact output. Where a test value is supplied,
pupils should be able to observe whether their program meets the requirement.

## Curriculum sequence

### Grade 6: foundations and control flow

| Lesson | Focus |
| --- | --- |
| 01 — Hello Python! | Input, output, variables, and strings |
| 02 — Operators and Integers | Whole-number input, `int()`, variables, and arithmetic |
| 03 — Decimal Numbers | Decimal input, `float()`, and arithmetic |
| 04 — Decisions | `if`/`else`, Boolean conditions, and indentation |
| 05 — More Decisions | Ordered `if`/`elif`/`else` choices |
| 06 — Logical Choices | Combining conditions with `and` and `or` |
| 07 — Nested Decisions | A decision inside another decision |
| 08 — Counted Loops | Repetition with `for` and `range()` |
| 09 — Condition Loops | Repetition with `while`, conditions, and counters |
| 10 — Choosing Loop Structures | Selecting and combining appropriate loop structures |

### Grade 7: text, randomness, menus, and lists

| Lesson | Focus |
| --- | --- |
| 12 — Strings and Text | Cleaning and formatting text with string methods |
| 13 — String Positions | Reading characters and substrings with indexes and slices |
| 14 — Changing Text Case | Normalising text with upper- and lower-case methods |
| 15 — Joining Text | Building new strings by concatenation |
| 16 — Text Length and Lines | Measuring strings and arranging output across lines |
| 17 — Lists | Creating, displaying, and appending to ordered collections |
| 18 — Random Whole Numbers | Generating bounded random integers |
| 19 — Random Steps and Choices | Random stepped values and choices from a list |
| 20 — Reliable Menus | Repeating and validating a menu with a Boolean flag |
| 21 — Character Codes | Converting between characters and numeric codes |
| 22 — List Positions and Updates | Reading and replacing items by position |
| 23 — Inserting and Removing List Items | Changing list membership by value and position |
| 24 — Deleting by List Position | Removing an item when its position is known |
| 25 — Working Through Lists | Visiting each item with a loop and counting with `len()` |
| 26 — Building Lists with Loops | Collecting repeated input into a list |

### Grade 8: two-dimensional data and functions

| Lesson | Focus |
| --- | --- |
| 28 — Reading 2D Lists | Representing records as rows and reading rows or cells |
| 29 — Updating 2D List Cells | Replacing one field in a selected row |
| 30 — Changing 2D List Rows | Appending, inserting, and deleting complete records |
| 31 — Searching 2D Lists | Finding a record and handling a not-found result |
| 32 — Functions | Defining and calling a reusable procedure |
| 33 — Functions with Results | Passing parameters and returning a result |
| 34 — Several Functions | Dividing a program into separate responsibilities |
| 35 — Functions with 2D Data | Passing record data into display and search functions |

## Assessment and support

Prediction and investigation answers reveal misconceptions before pupils begin
editing. Challenge programs provide evidence that pupils can apply the concept.
The Make task shows whether they can transfer it to a related problem.

For additional support, keep the starter code visible, trace one worked input,
and provide the concept sheet. For greater challenge, ask pupils to select their
own test cases, explain why those cases are useful, or compare two correct
solutions. Avoid introducing untaught syntax merely to make a solution shorter;
the sequence is designed to build complexity gradually.
