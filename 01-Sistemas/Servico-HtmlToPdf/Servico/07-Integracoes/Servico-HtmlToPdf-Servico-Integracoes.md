---
type: integration
aliases:
  - "Serviço HtmlToPdf — integrações (lado provedor)"
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
provider: Servico-HtmlToPdf
tags:
  - geracao-pdf
sources:
  - app/pdf/routes.py
  - app/pdf/service.py
---
# Serviço HtmlToPdf — integrações (lado provedor)

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Visão geral
O serviço é **somente provedor**: não há clientes HTTP, filas nem banco no código. As notas canônicas ficam no lado de cada consumidor; esta nota só aponta para elas (BRAIN-RULES, seção 7).

| Consumidor | Provedor | Tecnologia | Direção (do ponto de vista do consumidor) | Nota canônica |
|---|---|---|---|---|
| `PARTICIPA-DF` (`participa-df-backend`) | `Servico-HtmlToPdf` | HTTP POST JSON | saída | [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas\|Integrações externas do PARTICIPA-DF Backend]] |
| `SCI` (`sci-backend`) | `Servico-HtmlToPdf` | HTTP POST JSON | saída | [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-HtmlToPdf\|Integração SCI → HtmlToPdf]] |
| `SICI` (`sici-backend`) | `Servico-HtmlToPdf` | HTTP POST JSON | saída | [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas\|Integrações externas do SICI Backend]] |

## Evidências
- Contrato do provedor: `POST /html-to-pdf/generate` com `{"HtmlString": ...}` e resposta binária `application/pdf` (`app/pdf/routes.py`).
- Contrato dos clientes: os três consumidores usam o mesmo corpo `{"HtmlString": ...}` e o mesmo caminho `html-to-pdf/generate` (notas dos consumidores).

## Informações confirmadas
- ✅ O contrato do provedor é compatível com o que os três consumidores enviam.
- ✅ O provedor devolve erros JSON com `requestId`; consumidores que propagarem `X-Request-ID` permitem correlação de logs.

## Inferências e limitações
- ✅ Confirmado pelo usuário em 2026-10-19: este repositório é o serviço usado pelos três consumidores (além da coincidência de contrato). O código em si não mostra os chamadores nem a URL implantada.
- ❓ Se algum consumidor envia `X-Request-ID` não foi verificado.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/06-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Catálogo de endpoints]]

## Pendências e próximo passo
- Registrar o dono e as URLs por ambiente quando informados.
