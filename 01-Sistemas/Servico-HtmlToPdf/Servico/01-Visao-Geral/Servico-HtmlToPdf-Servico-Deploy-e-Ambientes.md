---
type: reference
aliases:
  - "Serviço HtmlToPdf — deploy e ambientes"
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
  - .docker/Dockerfile
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/staging.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/prod.env.yml
---
# Serviço HtmlToPdf — deploy e ambientes

Voltar: [[01-Sistemas/Servico-HtmlToPdf/Servico/Servico-HtmlToPdf-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar como o serviço é empacotado e implantado. Valores sensíveis e credenciais não são reproduzidos.

## Evidências
- `.jenkins-pipelines/deployment.params.yml` e os três `*.env.yml`; `.docker/Dockerfile`.

## Informações confirmadas
- ✅ Imagem `html-to-pdf-img`, branch principal `master`, health check `healthcheck`.
- ✅ Três regiões:
  | Região | Cluster | Contêiner | Memória | Réplicas | Observações |
  |---|---|---|---|---|---|
  | Staging | não produtivo | `html-to-pdf-staging` | 2G | 1 | restrição de rótulo `env==staging`, rede `nginx-ingress-network` |
  | Sandbox | não produtivo | `html-to-pdf-sandbox` | 2G | 1 | restrição de rótulo `env==sandbox`, rede `nginx-ingress-network` |
  | Produção | produtivo | `html-to-pdf` | 2G | 2 | sem `network` declarado no bloco |
- ✅ Porta interna 3005; logs do contêiner limitados a 5 arquivos de 5m.
- ✅ Variáveis de ambiente dos `env.yml` (só nomes): `NEW_RELIC_APP_NAME`, `NEW_RELIC_LICENSE_KEY`. Valores omitidos.
- ✅ `LOG_LEVEL` é lido pelo código (padrão `WARNING`) mas não aparece nos `env.yml`.

## Inferências e limitações
- 🔶 "Swarm" vem do histórico de commits ("novo cluster swarm nonprod"); o arquivo em si não afirma o orquestrador.
- ❓ Hostnames/URLs expostos por ambiente não estão no repositório.

## Relacionamentos
- [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Stack-e-Dependencias|Stack]] · [[01-Sistemas/Servico-HtmlToPdf/Servico/01-Visao-Geral/Servico-HtmlToPdf-Servico-Observabilidade-e-Logs|Observabilidade]]

## Pendências e próximo passo
- Registrar URLs por ambiente se o usuário autorizar a publicação delas.
