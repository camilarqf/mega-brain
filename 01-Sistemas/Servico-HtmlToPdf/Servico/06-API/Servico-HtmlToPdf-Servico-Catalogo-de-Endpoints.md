---
type: api
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - html-to-pdf
  - api
  - endpoints
sources:
  - app/pdf/routes.py
  - app/health.py
  - app/errors.py
  - app/__init__.py
  - README.md
---
# Serviço HtmlToPdf — catálogo de endpoints

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Documentar o contrato HTTP exposto.

## Evidências
- `app/pdf/routes.py` (`html_to_pdf`), `app/health.py` (`health_check`), `app/errors.py`, `app/__init__.py`.

## Informações confirmadas
| Método | Caminho | Função | Resposta |
|---|---|---|---|
| POST | `/html-to-pdf/generate` | Gera o PDF | `200 application/pdf` (bytes) |
| GET | `/healthcheck` | Saúde | `200` JSON `{uptime, message: "OK", timestamp}` |
| GET | `/prometheus` | Métricas Prometheus | texto Prometheus |
| GET | `/apidocs/` · `/apispec_1.json` | Swagger UI e spec (README) | — |

**Requisição de `POST /html-to-pdf/generate`:** `Content-Type: application/json`, corpo `{"HtmlString": "<html>"}`. O header `X-Request-ID` é opcional e ecoado.

**Erros** (corpo `{message, errorCode, requestId}`):
| Situação | Status | `errorCode` |
|---|---|---|
| `Content-Type` não JSON | 400 | `invalid_content_type` |
| Corpo JSON não é objeto | 400 | `invalid_json_payload` |
| `HtmlString` ausente, não string ou em branco | 400 | `invalid_html_string` |
| Falha do WeasyPrint | 500 | `pdf_generation_failed` |
| Outros `HTTPException` (404, 405, 415…) | código HTTP | nome do erro em minúsculas com `_` |
| Exceção inesperada | 500 | `internal_server_error` |

- ✅ Recursos relativos (`/style/x.css`) não são carregados; só URL absoluta, `data:` URI ou conteúdo inline (README). Ver [[01-Sistemas/Servico-HtmlToPdf/Servico/03-Modulos/Servico-HtmlToPdf-Servico-Geracao-de-PDF|Geração de PDF]].

## Inferências e limitações
- ❓ Limite de tamanho do corpo não definido no código (ver [[01-Sistemas/Servico-HtmlToPdf/Servico/08-Seguranca/Servico-HtmlToPdf-Servico-Seguranca|Segurança]]).

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/05-Fluxos/Servico-HtmlToPdf-Servico-Fluxo-Geracao-de-PDF|Fluxo]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/07-Integracoes/Servico-HtmlToPdf-Servico-Integracoes|Consumidores]]

## Pendências e próximo passo
- Nenhuma específica.
