---
type: flow
aliases:
  - "Serviço HtmlToPdf — fluxo de geração de PDF"
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - geracao-pdf
sources:
  - app/__init__.py
  - app/pdf/routes.py
  - app/pdf/service.py
  - app/errors.py
---
# Serviço HtmlToPdf — fluxo de geração de PDF

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever a sequência ponta a ponta de `POST /html-to-pdf/generate`.

## Evidências
- `app/__init__.py` (middleware), `app/pdf/routes.py::html_to_pdf`, `app/pdf/service.py::generate_pdf`, `app/errors.py`.

## Informações confirmadas
1. ✅ `before_request`: define `request_id` (`X-Request-ID` ou UUID) e inicia o cronômetro.
2. ✅ Valida `request.is_json`; senão `ApiError` 400 `invalid_content_type`.
3. ✅ Valida que o JSON é objeto; senão 400 `invalid_json_payload`.
4. ✅ Valida `HtmlString` como string não vazia (após `strip`); senão 400 `invalid_html_string`.
5. ✅ `generate_pdf` aplica o CSS base e chama o WeasyPrint; falha → 500 `pdf_generation_failed`, registrada com `logger.exception` uma vez.
6. ✅ Sucesso: log `pdf_generated` e resposta `200 application/pdf`.
7. ✅ `after_request`: devolve `X-Request-ID` e registra `http_request_completed` com `duration_ms`.

## Inferências e limitações
- Um JSON malformado com `Content-Type` JSON é tratado pelo Flask (`HTTPException` 400), não por `ApiError`. 🔶 pelo comportamento do Flask, sem teste específico.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/03-Modulos/Servico-HtmlToPdf-Servico-Geracao-de-PDF|Módulo de geração]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/06-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Nenhuma específica.
