---
type: reference
aliases:
  - "PeoplesCheck Serviço — observabilidade e logs"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - observabilidade
sources:
  - src/main/resources/application.properties
  - src/main/java/br/gov/df/peoplescheckapi/api/healthcheck/HealthCheck.java
  - src/main/java/br/gov/df/peoplescheckapi/api/healthcheck/CouchDBHealthCheck.java
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/JobsController.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb/CouchDbClient.java
---
# PeoplesCheck Serviço — observabilidade e logs

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar health checks, métricas e logs.

## Evidências
- `application.properties` (`management.*`), classes `HealthCheck` e `CouchDBHealthCheck`.

## Informações confirmadas
- ✅ Actuator com base path `/`: `GET /healthcheck` (saúde, com `show-details=always`) e `GET /prometheus` (métricas Micrometer). Ambos liberados sem chave de API.
- ✅ Indicadores: `HealthCheck` (sempre `UP`, com o tempo de atividade) e `CouchDB` (`couchDB.enabled=true`): faz `GET` no URI do CouchDB com as credenciais e devolve `UP` com a `version`, ou `DOWN` com a mensagem fixa "Failed to connect to CouchDB". O disco é desabilitado (`diskspace.enabled=false`).
- ✅ **Não há indicador de saúde do MongoDB** nos arquivos lidos (apenas o padrão do Spring Boot, que o inclui se o starter estiver presente; comportamento não verificado).
- ✅ Logs: SLF4J. `JobsController` registra a limpeza ("Limpeza da base de desafios concluída…"); `CouchDbClient` registra em `debug` a URL e em `error` a falha HTTP. Nenhum arquivo de configuração de logging (logback/log4j) no repositório; usa o padrão do Spring Boot.
- ✅ Exceções do Mongo em `insertChallenge` são impressas com `printStackTrace` (não passam pelo logger).

## Inferências e limitações
- 🔴 `show-details=always` publica detalhes no endpoint público `/healthcheck` (versão do CouchDB).
- 🔶 `/prometheus` sem autenticação expõe métricas da aplicação a quem alcançar a porta.
- ❓ Nível de log por ambiente e destino dos logs (stdout do contêiner, limitado a 5×5 MB).
- Ver agente New Relic em [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Deploy-e-Ambientes|Deploy e ambientes]].

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/08-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]] · [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-CouchDB|Integração CouchDB]]

## Pendências e próximo passo
- Definir se o MongoDB deve ter indicador de saúde próprio.
