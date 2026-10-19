---
type: reference
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - html-to-pdf
  - stack
  - dependencias
sources:
  - requirements.txt
  - .docker/Dockerfile
  - main.py
---
# Serviço HtmlToPdf — stack e dependências

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar a stack e as dependências relevantes.

## Evidências
- `requirements.txt` (versões fixadas), `.docker/Dockerfile`, `main.py`.

## Informações confirmadas
| Item | Valor |
|---|---|
| Linguagem / imagem base | Python (imagem `python:3.11-slim`) |
| Framework web | Flask 3.1.3, Werkzeug 3.1.8 |
| Servidor | gunicorn 26.2.0 (`main:app`, 2 workers, timeout 30s, porta 3005) |
| Geração de PDF | WeasyPrint 70.0 (com pydyf, tinycss2, tinyhtml5, cssselect2, pyphen, fonttools, pillow) |
| Documentação da API | flasgger 0.9.7.1 (Swagger UI em `/apidocs/`) |
| Métricas | prometheus_flask_exporter 0.23.2 (`/prometheus`) |
| APM | newrelic 13.5.0 (`newrelic-admin run-program`) |
| Bibliotecas de sistema (Docker) | cairo, pango, pangocairo, pangoft2, harfbuzz-subset, gdk-pixbuf, libffi, shared-mime-info, curl |
| Testes | `unittest` (sem dependência extra); `locust` apenas em `requirements-dev.txt` (não versionado) |

- ✅ O contêiner expõe a porta 3005 e declara `HEALTHCHECK` em `GET /healthcheck`.
- ✅ Execução local: `app.run(port=3005, debug=False)` em todas as interfaces em `main.py`.

## Inferências e limitações
- Em desenvolvimento no Windows, o README exige GTK3 e a variável `WEASYPRINT_DLL_DIRECTORIES`.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Arquitetura|Arquitetura]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Deploy-e-Ambientes|Deploy e ambientes]]

## Pendências e próximo passo
- Nenhuma específica; ver [[01-Sistemas/Servico-HtmlToPdf/Servico/99-Controle/Servico-HtmlToPdf-Servico-Pendencias|Pendências]].
