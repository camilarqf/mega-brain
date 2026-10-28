---
type: reference
aliases:
  - "Serviço HtmlToPdf — observabilidade e logs"
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - geracao-pdf
  - observabilidade
sources:
  - app/logging_utils.py
  - app/__init__.py
  - app/errors.py
  - .docker/Dockerfile
---
# Serviço HtmlToPdf — observabilidade e logs

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Documentar logs, correlação e métricas.

## Evidências
- `app/logging_utils.py`: `JsonFormatter`, `FiltroUriRelativaWeasyPrint`, `FiltroPropriedadeCssIgnoradaWeasyPrint`, `configure_logging`, `log_extra`.

## Informações confirmadas
- ✅ Logs em JSON no stdout, com `timestamp`, `level`, `logger`, `message` e, quando presentes, `event`, `request_id`, `method`, `path`, `status_code`, `duration_ms`, `error_code`, `relative_url`, `exception`.
- ✅ Nível raiz vem de `LOG_LEVEL` (padrão `WARNING`). Com o padrão, os logs `INFO` (`http_request_completed`, `pdf_generated`) **não são emitidos**; só avisos e erros.
- ✅ Correlação: `X-Request-ID` do cliente ou UUID gerado, devolvido no header e no corpo de erro (`requestId`).
- ✅ Filtros no logger `weasyprint`:
  - mensagens `Relative URI reference without a base URI:` viram `WARNING` estruturado (`event=url_nao_carregada`, `relative_url`);
  - mensagens que começam com ``Ignored ` `` (CSS/SVG ignorado) viram `DEBUG` (`event=propriedade_css_ignorada`). Origem: commit `6b9a903` / branch `fix/reduz-ruido-log-css-weasyprint`.
- ✅ Erros 5xx usam `logger.exception`; 4xx usam `warning`.
- ✅ Métricas Prometheus em `/prometheus` (sem autenticação) e APM New Relic via `newrelic-admin` no `CMD` do Docker.

## Inferências e limitações
- ✅ `LOG_LEVEL` efetivo é `WARNING` (informado pelo usuário), então os logs `INFO` não são emitidos.
- ❓ Painéis, alertas e destino dos logs (stdout do contêiner, rotação `5m` × 5 arquivos no Swarm) não estão neste repositório.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Deploy-e-Ambientes|Deploy e ambientes]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Testes-e-Cobertura|Testes]]

## Pendências e próximo passo
- Nenhuma. `LOG_LEVEL` efetivo: `WARNING`, informado pelo usuário em 2026-10-19 (igual ao padrão do código).
