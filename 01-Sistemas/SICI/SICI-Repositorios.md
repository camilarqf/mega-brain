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
- `sici-frontend`: repositório presente localmente; só o HEAD foi lido (`7f497cc`, em 2026-10-18). Conteúdo não analisado.
- Endereços dos remotos omitidos (infraestrutura interna).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `sici-backend` | API REST (Java 21, Spring Boot 3.3, SQL Server) | analisado: 6 lotes, 27 notas; cobertura parcial em `Banco-e-Migrations` (seeders não lidos de propósito) e `OS-Generica` | `1871e32` | [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] |
| `sici-frontend` | ❓ não identificado (🔶 provável interface web do sistema, pelo nome; não confirmado) | **não analisado** | — | — (pasta `Frontend/` não criada, conforme `BRAIN-RULES.md`) |

## Inferências e limitações
- 🔶 O backend referencia uma página de validação de QR Code no frontend (`AssinaturaProperties`, comentário da propriedade `assinatura.url.validacao`). A relação entre os repositórios precisa ser confirmada na análise do frontend.
- A relação do frontend com o sistema foi registrada a partir do [[Catalogo-de-Sistemas|catálogo]], não do código.

## Relacionamentos
- [[01-Sistemas/SICI/SICI-Contexto-do-Sistema|Contexto do sistema]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Analisar `sici-frontend` e registrar aqui o commit analisado.
- Para atualizar o backend: `git diff 1871e32..HEAD --stat` (skill `atualizar-documentacao`).
