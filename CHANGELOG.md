# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Added

- Added a self-contained manifest review page with issue-only agent reports and
  side-by-side proposal approval.

### Changed

- Allowed worksheets to render to either three or four pages and retained all
  middle challenge pages in the learner challenge PDF.
- Applied the approved follow-up challenge wording across Lessons 4, 7, 9, 10,
  12, 17, 22, 23, 25, 26, 28–31, 34, and 35, including aligned solution
  outputs and cumulative Lesson 4 starter code.
- Added suite-wide regression coverage for programming-item colour roles in
  revised challenge prose across Word and PowerPoint compilation paths.
- Rewrote 51 approved challenge prompts for direct programming language,
  suggested variables, concrete tests, and observable outputs.
- Preserved canonical challenge prose while applying semantic code colours.
- Promoted the current learner and supplemental lesson trees to the repository root.
- Consolidated compiler code, curriculum data, assets, and templates under `src`.
- Made the two root lesson folders the compiler's default output.
- Added one clear build-and-verify command for maintainers and agents.
- Replaced the build-focused README with a teacher-facing PRIMM guide and curriculum map.

### Removed

- Removed superseded dated builds and duplicate lesson suites.
- Removed obsolete compiler entry points and unused document-generation code.
