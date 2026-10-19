---
type: repository
system: SICI
repository:
  - sici-backend
  - sici-frontend
status: pendente
updated: 2026-10-18
tags:
  - sici
  - repositorios
---
# SICI — repositórios

Voltar: [[01-Sistemas/SICI/SICI-Index|SICI]]

## Objetivo
Relacionar os repositórios que compõem o sistema SICI, o estado da análise e o commit de referência de cada um.

## Evidências
- `sici-backend`: `git rev-parse HEAD` = `1871e323ebfc26fe75ef8f809af3a2a9e033814a` (branch `master`, commit de 2026-10-05), igual ao commit registrado em [[01-Sistemas/SICI/Backend/99-Controle/SICI-Backend-Registro-de-Analise|Registro de análise]].
- `sici-frontend`: `git rev-parse HEAD` = `418642ffc9bc8481878633a73aff6fe60b41140a` (branch `master`, commit de 2026-09-29). Análise estática em andamento; ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Registro-de-Analise|Registro de análise do Frontend]].
- Endereços dos remotos omitidos (infraestrutura interna).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `sici-backend` | API REST (Java 21, Spring Boot 3.3, SQL Server) | analisado: 6 lotes, 27 notas; cobertura parcial em `Banco-e-Migrations` (seeders não lidos de propósito) e `OS-Generica` | `1871e32` | [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] |
| `sici-frontend` | SPA Angular (interface web do SICI); consome o `sici-backend` | **em análise** (lotes 0 a 5; cobertura parcial) | `418642f` | [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] |

## Inferências e limitações
- 🔶 O backend referencia uma página de validação de QR Code no frontend (`AssinaturaProperties`, comentário da propriedade `assinatura.url.validacao`). A relação entre os repositórios precisa ser confirmada na análise do frontend.
- A relação do frontend com o sistema veio do [[Catalogo-de-Sistemas|catálogo]] e foi confirmada no código (chamadas ao backend documentado).

## Relacionamentos
- [[01-Sistemas/SICI/SICI-Contexto-do-Sistema|Contexto do sistema]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Para atualizar o frontend: `git diff 418642f..HEAD --stat` (skill `atualizar-documentacao`).
- Para atualizar o backend: `git diff 1871e32..HEAD --stat` (skill `atualizar-documentacao`).
