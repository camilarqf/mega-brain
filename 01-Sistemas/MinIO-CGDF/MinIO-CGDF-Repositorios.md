---
type: repository
aliases:
  - "MinIO CGDF — repositórios"
system: MinIO-CGDF
repository: minio-infra
status: confirmado
coverage: completa
analyzed_commit: f36efc5fa586f71a2f964f0f3a51a8b9383d84d2
updated: 2026-10-28
tags:
  - armazenamento-objetos
---
# MinIO CGDF — repositórios

Voltar: [[01-Sistemas/MinIO-CGDF/MinIO-CGDF-Index|Índice do sistema]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `minio-infra`: `git rev-parse HEAD` = `f36efc5fa586f71a2f964f0f3a51a8b9383d84d2` (branch `master`, commit de 2026-08-19, merge de `feat/infraestrutura-servico`).
- Remoto GitLab interno; endereço omitido. Existe também a branch remota `feature/minio-infra`.
- O nome do README e do `.iml` da IDE é `api-minio`; o do remoto é `minio-infra`.
- Fora do escopo, por decisão do usuário (2026-10-21): alterações não commitadas na árvore de trabalho (README, `stack.yml` e a pasta `scripts/`). Esta análise cobre apenas o conteúdo do commit `f36efc5`.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `minio-infra` | Dockerfile e stacks Swarm do MinIO | analisado; cobertura completa do conteúdo versionado (leitura estática, nada executado) | `f36efc5` | [[01-Sistemas/MinIO-CGDF/Infra/MinIO-CGDF-Infra-Index|Índice da Infra]] |

## Inferências e limitações
- Não há outros repositórios conhecidos no sistema.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Registro-de-Analise|Registro de análise]]. As alterações não commitadas, quando forem versionadas, seguem para `atualizar-documentacao`.

## Histórico do catálogo (até 2026-10-28)
Texto original das colunas do `Catalogo-de-Sistemas.md`, antes da simplificação (melhorias do cofre, lote 6):
- **Sistema:** MinIO da CGDF (imagem e stacks Swarm do armazenamento de objetos S3-compatível em sandbox, staging e produção; ID escolhido pelo usuário em 2026-10-21; dono não informado; publicação autorizada pelo usuário)
- **Repositórios:** `minio-infra`
- **Estado:** Analisado (commit `f36efc5`; lotes 0 a 2 concluídos, leitura estática, cobertura completa do conteúdo versionado; alterações não commitadas fora do escopo)
