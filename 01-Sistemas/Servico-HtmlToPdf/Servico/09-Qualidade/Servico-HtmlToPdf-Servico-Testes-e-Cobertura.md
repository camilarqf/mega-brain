---
type: quality
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: confirmado
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - html-to-pdf
  - testes
sources:
  - tests/test_app.py
  - tests/test_errors.py
  - tests/test_health.py
  - tests/test_logging_utils.py
  - tests/test_pdf_routes.py
---
# Serviço HtmlToPdf — testes e cobertura

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar o que os testes automatizados cobrem.

## Evidências
- Cinco arquivos em `tests/` (`unittest`; comando `python -m unittest discover`). Testes lidos, **não executados** nesta análise.

## Informações confirmadas
| Arquivo | Cobre |
|---|---|
| `test_app.py` | geração e eco de `X-Request-ID` |
| `test_errors.py` | `errorCode` em erros HTTP não mapeados e inesperados |
| `test_health.py` | `GET /healthcheck` (200 e payload) |
| `test_pdf_routes.py` | contrato do POST (WeasyPrint mockado), 500 com log único, Content-Type inválido, `HtmlString` ausente/em branco, corpo não objeto |
| `test_logging_utils.py` | JSON válido; filtros de URL relativa e de CSS ignorado (reclassificação, mensagens não relacionadas, anexação ao logger `weasyprint`) |

- ✅ Não há medição de cobertura configurada.
- ✅ Não há teste que renderize um PDF real (o WeasyPrint é mockado nas rotas).
- ✅ `locustfile.py` (carga progressiva sobre o POST com HTML complexo) existe só na árvore de trabalho, não versionado; fora do escopo.

## Inferências e limitações
- ❓ Resultado da última execução dos testes e percentual de cobertura desconhecidos.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Observabilidade-e-Logs|Observabilidade]]

## Pendências e próximo passo
- Executar a suíte e registrar o resultado, se autorizado.
