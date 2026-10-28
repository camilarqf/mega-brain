---
type: technical-debt
aliases:
  - "Serviço HtmlToPdf — débitos técnicos"
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: inferido
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - geracao-pdf
sources:
  - app/pdf/service.py
  - .docker/Dockerfile
  - app/logging_utils.py
  - tests/test_pdf_routes.py
---
# Serviço HtmlToPdf — débitos técnicos

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Listar riscos e melhorias recomendadas, separados dos fatos.

## Evidências
- Fatos de origem nas notas de [[01-Sistemas/Servico-HtmlToPdf/Servico/08-Seguranca/Servico-HtmlToPdf-Servico-Seguranca|Segurança]], [[01-Sistemas/Servico-HtmlToPdf/Servico/03-Modulos/Servico-HtmlToPdf-Servico-Geracao-de-PDF|Geração de PDF]] e [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Testes-e-Cobertura|Testes]].

## Informações confirmadas (fatos que motivam as recomendações)
- ✅ CSS base fixo no código, com seletores de um consumidor específico.
- ✅ Sem autenticação, sem limite de corpo, contêiner sem `USER`.
- ✅ Workers síncronos (2 por réplica) com timeout de 30s.
- ✅ Nenhum teste gera PDF real; sem medição de cobertura.
- ✅ Logs `INFO` suprimidos com o `LOG_LEVEL` padrão.

## Inferências e limitações — recomendações (🔶)
| # | Recomendação | Motivo |
|---|---|---|
| 1 | Restringir o acesso à rede interna ou exigir autenticação; avaliar `url_fetcher` restritivo no WeasyPrint | risco de SSRF e uso indevido |
| 2 | Definir `MAX_CONTENT_LENGTH` | proteção contra corpos grandes |
| 3 | Rodar como usuário não root | endurecimento da imagem |
| 4 | Tornar o CSS base opcional ou por consumidor | evitar acoplamento (`.logo-ouv`, `.card-left`) |
| 5 | Teste de integração com PDF real e medição de cobertura | WeasyPrint hoje é mockado |
| 6 | Avaliar `--worker-class gthread` ou mais workers conforme o teste de carga | geração é CPU-bound e síncrona |
| 7 | Definir `LOG_LEVEL` explicitamente nos `env.yml` (hoje é `WARNING` pelo padrão) e decidir se `http_request_completed` deve ser emitido | rastreabilidade de requisições |

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Pendências e próximo passo
- Decisão do responsável sobre quais itens priorizar.
