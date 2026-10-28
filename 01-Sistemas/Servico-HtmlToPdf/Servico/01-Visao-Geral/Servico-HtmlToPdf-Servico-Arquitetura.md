---
type: architecture
aliases:
  - "Serviço HtmlToPdf — arquitetura"
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
  - main.py
  - app/__init__.py
  - app/errors.py
  - app/health.py
  - app/pdf/routes.py
  - app/pdf/service.py
  - app/swagger.py
---
# Serviço HtmlToPdf — arquitetura

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Descrever a estrutura da aplicação Flask.

## Evidências
- `app/__init__.py` (`create_app`), `main.py` (`app = create_app()`).

## Informações confirmadas
- ✅ **Application factory**: `create_app()` configura logging, cria o `Flask`, registra `PrometheusMetrics(path='/prometheus')`, o Swagger, os blueprints `pdf_bp` e `health_bp` e os error handlers.
- ✅ **Camadas** (simples, sem domínio nem persistência):
  - `app/pdf/routes.py` — blueprint `pdf` e validação da requisição.
  - `app/pdf/service.py` — `generate_pdf()` com o CSS base e a chamada ao WeasyPrint.
  - `app/health.py` — blueprint `health`.
  - `app/errors.py` — `ApiError`, `PdfGenerationError` e handlers para `ApiError`, `HTTPException` e `Exception`.
  - `app/logging_utils.py` — formatter JSON, filtros do WeasyPrint e `log_extra()`.
  - `app/swagger.py` — template OpenAPI (título "CGDF HTML to PDF", versão 1.0.0).
- ✅ **Middleware**: `before_request` define `g.request_id` (header `X-Request-ID` ou UUID) e o instante inicial; `after_request` devolve `X-Request-ID` e registra a duração.
- ✅ Respostas de erro sempre em JSON `{message, errorCode, requestId}`.

## Inferências e limitações
- Execução síncrona: o gunicorn usa o worker padrão (sem `--worker-class`), então cada worker atende uma requisição por vez. 🔶 conclusão pelo padrão do gunicorn, não testada.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/05-Fluxos/Servico-HtmlToPdf-Servico-Fluxo-Geracao-de-PDF|Fluxo de geração]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Observabilidade-e-Logs|Observabilidade]]

## Pendências e próximo passo
- Nenhuma específica.
