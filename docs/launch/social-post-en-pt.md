# Launch post — English + Português

I’m sharing Axiom SDD: a repository-based template and workflow for teams building software with AI coding agents.

The idea is straightforward: agree on expected behavior, split the work into bounded tasks, and keep evidence beside the code.

Axiom connects specifications, plans, task ownership, tests and review through a shared project contract. Its Python CLI installs the framework and generates entry points for selected coding tools.

The 2.1.0 changes focus on a problem we encountered while building Club S: repeated status updates can look like progress even when the evidence has not changed.

The new local metrics report checks evidence-file hashes, keeps unchanged proof from becoming “fresh” after another status update, and distinguishes simulated checks from required real-flow validation. The updater also preserves customized project profiles.

13 regression tests passed. A local rollout preserved 68 project-owned files checked by hash. We have not measured productivity or token savings, and this report does not certify a release.

The screenshots show Club S in development and its local Keycloak sign-in page. They illustrate the project behind the lessons; they do not claim a completed production login.

🇧🇷 Em português: o Axiom SDD transforma intenção em especificações, tarefas e evidências revisáveis. Várias IAs podem compartilhar o mesmo contrato de trabalho, com responsáveis e próximos passos claros. Teste simulado continua sendo teste simulado; entrega precisa de comprovação.

If you work with multiple coding agents, I’d like to hear how you track ownership, blockers and acceptance evidence.

Repository: https://github.com/alexandrehenrique-dev/axiom-sdd
Article: https://github.com/alexandrehenrique-dev/axiom-sdd/blob/main/docs/articles/axiom-sdd-from-intent-to-evidence.md

#SpecDrivenDevelopment #SoftwareEngineering #AICoding #DeveloperTools

---

Publication note (remove before posting): merge the documentation PR before using the main-branch article link. This draft announces the work, not a claim that the PR has already merged. Suggested carousel: portal → entry prototype → Keycloak sign-in → cave. Use the exact captions in ../images/README.md; historical labels in the portal are not current event dates or offers.
