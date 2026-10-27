---
type: security
system: Servico-HtmlToPdf
component: Servico
repository: cgdf-html-to-pdf
status: inferido
coverage: completa
analyzed_commit: 1393a68d633ed2ecc7c2c6a287a2631389d86ade
updated: 2026-10-19
tags:
  - html-to-pdf
  - seguranca
sources:
  - app/__init__.py
  - app/pdf/routes.py
  - app/pdf/service.py
  - .docker/Dockerfile
  - .jenkins-pipelines/staging.env.yml
---
# Serviço HtmlToPdf — segurança

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar controles de segurança presentes e ausentes. Sem segredos.

## Evidências
- Ausência de autenticação/autorização em qualquer rota; `Dockerfile` sem instrução `USER`; nenhuma configuração `MAX_CONTENT_LENGTH`.

## Informações confirmadas
- ✅ Nenhuma rota exige autenticação ou autorização (`/html-to-pdf/generate`, `/healthcheck`, `/prometheus`, `/apidocs/`). O README descreve `/prometheus` como "sem autenticação, uso interno".
- ✅ Validação de entrada limitada a tipo e presença de `HtmlString`; o HTML não é sanitizado.
- ✅ O limite de tempo é o `--timeout 30` do gunicorn; não há limite de tamanho do corpo no código.
- ✅ O contêiner executa sem `USER` declarado (processo como root por padrão da imagem).
- ✅ Segredo de runtime: licença do New Relic via variável de ambiente (valor omitido).
- ✅ As mensagens de erro ao cliente são genéricas; detalhes e stack trace ficam só nos logs.

## Inferências e limitações
- 🔶 O WeasyPrint busca recursos por URL absoluta presentes no HTML (README); sem restrição no código, isso pode permitir requisições a hosts internos (SSRF) se o serviço for alcançável por clientes não confiáveis. Não testado; o `url_fetcher` não é customizado.
- 🔶 A exposição real (rede interna apenas ou não) depende do ingress, não verificável aqui.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/09-Qualidade/Servico-HtmlToPdf-Servico-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/06-API/Servico-HtmlToPdf-Servico-Catalogo-de-Endpoints|Endpoints]]

## Pendências e próximo passo
- Confirmar como o serviço é exposto em cada ambiente.
