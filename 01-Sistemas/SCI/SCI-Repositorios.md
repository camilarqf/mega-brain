---
type: repository
system: SCI
repository:
  - sci-backend
  - sci-frontend
status: pendente
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - repositorios
---
# SCI — repositórios

Voltar: [[01-Sistemas/SCI/SCI-Index|SCI]]

## Objetivo
Relacionar os repositórios do SCI, o estado da análise e o commit de referência.

## Evidências
- `sci-backend`: `git rev-parse HEAD` = `8e3c8648386d0ee6767df7819faea9cdd44bef9c` (branch `master`, commit de 2026-10-18). 1068 commits, o primeiro em 2024-04-03.
- Remoto GitLab interno; endereço omitido.
- `sci-frontend`: `git rev-parse HEAD` = `5e20fda1ec781719cb277c36d160db2efd5a6c1b` (branch `master`, último commit de 2026-10-08). 845 commits, o primeiro em 2024-03-20. Remoto GitLab interno; endereço omitido. Árvore de trabalho com `environment.dev.ts` modificado e `docs/` não rastreado (fora do escopo).
- Árvore de trabalho do `sci-backend` com arquivos não commitados (POC de SSO e documentos de levantamento); **fora do escopo** desta documentação por decisão do usuário.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `sci-backend` | API REST em ASP.NET Core (.NET 10), CQRS + event sourcing parcial, SQL Server | analisado, cobertura parcial | `8e3c8648` | [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]] |
| `sci-frontend` | SPA Angular 18 (NgRx), consome o `sci-backend` | analisado por leitura estática, cobertura parcial | `5e20fda1` | [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] |

## Inferências e limitações
- A pasta `Legacy/` do repositório contém outra solução (`backend_cgdf.sln`) e não foi analisada.

## Relacionamentos
- [[01-Sistemas/SCI/SCI-Contexto-do-Sistema|Contexto do sistema]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Para atualizar: `git diff 8e3c8648386d0ee6767df7819faea9cdd44bef9c..HEAD --stat` no backend e `git diff 5e20fda1ec781719cb277c36d160db2efd5a6c1b..HEAD --stat` no frontend (skill `atualizar-documentacao`).
