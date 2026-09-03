# Examples

Tutorials and ready-to-paste prompts. **This folder belongs to the template** — it is never
installed into consumer projects (the installer excludes it by design; see
[INSTALL.md](../sdd/bootstrap/INSTALL.md)). If you copied it by accident, delete it or add
`examples/` to your `.gitignore`.

| Folder | What |
|---|---|
| [prompts/](./prompts/README.md) | Small, ready prompts for every step — behavior lives in the framework, not here |
| [agents/](./agents/) | One worked example per catalog agent: scenario, input, prompt, expected behavior/output, common errors, token tips |
| [scenarios/](./scenarios/) | End-to-end walkthroughs per context (greenfield, legacy, bugfix, migration, …). Start with the 3 full tutorials: [jira-to-feature](./scenarios/jira-to-feature.md), [legacy-refactor](./scenarios/legacy-refactor.md), [greenfield](./scenarios/greenfield.md) |
