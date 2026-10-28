---
type: analysis-log
aliases:
  - "Serviço HtmlToPdf — pendências"
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: pendente
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - geracao-pdf
---
# Serviço HtmlToPdf — pendências

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Listar lacunas e confirmações pendentes.

## Evidências
- Origem: lotes 0 a 3 em [[01-Sistemas/Servico-HtmlToPdf/Servico/99-Controle/Servico-HtmlToPdf-Servico-Registro-de-Analise|Registro de análise]].

## Informações confirmadas
- Item 1 (correspondência com os consumidores): confirmado pelo usuário em 2026-10-19.
- Item 4 (`LOG_LEVEL`): `WARNING`, informado pelo usuário em 2026-10-19.
- Item 2 (dono): a CGDF, informado pelo usuário em 2026-10-19. SLA continua não identificado.

## Inferências e limitações
| # | Pendência | Tipo | Nota afetada |
|---|---|---|---|
| 1 | ~~Confirmar que este repositório é o `Servico-HtmlToPdf` chamado por PARTICIPA-DF, SCI e SICI~~ — resolvido | ✅ | [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Integrações]] |
| 2 | ~~Dono do serviço~~ — resolvido (CGDF); SLA não definido/informado (baixa prioridade) | ❓ | [[01-Sistemas/Servico-HtmlToPdf/Servico-HtmlToPdf-Contexto-do-Sistema|Contexto]] |
| 3 | URLs e exposição de rede por ambiente | ❓ | [[01-Sistemas/Servico-HtmlToPdf/Servico/08-Seguranca/Servico-HtmlToPdf-Servico-Seguranca|Segurança]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Deploy-e-Ambientes|Deploy]] |
| 4 | ~~`LOG_LEVEL` efetivo por ambiente~~ — resolvido (`WARNING`) | ✅ | [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Observabilidade-e-Logs|Observabilidade]] |
| 5 | Quais consumidores usam `.logo-ouv` e `.card-left` | 🔶 | [[01-Sistemas/Servico-HtmlToPdf/Servico/03-Modulos/Servico-HtmlToPdf-Servico-Geracao-de-PDF|Geração de PDF]] |
| 6 | Executar os testes e medir cobertura | ❓ | [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Testes-e-Cobertura|Testes]] |
| 7 | Comportamento real do `url_fetcher` do WeasyPrint 70 (URLs absolutas e `file:`) | 🔶 | [[01-Sistemas/Servico-HtmlToPdf/Servico/08-Seguranca/Servico-HtmlToPdf-Servico-Seguranca|Segurança]] |

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Pendências e próximo passo
- Próximo passo: item 2 (apenas SLA) e item 3 (URLs por ambiente), se o usuário souber.
