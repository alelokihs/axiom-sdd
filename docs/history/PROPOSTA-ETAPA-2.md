# Proposta — Etapa 2: Camada Multiplataforma do template-sdd

> Status: **PROPOSTA PARA APROVAÇÃO** · Data: 2026-08-28
> Baseada em varredura das documentações oficiais (Copilot VS Code/JetBrains, Claude Code, OpenAI Codex, Devin) e na análise do template atual.

---

## 1. Resumo executivo

A boa notícia da pesquisa: **o problema que você quer resolver já tem uma "espinha dorsal" padronizada pelo mercado — o `AGENTS.md` na raiz do repositório.** Em 2026 ele é lido nativamente por:

| Ferramenta | Lê `AGENTS.md`? | Desde / como |
|---|---|---|
| OpenAI Codex (CLI e cloud) | ✅ nativo | é o arquivo canônico dele (global `~/.codex/AGENTS.md` → raiz → aninhados; cap de 32 KiB por padrão) |
| Devin | ✅ nativo | procura o arquivo antes de começar a codar |
| Copilot no VS Code | ✅ nativo | setting `chat.useAgentsMdFile`; aninhados via `chat.useNestedAgentsMdFiles` |
| Copilot no JetBrains/IntelliJ | ✅ nativo | release de mar/2026 do plugin (suporta também `CLAUDE.md` e nested) |
| Claude Code | ⚠️ via import | lê `CLAUDE.md`; a doc oficial recomenda um `CLAUDE.md` de 1 linha: `@AGENTS.md` |

Ou seja: a estratégia deixa de ser "um adapter gordo por ferramenta" e passa a ser **um arquivo canônico (`AGENTS.md`) + shims finos por ferramenta**, gerados e mantidos por script determinístico. Isso reduz a matriz de manutenção e cobre automaticamente ferramentas futuras que adotarem o padrão (Cursor, Gemini CLI, Copilot CLI etc. já leem).

Os seus 4 requisitos são todos viáveis, com **uma limitação estrutural importante** (item 3.4): arquivos escondidos via `.git/info/exclude` **não chegam a agentes cloud** (Devin, Codex cloud, Copilot coding agent), porque eles clonam do remoto. A proposta trata isso com dois modos de operação.

---

## 2. O que a documentação diz hoje (matriz de mecanismos)

### 2.1 Arquivos de instrução carregados automaticamente

| Ferramenta | Projeto (versionável) | Escopo por caminho | Global (máquina do dev) |
|---|---|---|---|
| **Copilot VS Code** | `.github/copilot-instructions.md` · `AGENTS.md` · `CLAUDE.md` | `.github/instructions/*.instructions.md` com frontmatter `applyTo: <glob>` | `~/.copilot/instructions/` + instruções de perfil do usuário (Settings Sync) |
| **Copilot IntelliJ** | `.github/copilot-instructions.md` · `AGENTS.md` · `CLAUDE.md` (plugin ≥ mar/2026) | file-based instructions (Settings > GitHub Copilot > Customizations) | `%LOCALAPPDATA%\github-copilot\intellij\global-copilot-instructions.md` |
| **Claude Code** | `CLAUDE.md` / `.claude/CLAUDE.md` · `CLAUDE.local.md` (pessoal) | `.claude/rules/*.md` com frontmatter `paths:` | `~/.claude/CLAUDE.md` · `~/.claude/rules/` · policy corporativa (`C:\Program Files\ClaudeCode\CLAUDE.md`) |
| **Codex** | `AGENTS.md` (raiz + aninhados, "mais próximo vence") | `AGENTS.md` aninhado por diretório | `~/.codex/AGENTS.md` · `~/.codex/config.toml` (inclui `project_doc_fallback_filenames`!) |
| **Devin** | `AGENTS.md` | — | Knowledge + Playbooks (org, via app — não são arquivos no repo) |

### 2.2 Comandos reutilizáveis ("ready prompts")

| Ferramenta | Mecanismo | Suporta input interativo? |
|---|---|---|
| Copilot VS Code | `.github/prompts/*.prompt.md` → viram slash commands | ✅ `${input:var}`, `${input:var:placeholder}`, tool `vscode/askQuestion` |
| Copilot IntelliJ | **não há prompt files de repo ainda** (só discussão aberta na comunidade) | fallback: vocabulário `SDD: ...` descrito no `AGENTS.md` |
| Claude Code | `.claude/commands/*.md` (com `$ARGUMENTS`) e skills | ✅ o agente pergunta no chat |
| Codex | `~/.codex/prompts/` **(deprecado — a doc manda usar skills)** · skills em `.codex/skills/` (projeto) e `~/.codex/skills/` | ✅ placeholders `$1..$9`, `$NOME` |
| Devin | Playbooks (colar/registrar no app) | ✅ sessão interativa |

### 2.3 Convergência emergente: skills (`SKILL.md`)

Claude Code (`.claude/skills/`), Codex (`.codex/skills/`), Cursor, Gemini CLI e outros já leem o mesmo formato `SKILL.md` sem modificação. Ainda não é universal (Copilot JetBrains não), mas é a aposta certa como **segunda camada** dos comandos SDD: um `sdd/skills/` canônico, symlinkado/copiado pelos shims.

---

## 3. Análise dos seus 4 requisitos

### 3.1 "Analisar todas as ferramentas instaladas" — ✅ VIÁVEL

Proposta: um novo comando **`sdd doctor`** (script Python stdlib, mesmo espírito do `install.py`) que varre a máquina e reporta, com os rótulos `CONFIRMED`/`INFERRED`/`UNKNOWN` que o framework já usa:

- **VS Code**: `%APPDATA%\Code\User\settings.json` (settings `chat.useAgentsMdFile` etc.), `%USERPROFILE%\.vscode\extensions\github.copilot-*` (versão do plugin);
- **JetBrains**: `%APPDATA%\JetBrains\<IDE><versão>\` (IDEs instaladas), `%LOCALAPPDATA%\github-copilot\intellij\` (instruções globais, versão do plugin via `plugins/github-copilot-intellij`);
- **Claude Code**: `%USERPROFILE%\.claude\` (CLAUDE.md global, settings.json, skills) + `claude --version`;
- **Codex**: `%USERPROFILE%\.codex\` (AGENTS.md global, config.toml, skills/prompts) + `codex --version`;
- **Devin**: não tem pegada local — reportado como "cloud runtime: configurar via AGENTS.md no repo + Knowledge/Playbooks no app";
- **Git**: presença de `.git/`, estado do `info/exclude`, hooks.

Saída: um relatório `SDD DOCTOR` + um `environment.yaml` que o bootstrap consome para decidir **quais shims gerar** (em vez do usuário declarar `Runtime:` na mão — a linha vira opcional, sobrescrevendo a detecção).

**Limitações honestas:**
- Detecção cobre *instalação*, não *login/licença* (não dá para saber se o Copilot do IntelliJ está autenticado sem abrir a IDE).
- Versão do plugin importa: `AGENTS.md` no JetBrains exige o plugin ≥ mar/2026. Seu `1.5.66-243` precisa ser verificado pelo doctor — se for anterior, o shim `.github/copilot-instructions.md` (suportado há muito mais tempo) cobre o gap. É exatamente por isso que o doctor reporta versão + mecanismo suportado, e o gerador escolhe o shim compatível.
- Escrever em arquivos **globais** (ex.: `global-copilot-instructions.md` do IntelliJ) afeta *todos* os projetos do dev — em ambiente corporativo isso é arriscado. Proposta: o doctor **reporta** os globais e só escreve neles com flag explícita `--write-global`, e o conteúdo global é minimalista (3 linhas: "se o repo tiver `sdd/sdd.yaml`, leia `AGENTS.md`/`sdd/` antes de agir").

### 3.2 "Triggers no Initialize SDD (perguntar onde ler/gerar)" — ✅ VIÁVEL

Hoje o `BOOTSTRAP.md` é "no human in the loop". Proposta: **modo interativo opcional**, sem quebrar o modo autônomo:

1. Nova fase `0.5 — Confirm inputs (interactive)` no BOOTSTRAP.md: se o prompt contiver `Interactive: yes` (ou se faltarem `Framework:`/`Source:`), o agente pergunta — em qualquer runtime, já que todos suportam diálogo: *(a)* de onde ler o template (path local, URL git, ou "já está vendored em `vendor/sdd`"); *(b)* onde instalar (raiz do projeto vs. subdiretório); *(c)* quais runtimes gerar (default: o que o `sdd doctor` detectou); *(d)* modo git (ver 3.4).
2. **Por ferramenta, o trigger vira artefato nativo**: no VS Code, `.github/prompts/sdd-init.prompt.md` usando `${input:templatePath:Caminho ou URL do template-sdd}` e `${input:source}` — a IDE literalmente abre campos de input; no Claude Code, `.claude/commands/sdd-init.md` com `$ARGUMENTS` + instrução de perguntar o que faltar; no Codex, skill `sdd-init`; no IntelliJ, o vocabulário `SDD: init` descrito no AGENTS.md (o plugin não tem prompt files — o agente pergunta no chat mesmo); no Devin, playbook "SDD init" cujo campo *What's needed* força as perguntas.

### 3.3 "Reconhecimento automático do `sdd/` em absolutamente todas as IDEs" — ⚠️ VIÁVEL COM NUANCE

"Absolutamente todas" não é tecnicamente garantível (cada ferramenta decide o que carrega). O que é garantível — e suficiente na prática — é uma **estratégia em 3 camadas**:

1. **Camada padrão (cobre a maioria e o futuro):** `AGENTS.md` canônico na raiz, gerado pelo bootstrap (o generator já existe no template). Quem lê AGENTS.md — Codex, Devin, Copilot VS Code, Copilot JetBrains, Cursor, Gemini CLI, Copilot CLI… — reconhece o `sdd/` sem nenhum arquivo extra.
2. **Camada de shims (ferramentas com arquivo próprio):** gerados por script a partir de um **registry declarativo** (`sdd/adapters/registry.yaml`): cada entrada mapeia *ferramenta → sinais de detecção → arquivos a gerar → template do shim*. Shims atuais: `CLAUDE.md` = `@AGENTS.md` + locks; `.github/copilot-instructions.md` = ponteiro de ~10 linhas (cobre também Visual Studio e Xcode de graça, e IntelliJ com plugin antigo); prompt files VS Code; commands/skills Claude; skills Codex. **Adicionar uma IDE nova = adicionar uma entrada no registry**, não escrever código.
3. **Camada global (opt-in):** os ponteiros globais do item 3.1 (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `global-copilot-instructions.md`) com as 3 linhas "detecte `sdd/`". Isso dá reconhecimento até em projetos onde o bootstrap ainda não rodou — útil no seu cenário corporativo, mas sempre com consentimento explícito.

Boas práticas que a doc impõe aqui: o Codex trunca a cadeia de AGENTS.md em **32 KiB** — o AGENTS.md canônico tem que continuar sendo ponteiro enxuto (o template já prega isso: "point, don't paste"); `AGENTS.md` aninhado em diretórios de risco (`migrations/`) funciona em Codex, VS Code e JetBrains (nested habilitado) — vale gerar quando o profile for `database-change` etc.

### 3.4 "git exclude automático, sem tocar no .gitignore" — ✅ VIÁVEL (com um limite físico)

Mecanismo correto: **`.git/info/exclude`** — funciona como o `.gitignore`, mas é local ao clone e nunca é commitado. Proposta:

- O `install.py`/bootstrap passa a manter um **bloco gerenciado** idempotente:

  ```
  # >>> sdd-managed (não edite; gerado pelo template-sdd) >>>
  /sdd/
  /AGENTS.md
  /CLAUDE.md
  /CLAUDE.local.md
  /.claude/
  /.codex/
  /.github/prompts/sdd-*.prompt.md
  /.github/instructions/sdd-*.instructions.md
  /.github/copilot-instructions.md   # só se foi o SDD que gerou
  # <<< sdd-managed <<<
  ```

  Idempotente (re-rodar substitui o bloco, não duplica), reversível (`--remove`), e **ciente de arquivos já rastreados**: se `.github/copilot-instructions.md` já existia commitado no repo, o exclude não tem efeito sobre ele — o script detecta (`git ls-files`) e avisa em vez de silenciosamente falhar.

- **Limite físico que precisa ficar explícito na doc:** `info/exclude` é por clone. Consequências: *(a)* cada dev da equipe precisa rodar o init (aceitável — o bootstrap é 1 prompt); *(b)* **agentes cloud não veem arquivos excluídos**: Devin, Codex cloud e Copilot coding agent clonam do remoto — se o `AGENTS.md` nunca foi commitado, eles trabalham sem SDD. Por isso o init pergunta (trigger do 3.2) o **modo git**:
  - `git-mode: stealth` (default no seu cenário) — tudo via `info/exclude`; SDD funciona nas IDEs locais + Claude Code + Codex CLI; para Devin, o conteúdo equivalente vai para Knowledge/Playbook (que vivem no app, não no repo — encaixe perfeito);
  - `git-mode: team` — os arquivos de entrada (`AGENTS.md`, `sdd/`) são commitados; agentes cloud passam a funcionar; `info/exclude` cobre só o que é pessoal (`CLAUDE.local.md`, `sdd/_tmp/`).

---

## 4. Arquitetura proposta (o que muda no template)

```
template-sdd/
  sdd/
    adapters/
      registry.yaml          # NOVO — ferramenta → detecção → shims (dados, não código)
      <tool>/ADAPTER.md      # mantidos, encolhem: viram doc do shim
    bootstrap/
      BOOTSTRAP.md           # + fase 0.5 interativa · + fase 3.5 git-exclude · consome environment.yaml
      install.py             # + bloco gerenciado no .git/info/exclude (--git-mode, --remove)
      doctor.py              # NOVO — sdd doctor: varre IDEs/plugins/CLIs → environment.yaml
      shims.py               # NOVO — gera shims a partir do registry (determinístico > generativo)
    skills/                  # NOVO (fase 2) — comandos SDD em formato SKILL.md portável
```

Princípios preservados do template: determinístico antes de generativo (doctor/shims são scripts, não prompts); core não conhece ferramenta nenhuma (tudo que é vendor-specific mora no registry + shims); AGENTS.md continua sendo o único artefato "gordo", todo o resto é ponteiro.

## 5. Boas práticas adicionais que a pesquisa sugere

1. **`CLAUDE.md` de uma linha** (`@AGENTS.md` + locks) — padrão recomendado pela própria doc da Anthropic; zero duplicação.
2. **Path-scoped rules onde existirem** (`.github/instructions/*.instructions.md` com `applyTo`, `.claude/rules/` com `paths:`): carregar as regras de `migrations/`, `api/` etc. só quando o agente tocar nesses arquivos — economia de contexto alinhada ao token-economy do framework.
3. **Orçamento de tamanho como gate**: o doctor valida que a cadeia AGENTS.md ≤ 32 KiB (limite do Codex) e que cada shim ≤ ~30 linhas.
4. **Nunca sobrescrever config de IA pré-existente** (o `detection.md` já manda "merge-or-ask") — o shims.py trata `AGENTS.md`/`copilot-instructions.md` existentes como merge com bloco gerenciado, igual ao exclude.
5. **`project_doc_fallback_filenames` do Codex** como plano B: se um repo corporativo já tiver um AGENTS.md de outro time, o SDD pode viver em `sdd/AGENTS.md` e ser registrado como fallback no `~/.codex/config.toml`.
6. **Devin via Knowledge/Playbooks para o modo stealth** — é o único runtime onde "não tocar no repo" é nativamente suportado.

## 6. Decisões que preciso de você (para a etapa 2)

1. **Modo git default**: `stealth` (info/exclude, nada commitado) como padrão, com `team` opt-in — confirma?
2. **Escrita em arquivos globais** (`global-copilot-instructions.md`, `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`): só com `--write-global` explícito, conteúdo de 3 linhas — confirma?
3. **Idioma dos artefatos gerados**: template hoje é inglês; manter inglês nos shims/AGENTS.md?
4. **Escopo da etapa 2**: proponho entregar nesta ordem — (a) `doctor.py` + `registry.yaml`; (b) `shims.py` + shims dos 4 runtimes; (c) exclude gerenciado no `install.py`; (d) fase interativa no BOOTSTRAP.md + prompt files/commands/skills de `sdd-init`. Devin Playbooks entra como texto pronto para colar no app.

## 7. Fontes principais

- VS Code — custom instructions: https://code.visualstudio.com/docs/agent-customization/custom-instructions
- VS Code — prompt files (inputs interativos): https://code.visualstudio.com/docs/copilot/customization/prompt-files
- GitHub Docs — instruções por IDE (inclui path global do JetBrains): https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
- GitHub Changelog — AGENTS.md/CLAUDE.md no JetBrains (mar/2026): https://github.blog/changelog/2026-03-11-major-agentic-capabilities-improvements-in-github-copilot-for-jetbrains-ides/
- Claude Code — memória/CLAUDE.md/AGENTS.md import: https://code.claude.com/docs/en/memory
- Codex — AGENTS.md (precedência, 32 KiB, fallbacks): https://developers.openai.com/codex/guides/agents-md
- Codex — custom prompts (deprecados → skills): https://developers.openai.com/codex/custom-prompts
- Devin — AGENTS.md: https://docs.devin.ai/onboard-devin/agents-md
