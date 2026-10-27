---
type: api
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - api
  - endpoints
sources:
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/PeopleController.java
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/ChallengeController.java
  - src/main/java/br/gov/df/peoplescheckapi/api/controllers/JobsController.java
  - src/main/java/br/gov/df/peoplescheckapi/api/httpResponse/ValidationContractHttpResponse.java
  - src/main/java/br/gov/df/peoplescheckapi/api/security/SecurityConfig.java
  - src/main/resources/application.properties
---
# PeoplesCheck Serviço — catálogo de endpoints

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Listar o contrato HTTP exposto. Exemplos usam dados fictícios.

## Evidências
- Controllers e `SecurityConfig` (ver `sources`). Sem OpenAPI/Swagger no repositório.

## Informações confirmadas
Todos os endpoints exigem o cabeçalho de chave de API (nome em `security.api.key.header`; ✅ `X-API-KEY` conforme o cliente do consumidor e os testes), **exceto** `GET /healthcheck` e `GET /prometheus`. Falha → 401 (ver [[01-Sistemas/PeoplesCheck/Servico/08-Seguranca/PeoplesCheck-Servico-Seguranca-e-Autorizacao|Segurança]]). Sucesso de validação → 200; falha de validação (qualquer contrato de falha) → 400 com `{type, message}`.

| Verbo e caminho | Entrada | Saída | Módulo |
|---|---|---|---|
| `GET /people/check` | query `data` (CPF/CNPJ, com ou sem máscara) | 200 `challengeContract` `{responseChallenge:{id, steps[{description,item}]}}`; 400 falha | [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Validacao-de-Pessoa|Validação de pessoa]] |
| `GET /people/check/cnpj/{cnpj}` | path `cnpj`, query `data` (CPF) | igual ao anterior, com o CNPJ associado ao desafio | idem |
| `POST /challenge/check` | corpo `{"challenge":{"id":"<uuid>","keys":["<nome>","<mãe>","dd/MM/yyyy"]}}` | 200 `challengeSolvedContract` `{challenge:{id,keys[]}}`; 400 falha | [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]] |
| `GET /challenge/count-try` | query `data` | 200 inteiro (tentativas erradas); 404 se o tamanho não é 11 nem 14 | idem |
| `POST /challenge` | corpo `Challenge` (usa `personId`, `associatedPersonId`) | 201 sem corpo | idem |
| `GET /challenge` | query `id` | 200 `Challenge` (`id`, `personId`, `associatedPersonId`, `expirationDate`, `countTry`, `steps`); 404 | idem |
| `DELETE /challenge` | query `id` | 200; 404 se não existe | idem |
| `DELETE /challenge/old` | query `data` (`yyyy-MM-dd`) | 200 (apaga criados até a data) | idem |
| `DELETE /jobs/limpar-base-desafio` | — | 200 (apaga com mais de 24 h) | idem |
| `GET /healthcheck` | — | 200/503 com detalhes (público) | [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Observabilidade-e-Logs|Observabilidade]] |
| `GET /prometheus` | — | métricas Prometheus (público) | idem |

Contratos de falha (400): `invalidRequestContract`, `entityNotFoundContract`, `invalidAnswerContract`, `limitedExceeded` (mensagens em [[01-Sistemas/PeoplesCheck/Servico/02-Dominio/PeoplesCheck-Servico-Modelo-de-Dominio|Modelo de domínio]]).

## Inferências e limitações
- 🔶 `GET /challenge` devolve o `personId` (CPF) em texto; `POST /challenge` e `GET /challenge/count-try` aceitam CPF/CNPJ na query ou corpo (dados pessoais em URLs, que aparecem em logs de proxy).
- 🔶 Não há tratador global de exceções: `IOException`, `NullPointerException` e `IndexOutOfBoundsException` resultam na resposta de erro padrão do Spring (5xx).
- 🔶 `GET /people/check` aceita CPF e CNPJ no mesmo caminho (o tipo é deduzido pelo tamanho).
- ❓ Versionamento e quotas: não existem no código.
- Consumidor conhecido: operações `Check`, `CountTry`, `Challenge` e `CheckPJ` do cliente do `PARTICIPA-DF` ([[Mapa-de-Integracoes|Mapa de integrações]]).

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Consulta-e-Geracao-de-Desafio|Fluxo de consulta]] · [[01-Sistemas/PeoplesCheck/Servico/05-Fluxos/PeoplesCheck-Servico-Fluxo-Resposta-ao-Desafio|Fluxo de resposta]]

## Pendências e próximo passo
- Comparar com os DTOs do cliente do `PARTICIPA-DF` campo a campo (não feito).
