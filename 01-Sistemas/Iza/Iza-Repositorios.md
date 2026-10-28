---
type: repository
aliases:
  - "Iza — repositórios"
system: Iza
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
---
# Iza — repositórios

Voltar: [[01-Sistemas/Iza/Iza-Index|Índice do sistema]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `cgdf-iza`: `git rev-parse HEAD` = `988360c5302bb0785f21c4c1bb9f04da02816b7c` (branch `main`, commit de 2026-03-26, "BUG: corrige ordenamento da lista de assuntos"). Árvore de trabalho limpa na análise.
- Remoto GitLab interno chamado `cgdf-iza-api`; endereço omitido. O `README.md` está vazio (apenas o título `iza-api`).
- Ramos remotos observados nas referências locais: `main`, `homolog`, `mainbkt`, `47323-2025`, `feat/novo-cluster-swarm-nonprod`, `feat/ajuste-novo-cluster-swarm`.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `cgdf-iza` | API FastAPI que serve os modelos de triagem do Robô Iza | analisado; cobertura parcial (leitura estática; testes não executados; modelos fora do repositório) | `988360c` | [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]] |

## Inferências e limitações
- ❓ O repositório de treinamento dos modelos não é conhecido; não há front-end nem outros repositórios identificados.
- 🔶 O ramo `homolog` e o `main` usam Jenkinsfiles diferentes (`deploy/Jenkinsfile` e `deploy/Jenkinsfile.hom`); não foi verificado qual ramo alimenta cada ambiente.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Registro-de-Analise|Registro de análise]].
