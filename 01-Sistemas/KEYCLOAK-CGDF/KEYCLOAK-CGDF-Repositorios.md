---
type: repository
aliases:
  - "KEYCLOAK-CGDF — repositórios"
system: KEYCLOAK-CGDF
repository: keycloak
status: pendente
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-28
---
# KEYCLOAK-CGDF — repositórios

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Index|KEYCLOAK-CGDF]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `keycloak`: `git rev-parse HEAD` = `1755591a3abfeee96a626cedd800187263967154` (branch `master`, commit de 2026-09-03).
- Endereço do remoto omitido (infraestrutura interna).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `keycloak` | Imagem Keycloak + SPI Java 21 (Maven) + tema de login + pipeline | analisado (lotes 0 a 3; cobertura parcial) | `1755591` | [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice do Serviço Keycloak]] |

## Inferências e limitações
- 🔶 Não há outros repositórios conhecidos do sistema. Código-fonte do tema (Keycloakify) não está neste repositório (apenas o `dist` compilado); repositório de origem não identificado.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Contexto-do-Sistema|Contexto do sistema]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Para atualizar: `git diff 1755591..HEAD --stat` no repositório (skill `atualizar-documentacao`).

## Histórico do catálogo (até 2026-10-28)
Texto original das colunas do `Catalogo-de-Sistemas.md`, antes da simplificação (melhorias do cofre, lote 6):
- **Sistema:** Keycloak da CGDF (imagem, extensão Java de autenticação via IBS e tema de login; ID escolhido pelo usuário)
- **Repositórios:** `keycloak`
- **Estado:** Analisado (commit `1755591`; lotes 0 a 3 concluídos, cobertura parcial: tema só por inventário)
- 2026-10-28: publicação no remoto autorizada pelo usuário (coluna Publicação do catálogo).
