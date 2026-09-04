---
name: git-commit
description: >-
  Analyze current Git changes and create one or more logically atomic commits
  using Conventional Commits, with each commit representing one coherent change.
  Use when the user asks to commit changes, split changes into commits, write
  commit messages, or create a clean commit history.
---

# Git Commit

Create one or more clean, logically atomic Git commits from the current working tree.
Use Conventional Commits and preserve changes outside the user's requested scope.

## Workflow

1. Inspect the repository before staging: run `git status --short`, review both
   `git diff` and `git diff --cached`, and inspect untracked files within scope.
   Read recent commit history when useful for existing conventions.
2. Understand the changes and identify which ones the user asked to commit.
3. Partition those changes into logical commits:

   - Each commit should represent one coherent change. Separate unrelated
     features, fixes, refactors, documentation, tests, configuration, and cleanup
     when practical.
   - Keep implementation and its tests or supporting documentation together
     when they form one coherent change. Do not split mechanically by file.
   - If there is only one logical change, create one commit; do not split it
     merely to make the history look granular.

4. Run relevant, reasonably scoped checks. If checks are skipped, say why.
5. For each logical commit:

   - Stage only its files or hunks. When one file contains different logical
     changes, use patch/hunk staging when practical.
   - Inspect `git diff --cached` and verify that no unrelated changes are
     staged before committing, including changes staged before this workflow.
   - Generate the commit message from the staged diff only, then create the
     commit.

6. Repeat until all requested changes are committed. Leave unrelated
   pre-existing changes untouched.
7. Check the final repository state and report each commit's hash, message,
   files included, checks run, and any remaining uncommitted changes.

## Commit Messages

Use Conventional Commits, following the repository's established type and scope
conventions:

```text
<type>(<scope>): <description>
```

Use common types such as `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`, `perf`, `style`, or `revert`.

- Use imperative, lowercase descriptions without a trailing period.
- Infer the scope from the actual change and include it when it clarifies the
  affected area, for example `docs(agents): add project guidance`.
- Describe the staged change, not the task title or branch name. Avoid vague
  summaries such as "update files" or "misc changes".
- Do not mention AI, Codex, prompts, or the conversation in commit messages.
- Add a body only when it helps explain motivation, tradeoffs, or validation.
- For breaking changes, include `!` after the type or scope and add a `BREAKING CHANGE:` footer.

## Safety

- Never use destructive git commands unless the user explicitly requested them.
- Never revert, discard, or rewrite user changes to make a commit easier, or
  use destructive reset/checkout commands to separate commits.
- Never amend, rebase, squash, or rewrite existing commits unless explicitly
  requested.
- Never push unless explicitly requested.
- If the worktree contains changes that cannot be safely separated, ask before committing.
