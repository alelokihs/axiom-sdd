# Proposta — Etapa 3: Unificação `template-sdd` + `sdd-setup`

> Status: **PROPOSTA PARA REFINAR E IMPLEMENTAR** · Data: 2026-08-29 · rev. 2 (inventário do `sdd-setup` incluído)
> Origem: ideia esboçada com GPT + confronto com o estado real do `template-sdd`.
> Destino: projeto novo em `~/git/zup/`, ao lado dos dois repositórios atuais.

---

## 1. Decisão e motivação

Manter dois projetos separados — `template-sdd` (o quê instalar) e `sdd-setup` (como
instalar) — gera versionamento cruzado, documentação duplicada e o risco de um evoluir
e o outro apodrecer. O instalador não é outro produto: **é a interface de entrada do
próprio SDD**. Decisão: unir os dois num projeto novo, com uma interface intuitiva e
fácil de usar em qualquer sistema operacional.

## 2. O que a ideia do GPT acerta

Três acertos centrais, que ficam como princípios do projeto unificado:

1. **O instalador é só UX.** O fluxo é: detecta → pergunta → resolve profile → compõe
   módulos → aplica adapter → valida. Quem instala não precisa entender a estrutura
   interna do framework.
2. **Composição declarativa, nunca condicional imperativa.** A lógica "o que entra em
   cada instalação" vive em manifestos (profiles que estendem uma base, adapters com
   capabilities), não em cadeias de `if legacy && copilot && refactor` — o "COBOL do
   inferno" que o próprio GPT alertou.
3. **Adapters são tradução fina, não templates completos.** O núcleo permanece
   agnóstico; cada adapter materializa apenas o que aquela ferramenta precisa no
   projeto destino, sem versionar lixo específico de ferramenta no núcleo.

## 3. O confronto importante: boa parte disso **já existe** no `template-sdd`

O esboço do GPT foi feito sem olhar o repositório. Varredura de 2026-08-29 mostra que a
"peça que está querendo nascer" em grande parte **já nasceu** — a Etapa 3 é menos
"criar do zero" e mais "unificar, dar interface e aposentar redundância":

| Conceito no esboço do GPT | Já existe no `template-sdd` como |
|---|---|
| `templates/` por cenário | `sdd/profiles/*.yaml` — 21 profiles (`legacy-refactor`, `hotfix`, `greenfield-feature`…) |
| Manifesto com `extends` + `include` + `rules` | Exatamente o schema dos profiles: `extends: _defaults`, `agents+`, `gates+`, `dor_extra`, `dod_extra` |
| `adapters/` (copilot, claude, codex, devin) | `sdd/adapters/{copilot,claude,codex,devin}/ADAPTER.md`, com contrato documentado |
| `adapter.yaml` com `capabilities` | `sdd/agents/capability-matrix.yaml` + tabela de mecanismos por runtime (Proposta Etapa 2) |
| `workflows/` | `sdd/workflows/{fast,standard,full,hotfix}.yaml` |
| `agents/` | `sdd/agents/*.agent.md` (12 agentes) |
| Motor que "compõe módulos" | `sdd/bootstrap/install.py` — resolve profile, copia determinístico, `--update` seguro via ownership model |
| Detecção do projeto destino | `sdd/bootstrap/detection.md` (com rótulos `CONFIRMED`/`INFERRED`/`UNKNOWN`) |

**Consequência prática:** o projeto novo deve nascer da arquitetura do `template-sdd`
(que é mais madura que o esboço), absorvendo do `sdd-setup` apenas o que ele tem de
único — presumivelmente a experiência interativa de instalação. Não jogar fora o que
já foi resolvido.

## 4. Refinamentos sobre o esboço (o que realmente falta construir)

### 4.1 Motor em Python, não em Bash — divergência deliberada do esboço

O GPT propõe `install.sh` como núcleo. Mas o requisito é **"independente do sistema
operacional"**, e Bash não roda nativo em Windows. O `template-sdd` já tomou a decisão
certa: `install.py`, Python 3.8+, **stdlib pura, zero dependências** ("Deterministic
before generative: copying files is not a job for an LLM"). Refinamento:

- O motor e a interface interativa ficam em **Python stdlib** (menus numerados, ANSI
  colors e box-drawing funcionam em Terminal, iTerm, Windows Terminal e PowerShell 5+).
- `install.sh` e `install.ps1` viram, no máximo, **wrappers de 3 linhas** que localizam
  o Python e delegam — puro açúcar de entrada, nenhuma lógica.
- Nada de parsear YAML em Bash, nada de depender de `yq`. O parser mínimo de profiles
  já existe dentro do `install.py`.
- O `sdd-setup` confirma a decisão: ele já é Python 3.8+ stdlib pura, roda com um
  comando em Windows/Linux/macOS, e trocou `registry.yaml` por **JSON** justamente
  para não depender de PyYAML. O repo unificado herda essa regra.

### 4.2 O que o `sdd-setup` traz de fato — inventário de 2026-08-29

Com a pasta conectada, a varredura mudou uma premissa desta proposta: o `sdd-setup`
**não é redundante** com o `install.py` — é a implementação viva da Etapa 2, pequena
(~600 linhas, stdlib pura) e bem fatorada. O que ele contém:

| Peça | O que faz | Veredito para a fusão |
|---|---|---|
| `sddsetup/doctor.py` | Varre a **máquina** (VS Code, JetBrains, Claude Code, Codex, git) com rótulos `CONFIRMED`/`INFERRED`/`UNKNOWN`; salva `sdd/environment.json` | **Único — migrar.** É o `sdd doctor` que a Etapa 2 propôs |
| `sddsetup/shims.py` + `templates/` | Gera `AGENTS.md` canônico + shims finos por ferramenta, com **bloco gerenciado** (`>>> sdd-managed >>>`), idempotente e com `--remove` (desinstalação limpa) | **Único — migrar.** O `install.py` não tem nada disso |
| `sddsetup/registry.json` | Dados: ferramenta → sinais de detecção → shims → 5 comandos SDD renderizados no formato nativo de cada runtime | **Único — migrar e promover** (ver abaixo) |
| `sddsetup/gitexclude.py` | Modos `stealth`/`team`/`none` via `.git/info/exclude`, com aviso de arquivos já rastreados | **Único — migrar** |
| `sdd_setup.py` | Orquestração (doctor → install do core via subprocess no `install.py` do template → shims → exclude → report) + modo interativo básico + `--yes` para CI | **Fundir com `install.py`** num entrypoint só — esta é a única redundância real (dois entrypoints, ponte frágil por subprocess + caminho relativo) |
| `__pycache__/` | bytecode | Descartar (gitignore no repo novo) |

Duas consequências importantes:

**(a) O `registry.json` é o "manifesto de adapter" que o GPT propôs** — só que já
executável. Na fusão, ele vira a fonte única dos adapters: os `ADAPTER.md` do template
passam a ser documentação gerada/apontada a partir dele, eliminando a duplicação
conceitual (hoje os *locks*, por exemplo, existem nos dois repos).

**(b) O que falta de verdade é menos do que a proposta assumia.** O modo interativo já
existe em versão básica (pergunta runtimes, git-mode, template, profile por texto
livre). O trabalho novo da Etapa 3 se reduz a: (1) **detecção do projeto alvo** —
o doctor detecta a máquina, não o stack do projeto ("Java/Spring · git · legado");
(2) **menu de intenção** mapeando para os 21 profiles ([1] Base, [2] Feature, [3]
Refatoração…); (3) **seleção de runtimes por checkbox** pré-marcada pela detecção;
(4) **entrypoint único** com subcomandos (`install` interativo por default, `doctor`,
`update`, `remove`). A meta de UX continua sendo:

```
╔══════════════════════════════════════╗
║              SDD SETUP               ║
╚══════════════════════════════════════╝

Projeto detectado:   Java / Spring Boot · git · legado   [confirmar? S/n]

O que deseja fazer?  [1] Base  [2] Feature  [3] Refatoração  [4] Análise legado  [5] Challenge  [6] Custom
Runtimes:            [x] Copilot  [ ] Claude  [ ] Codex  [ ] Devin
```

Regras do modo interativo:

- **Detecção sugere, nunca decide.** Todo item detectado aparece com seu rótulo
  (`CONFIRMED`/`INFERRED`) e é confirmável/corrigível pelo usuário — coerente com
  `detection.md`.
- As opções do menu mapeiam para profiles existentes (ex.: "Refatoração" →
  `legacy-refactor` ou `technical-debt` conforme a detecção); "Custom" lista os 21.
- **Mesmo binário, dois modos:** sem argumentos → interativo; com flags → automação/CI
  (`--target … --profile … --runtimes … --yes`), com exit codes limpos.

### 4.3 Fechamento do ciclo: validação e estado instalado

- Ao fim da instalação, imprimir **resumo do que foi composto** (profile resolvido,
  agentes, workflow, adapters gerados) e rodar uma **auto-validação** (arquivos no
  lugar, entry files apontando certo).
- O `sdd doctor` da Proposta Etapa 2 entra aqui como comando irmão do instalador —
  mesma casa, mesma linguagem, mesmo espírito.
- O estado no projeto consumidor já é coberto pelo ownership model
  (framework-owned × project-owned) + `sdd.yaml` com versão; avaliar amanhã se um
  `manifest.lock` explícito (lista exata de arquivos gerados) agrega para `--update`
  e desinstalação limpa, ou se é complexidade prematura.

### 4.4 Coerência com a Etapa 2

A estratégia "AGENTS.md canônico + shims finos por ferramenta" da Etapa 2 continua
valendo e simplifica os adapters do projeto unificado. A Etapa 3 não a substitui; é a
embalagem dela.

## 5. Estrutura proposta do projeto novo

Baseada na atual, com o instalador promovido a cidadão de primeira classe:

```
sdd/                        # nome a confirmar (ver §7)
├── install.sh              # wrapper fino → cli/
├── install.ps1             # wrapper fino → cli/ (Windows)
├── cli/                    # ex-bootstrap + ex-sdd-setup: UX interativa, install, update, doctor
├── core/                   # metodologia agnóstica (14 arquivos atuais)
├── profiles/               # 21 manifestos de composição (+ _defaults)
├── workflows/              # fast · standard · full · hotfix
├── agents/                 # 12 agentes + capability-matrix.yaml
├── adapters/               # copilot · claude · codex · devin (finos, geráveis)
├── templates/              # SPEC, PLAN, TASKS, ADR, …
├── examples/               # nunca instalado no consumidor
└── docs/
```

## 6. Migração

- **De `template-sdd`:** praticamente tudo (`sdd/**`, `examples/`, docs, propostas) —
  é a base do projeto novo. `bootstrap/install.py` funde-se no `cli/`.
- **De `sdd-setup`:** quase tudo é único e migra para `cli/` — `doctor.py`,
  `shims.py`, `gitexclude.py`, `registry.json` e `templates/` (inventário completo no
  §4.2). O que morre na fusão: o entrypoint duplicado (`sdd_setup.py` + `install.py`
  viram um só, sem a ponte por subprocess) e a duplicação conceitual entre
  `registry.json` e os `ADAPTER.md` (registry vira fonte única).
- Os dois repositórios atuais ficam congelados com um README apontando para o novo.

## 7. Questões abertas (decidir amanhã, antes de codar)

1. **Nome do projeto novo** — `sdd`? `zup-sdd`? Define a pasta em `~/git/zup/`.
2. **Histórico git** — repo limpo, ou preservar histórico dos dois via
   `git filter-repo`/subtree? (Sugestão: repo limpo; os antigos ficam como arquivo.)
3. ~~Inventário do `sdd-setup`~~ — **resolvido em 2026-08-29** (§4.2): quase tudo é
   único e migra; só o entrypoint duplicado morre.
4. **`manifest.lock` explícito** no consumidor: agora ou quando a realidade pedir?
   (Nota: o bloco gerenciado + `--remove` do sdd-setup já cobrem os shims; faltaria
   só para o core instalado pelo install.py.)
5. **TUI**: stdlib pura (zero deps, aposta já tomada pelos dois repos) é suficiente,
   ou vale `rich`/`textual`? (Sugestão: stdlib — quebrar a promessa de zero
   dependências precisa de justificativa forte.)
6. **Nível da raiz**: o projeto novo mantém o prefixo `sdd/` interno ou achata a
   estrutura para a raiz do repo (como no §5)?
7. **Detecção do projeto alvo** (stack/legado, para o menu): heurística simples em
   Python (arquivos-sinal: `pom.xml`, `build.gradle`, `package.json`, idade do
   repo…) ou manter como responsabilidade do agente via `detection.md`? A UX do §4.2
   precisa dela em Python, ainda que mínima.
8. **`registry.json` como fonte única dos adapters**: confirmar a promoção e definir
   o que acontece com os `ADAPTER.md` (gerados? reduzidos a doc conceitual?).

## 8. Plano para amanhã

1. ~~Inventariar o `sdd-setup`~~ — **feito** (§4.2).
2. Fechar as questões do §7 (restam 1, 2, 4, 5, 6, 7 e 8).
3. Criar o repositório novo em `~/git/zup/` com a estrutura do §5: migrar o
   `template-sdd` e mover `sddsetup/` + `install.py` para `cli/`.
4. Fundir os entrypoints num CLI único com subcomandos (`install` interativo por
   default, `doctor`, `update`, `remove`) e escrever o que falta da UX: detecção do
   projeto alvo, menu de intenção → profile, checkboxes de runtimes.
5. Promover `registry.json` a fonte única dos adapters (desduplicar locks/ADAPTER.md).
6. Validar em um projeto real: modo interativo + modo CI (`--yes`) + `--update` +
   `--remove`.
7. Congelar os repos antigos com aviso de migração.
