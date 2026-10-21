# claude-skills

Shared [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) for development projects. Each folder is one skill: a `SKILL.md` that tells Claude when and how to use it, plus any reference files or scripts it loads on demand.

Code repos don't copy these files. They include this repo as a git submodule, so every project uses the same reviewed version of each skill.

## Skills

| Skill | What it does |
|---|---|
| [`wcag-22-aa`](wcag-22-aa/SKILL.md) | Builds and reviews UI to WCAG 2.2 Level AA on web and native mobile: component patterns, ARIA, tables, design tokens, testing, and a contrast-check script. |

## Using these skills in a code repo

Add the submodule once:

```bash
git submodule add -b main https://github.com/sgupta0824/claude-skills .claude/skills
git commit -m "chore: add claude-skills as submodule"
```

Clone with submodules, and keep them in step on every pull:

```bash
git clone --recurse-submodules <repo-url>
git config submodule.recurse true
```

For cloud sessions, add a SessionStart hook to the repo's `.claude/settings.json` so the submodule is checked out when a session starts:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "git submodule update --init --recursive" }] }
    ]
  }
}
```

The code repo pins a specific commit of this repo. A new skill version reaches a project only when that project bumps the pointer.

## Changing a skill

All changes go through a pull request here. Never commit skill edits inside a code repo unless it is very specific to that repo.

1. From the code repo, branch inside the submodule:
```bash
   cd .claude/skills
   git fetch origin
   git checkout -b skill/<short-name> origin/main
```
2. Edit, commit, push the branch, and open a PR against `main`.
3. After the PR is merged, bump the pointer in each code repo that should get the change:
```bash
   git submodule update --remote .claude/skills
   git commit -am "chore: bump claude-skills"
```
   Then open a PR in that repo as usual.

## Adding a new skill

Create a folder named after the skill (lowercase, hyphens) with a `SKILL.md` at its root:

```markdown
---
name: my-skill
description: One sentence on what it does and when Claude should use it.
---

Instructions...
```

The `description` decides when Claude picks the skill up, so name the tasks and keywords that should trigger it. Keep `SKILL.md` lean, and put long material in a `references/` folder for Claude to open only when needed. Add the new skill to the table above in the same PR.
