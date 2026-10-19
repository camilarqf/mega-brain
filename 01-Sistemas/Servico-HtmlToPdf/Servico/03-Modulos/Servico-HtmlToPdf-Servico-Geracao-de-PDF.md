---
type: module
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - html-to-pdf
  - modulo
  - weasyprint
sources:
  - app/pdf/service.py
  - app/pdf/routes.py
  - app/errors.py
---
# Serviço HtmlToPdf — módulo de geração de PDF

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Documentar a capacidade única do serviço: transformar HTML em PDF.

## Evidências
- `app/pdf/service.py`: `generate_pdf(conteudo_html)` e constante `PDF_BASE_STYLES`.
- `app/pdf/routes.py`: `html_to_pdf` (validação e resposta).

## Informações confirmadas
- ✅ `generate_pdf` concatena `PDF_BASE_STYLES` (um bloco `<style>`) ao HTML recebido e chama `HTML(string=...).write_pdf()`; qualquer exceção vira `PdfGenerationError` (500, `pdf_generation_failed`) com a causa encadeada.
- ✅ O CSS base é sempre aplicado, antes do HTML do cliente:
  - `@page`: tamanho A4 e margem de 50px, ambos `!important`.
  - `hr`: largura 690px (`!important`) e borda superior cinza de 1px.
  - `p, span`: fonte de 16px (`!important`) e `line-height` 1.6.
  - `.card-left`: `margin-left` de 100px (`!important`).
  - `.logo-ouv > svg`: largura 100% (`!important`).
- ✅ O PDF é devolvido como `Response(pdf, content_type='application/pdf')`, em memória, sem gravar arquivo.
- ✅ Avisos do WeasyPrint sobre URL relativa e CSS ignorado são tratados por filtros de log (ver [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Observabilidade-e-Logs|Observabilidade]]).

## Inferências e limitações
- 🔶 `.logo-ouv` e `.card-left` indicam layouts específicos de um consumidor (provavelmente Ouvidoria do PARTICIPA-DF); o estilo vale para todos os consumidores.
- ❓ Fontes disponíveis no contêiner não foram inspecionadas.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/04-Fluxos/Servico-HtmlToPdf-Servico-Fluxo-Geracao-de-PDF|Fluxo]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/05-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Endpoints]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/08-Qualidade/Servico-HtmlToPdf-Servico-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Confirmar com os consumidores quais usam `.logo-ouv` e `.card-left`.
