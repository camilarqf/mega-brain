---
type: repository
aliases:
  - "Serviço HtmlToPdf — repositórios"
system: Servico-HtmlToPdf
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - geracao-pdf
---
# Serviço HtmlToPdf — repositórios

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Index|Índice do sistema]]

## Objetivo
Relacionar os repositórios do sistema, o estado da análise e o commit de referência.

## Evidências
- `cgdf-html-to-pdf`: `git rev-parse HEAD` = `1393a68d633ed2ecc7c2c6a287a2631389d86ade` (branch `master`, commit de 2026-09-23, merge de `fix/reduz-ruido-log-css-weasyprint`). 19 commits.
- Remoto GitLab interno; endereço omitido.
- Fora do escopo: `locustfile.py` e `requirements-dev.txt` (não versionados no momento da análise) e `cgdf-html-to-pdf.iml` (modificado).

## Informações confirmadas
| Repositório | Papel | Estado | Commit analisado | Documentação |
|---|---|---|---|---|
| `cgdf-html-to-pdf` | API Flask que gera PDF com WeasyPrint | analisado; cobertura completa do código da aplicação (leitura estática; testes não executados) | `1393a68` | [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]] |

## Inferências e limitações
- Não há front-end nem outros repositórios conhecidos.

## Relacionamentos
- [[Catalogo-de-Sistemas|Catálogo de sistemas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Servico-HtmlToPdf/Servico/99-Controle/Servico-HtmlToPdf-Servico-Registro-de-Analise|Registro de análise]].
