---
type: repository
system: INGRESS-CGDF
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
tags:
  - ingress
  - repositorios
---
# INGRESS-CGDF — repositórios

Voltar: [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Index|Índice do sistema]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `ingress-controller`: `git rev-parse HEAD` = `a51459e9e167b5cb4b34910af8ffe26e583d36da` (branch `master`, commit de 2026-10-15, merge de `feat/noprod`; 107 commits no histórico).
- Remoto GitLab interno (endereço omitido). Árvore de trabalho limpa na data da análise; 50 arquivos versionados.

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `ingress-controller` | Imagem Nginx com roteamento por path e proxy TCP do RabbitMQ | analisado; cobertura completa do conteúdo versionado (leitura estática, nada executado) | `a51459e` | [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]] |

## Inferências e limitações
- Não há outros repositórios conhecidos no sistema. As stacks Swarm dos serviços atrás do ingress ficam nos repositórios deles.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Registro-de-Analise|Registro de análise]].
