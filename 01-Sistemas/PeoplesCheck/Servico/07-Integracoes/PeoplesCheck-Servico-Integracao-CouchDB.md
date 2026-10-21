---
type: integration
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
consumer: PeoplesCheck
provider: CouchDB
tags:
  - peoplescheck
  - integracao
  - couchdb
sources:
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb/CouchDbClient.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb/HttClientFactory.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb/NaturalPersonRepository.java
  - src/main/java/br/gov/df/peoplescheckapi/infrastructure/couchdb/JuridicalPersonRepository.java
  - src/main/java/br/gov/df/peoplescheckapi/api/healthcheck/CouchDBHealthCheck.java
---
# PeoplesCheck Serviço → CouchDB

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `PeoplesCheck` (`cgdf-peoples-check-api`) | `CouchDB` | HTTP(S) JSON, Basic Auth | `POST /{banco}/_find` (Mango) em `chcpf_replica` e `chcnpj_replica` | saída (somente leitura) |

## Evidências
- `CouchDbClient.find`, repositórios de PF e PJ, `HttClientFactory`, `CouchDBHealthCheck`. Configuração (apenas nomes): `couchdb.uri`, `couchdb.username`, `couchdb.password`, `couchdb.pool.maxTotal`, `couchdb.pool.maxPerRoute`.

## Informações confirmadas
- ✅ Consultas e campos lidos em [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Banco-e-Persistencia|Banco e persistência]]. PF: uma consulta por CPF. PJ: duas consultas (CNPJ base e CNPJ completo).
- ✅ Pool de conexões de 100 (total) e 50 (por rota); cliente criado uma vez no construtor de `CouchDbClient`.
- ✅ Saúde: `CouchDBHealthCheck` (`GET` no `couchdb.uri`) alimenta `/healthcheck`.

## Falhas e dependências
- ✅ Sem retry, circuit breaker, fallback nem timeout configurados; erro de E/S é registrado em log e relançado (`IOException`) → 5xx ao consumidor.
- ✅ O CouchDB é dependência síncrona de `GET /people/check` e `POST /challenge/check`.
- 🔴 ✅ TLS sem validação de certificado e de host (`HttClientFactory`).
- 🔴 ✅ Seletor construído por concatenação do dado informado (sem escape): ver [[01-Sistemas/PeoplesCheck/Servico/08-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]].

## Inferências e limitações
- ❓ Dono, URL e origem das réplicas; ID `CouchDB` cadastrado no catálogo como serviço externo, com dono não identificado.
- 🔶 Nomes `*_replica` indicam réplica de uma base de origem (provavelmente dados cadastrais da Receita Federal).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/PeoplesCheck/Servico/07-Integracoes/PeoplesCheck-Servico-Integracao-MongoDB|Integração MongoDB]]

## Pendências e próximo passo
- Identificar dono e política de atualização das réplicas.
