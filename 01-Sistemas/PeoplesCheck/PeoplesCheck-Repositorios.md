---
type: repository
system: PeoplesCheck
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - repositorios
---
# PeoplesCheck — repositórios

Voltar: [[01-Sistemas/PeoplesCheck/PeoplesCheck-Index|Índice do sistema]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `cgdf-peoples-check-api`: `git rev-parse HEAD` = `21dbf0b20b6a902e6ec879beff09db3c72300514` (branch `master`, commit de 2026-05-21, "Ajustes de constraints worker"). 55 commits.
- Remoto GitLab interno; endereço omitido.
- Árvore de trabalho limpa na data da análise.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `cgdf-peoples-check-api` | API Spring Boot de validação de CPF/CNPJ e desafio de identidade | analisado; cobertura completa do código da aplicação (leitura estática; testes não executados) | `21dbf0b` | [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]] |

## Inferências e limitações
- Não há front-end nem outros repositórios conhecidos. Os repositórios da infraestrutura de deploy (cluster) não foram analisados.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PeoplesCheck/Servico/99-Controle/PeoplesCheck-Servico-Registro-de-Analise|Registro de análise]].
