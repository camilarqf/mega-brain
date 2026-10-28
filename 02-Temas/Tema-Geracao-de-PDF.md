---
type: index
aliases:
  - "Geração de PDF"
status: pendente
updated: 2026-10-28
tags:
  - geracao-pdf
---
# Geração de PDF

Voltar: [[Home]] · [[Mapa-de-Integracoes|Mapa de integrações]]

Tema transversal: geração de documentos PDF. Os fatos e a confirmação de cada relação vêm do [[Mapa-de-Integracoes|Mapa de integrações]]; aqui só se reúnem os caminhos.

## Visão geral
- ✅ O `Servico-HtmlToPdf` (repositório `cgdf-html-to-pdf`, Flask + WeasyPrint) recebe `POST` com `{"HtmlString": ...}` e devolve o PDF.
- ✅ Os backends do `PARTICIPA-DF`, do `SCI` e do `SICI` usam o mesmo serviço (confirmado pelo usuário em 2026-10-19).

## Por sistema
- **Servico-HtmlToPdf (provedor):** [[01-Sistemas/Servico-HtmlToPdf/Servico/05-Fluxos/Servico-HtmlToPdf-Servico-Fluxo-Geracao-de-PDF|Fluxo de geração]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/06-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Consumidores]]
- **PARTICIPA-DF:** [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|Integrações externas]]
- **SCI:** [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-HtmlToPdf|SCI → HtmlToPdf]]
- **SICI:** [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integrações externas]] · [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Assinatura-Digital|Assinatura digital]]

## Todas as notas com a tag `geracao-pdf`
```base
filters:
  and:
    - file.hasTag("geracao-pdf")
views:
  - type: table
    name: Geração de PDF
    groupBy:
      property: system
      direction: ASC
    order:
      - file.name
      - type
      - status
```
