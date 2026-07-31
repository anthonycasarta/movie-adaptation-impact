# Repository Agent Guidance

## Purpose

This file defines persistent workflow rules for agents working in this repository, especially when following `todo.md`.

## Responsibilities

- The planning/review agent may inspect files, explain steps, identify ambiguity, and recommend changes.
- The planning/review agent must not check off checklist items.
- Only the build agent may check off items after completing or verifying the corresponding work.
- Proposed or planned work must never be marked complete.

## Simplicity And Delivery

- Prioritize a working vertical slice over speculative completeness.
- Implement only behavior required by the current step, current fixtures, and existing tests.
- Prefer direct functions and simple local state over abstractions, generic engines, or future-proofing.
- Do not add compatibility layers, configuration options, helpers, or public APIs for possible future requirements.
- Add private helpers only when they materially improve readability or remove real duplication.
- Harden behavior later when real data, observed failures, or explicit requirements demonstrate the need.
- Prefer one representative integration test when it adequately verifies the current contract.
- Add separate tests only for explicit requirements, reproduced bugs, or common failures that would block the basic workflow.
- Do not create exhaustive input matrices or tests for theoretical malformed data unless explicitly requested.
- Avoid duplicate tests and assertions that prove behavior already covered by another test.
- Keep checklists outcome-focused. Do not split trivial implementation details such as individual imports or assignments into separate checklist items.

## Step Reviews

When asked to review or explain a step, cover:

- the step's goal
- why it is needed
- affected files
- expected implementation
- verification criteria
- ambiguities or risks
- whether a change is required

When responding, distinguish between:

- Change required: the step is incomplete, ambiguous, contradictory, or points to the wrong file.
- No change required: the step is being explained or confirmed as written.
- A step is not incomplete solely because it lacks exhaustive edge-case tests, generalized abstractions, or future-proofing.
- Recommend additional tests only when they protect an explicit requirement, a reproduced bug, or the basic end-to-end workflow.

## Checklist Updates

The build agent must:

- check off each substep only after it is completed
- leave blocked or unverified substeps unchecked
- when a step has a linked detailed checklist file, update that file's substeps rather than duplicating them in `todo.md`
- check off the parent step in `todo.md` only when every substep in the linked step file is checked
- immediately check off the parent step after its final linked substep is completed and verified
- leave the parent unchecked if any linked substep remains incomplete
- update checklist state during the same task that completes the work
- never finish a build task without updating the authoritative checklist file in the same response cycle
- before sending the final response, reread the applicable `todo.md` section and linked step file and confirm that their checkbox states match the completed work
- if any substep remains incomplete or unverified, leave it and its parent unchecked and report the exact reason
- never mark a task complete based only on intent or partial implementation

## Implementation

- Follow the file paths specified in `todo.md`.
- Inspect existing files before editing.
- Avoid introducing unrelated dependencies or refactors.
- Make the smallest correct change.
- Preserve existing behavior outside the current step.
- Avoid implementing later steps early unless required by the current step.
- Report unexpected conflicts rather than silently changing scope.
- Never remove, overwrite, or revert unrelated user changes.
- Continue when unrelated changes do not conflict with the task. Stop and ask the user only when existing changes directly conflict with the required implementation.
- Try to resolve ambiguity by inspecting existing code, tests, and documentation first. Ask one concise question only when different interpretations would materially change the result.
- Do not silently choose between conflicting requirements.
- Do not modify files outside the current step unless the step, its verification, or a necessary dependency explicitly requires it.
- Do not manually edit generated files unless the current step explicitly requires it.
- Prefer the simplest implementation that makes the current workflow functional.
- Do not build generalized infrastructure when a direct implementation satisfies the current requirement.

## Tool Safety

- Do not run destructive commands unless the user explicitly requests and approves them.
- Do not use `git reset --hard`, forced checkouts, broad file deletion, or force-pushing without explicit approval.
- Prefer non-interactive commands and avoid prompts that cannot be handled reliably.
- Use commands whose output clearly shows what ran and whether it succeeded.
- Do not bypass tests, hooks, or validation to make a command pass.
- Never expose, commit, or include credentials, tokens, private keys, or `.env` contents in output or source files.

## Verification

- Run the narrowest relevant tests first.
- Complete any verification command required by the substep.
- Report commands and results.
- Leave verification items unchecked if tools or dependencies prevent execution.
- Check verification items only after successful execution.
- Avoid live network requests unless the current step explicitly requires them.
- If verification cannot run, report the exact missing dependency, tool, or other blocker.
- Attempt a safe, in-scope resolution when possible.
- Do not substitute manual inspection for a required automated test without reporting that limitation.
- Use the smallest representative test set that verifies the current behavior.
- Do not expand verification into exhaustive edge-case coverage unless explicitly required.
- A focused integration test may replace multiple granular unit tests when it verifies the same contract clearly.

## Scope

Do not implement the following unless the user explicitly changes scope:

- Open Library
- TMDb
- NYT
- dataset merging
- notebooks
- analysis
- modeling
