---
type: repository
system: IBS
repository: identity-broker-service
status: confirmado
coverage: parcial
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - repositorios
---
# IBS — repositórios

Voltar: [[01-Sistemas/IBS/IBS-Index|IBS]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `identity-broker-service`: `git rev-parse HEAD` = `cf0959ae140844926755b218a8452d34f3970ed3` (branch `master`, commit de 2026-08-31).
- Endereço do remoto omitido.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `identity-broker-service` | Backend Spring Boot (Java 25) de autenticação via LDAP e claims do SIP | analisado (lotes 0 a 4; cobertura parcial) | `cf0959a` | [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice do IBS Backend]] |

## Inferências e limitações
- 🔶 Não há outros repositórios conhecidos do sistema.

## Relacionamentos
- [[01-Sistemas/IBS/IBS-Contexto-do-Sistema|Contexto do sistema]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Para atualizar: `git diff cf0959a..HEAD --stat` no repositório (skill `atualizar-documentacao`).
