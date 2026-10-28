---
type: reference
aliases:
  - "Iza Api — observabilidade e logs"
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: completa
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - observabilidade
sources:
  - src/main.py
  - src/log_config.py
  - .jenkins-pipelines/homolog.env.yml
  - .jenkins-pipelines/prod.env.yml
---
# Iza Api — observabilidade e logs

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Registrar o que a API emite para diagnóstico: logs, métricas e verificação de saúde.

## Evidências
- `src/log_config.py` (`sample_logger`), `src/main.py` (`Instrumentator`, `/health-check`, `print`), `.jenkins-pipelines/*.env.yml`.

## Informações confirmadas
- ✅ **Log de acesso:** o logger `uvicorn.access` (nível `INFO`) escreve em `stdout` no formato `nível data :: cliente - "linha da requisição" status`. Só contém método, caminho e status: o **corpo** da requisição (o `relato`) não é registrado.
- ✅ **Métricas:** `Instrumentator().instrument(app).expose(app, endpoint="/prometheus")` publica métricas HTTP padrão em `GET /prometheus`.
- ✅ **Saúde:** `GET /health-check` devolve `true` (sem verificar se os modelos estão carregados); também usado pelo `HEALTHCHECK` do Docker e pelo pipeline.
- ✅ **Carga de modelos:** mensagens por `print` (`Unpickle modelo de assunto|tipologia|denúncia|unidade`); não há log estruturado nem registro de falha de carga além do erro do Python.
- ✅ O `CHANGELOG.md` (2.6.0) registra a adoção do formato de log `AAAA-MM-DD HORA :: ORIGEM - CHAMADO`.

## Inferências e limitações
- ✅ Não há log da aplicação (logger próprio), de erros de inferência, de tempo de predição nem de qual `assunto`/modelo foi usado.
- 🔶 Como o health check é fixo e a carga ocorre antes de aceitar tráfego, um modelo ausente derruba o processo na inicialização em vez de reportar "não saudável".
- ❓ `NEW_RELIC_APP_NAME` está definido por ambiente, mas não há agente New Relic nas dependências nem no comando de inicialização; não se sabe se há monitoramento ativo.
- ❓ Destino e retenção dos logs (além do limite de 5 × 5m do Swarm) não constam no repositório.

## Relacionamentos
- [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Deploy-e-Ambientes|Deploy e ambientes]] · [[01-Sistemas/Iza/Api/06-API/Iza-Api-Catalogo-de-Endpoints|Catálogo de endpoints]]

## Pendências e próximo passo
- Confirmar se há agente New Relic ativo; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
