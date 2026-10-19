---
type: integration
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
consumer: KEYCLOAK-CGDF
provider: IBS
tags:
  - keycloak-cgdf
  - integracao
  - ibs
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsApiClient.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsLoginRequest.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsLoginResponse.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/config/IbsConfig.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/client/IbsRestClientTest.java
---
# Integração Keycloak → IBS

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `KEYCLOAK-CGDF` (`keycloak`) | `IBS` | HTTP POST JSON (`java.net.http.HttpClient`) | `POST {ibsBaseUrl}/auth` | saída |

## Evidências
- `IbsApiClient.login`, `loginUri`; `IbsLoginRequest`; `IbsLoginResponse`; `IbsConfig`; testes `IbsRestClientTest` (7 cenários, com WireMock).

## Informações confirmadas
**Requisição:** cabeçalhos `Content-Type: application/json`, `X-Correlation-ID` (UUID novo a cada chamada) e `X-IBS-Secret` (se houver segredo). Corpo: `{"login": ..., "senha": ..., "idOrgao": "<texto>"}`. A barra final de `ibsBaseUrl` é removida; o caminho `/auth` é sempre acrescentado (não incluir `/auth` na configuração).

**Resposta esperada (campos usados):** `autenticado`, `idUsuario`, `correlationKey`, `message` e `claims` (`login`, `idOrgao`, `siglaOrgao`, `nomeOrgao`, `nomePessoa`, `nomeSocial`, `matricula`, `unidades[]`). Campos desconhecidos são ignorados.

**Tratamento do HTTP:**

| HTTP do IBS | Resultado no cliente |
|---|---|
| 200 | desserializa a resposta |
| 401 | desserializa a resposta (autenticação negada, com `message`) |
| qualquer outro (403, 404, 500…) | `IOException("IBS retornou HTTP n.")` → `server_error` |
| timeout / conexão recusada | `IOException` → `server_error` |

**Configuração** (ordem de precedência: configuração da execução → propriedade de sistema → variável de ambiente):

| Parâmetro | Chaves aceitas | Padrão |
|---|---|---|
| URL base (obrigatória) | `ibsBaseUrl`, `ibs.url` / env `IBS_BASE_URL`, `IBS_URL` | — |
| Timeout | `ibsTimeoutSeconds` (s) ou `ibs.timeout-ms` / env `IBS_TIMEOUT_SECONDS`, `IBS_TIMEOUT_MS` | 3 s |
| Segredo | `ibs.shared-secret` / env `IBS_SHARED_SECRET` | vazio (sem cabeçalho) |

O mesmo timeout vale para conexão e requisição. Valores de URL por ambiente não estão no repositório.

## Falhas e dependências
- O IBS é dependência síncrona do login: indisponibilidade impede toda autenticação pelo fluxo `ibs-authenticator`.
- Não há retry, circuit breaker nem cache de resposta no código (✅ ausência verificada nas classes do cliente).

## Inferências e limitações
- ❓ Dono, tecnologia, ambientes e SLA do IBS não identificados (ID `IBS` cadastrado no catálogo como serviço externo, sem repositório).
- ❓ Consumidores do fluxo (clients/realms que usam `ibs-authenticator`) não identificados. Informado pelo usuário: o SICI **não** usa este componente (usa o AD).
- 🔶 O README mostra o IBS em `host.docker.internal` apenas para uso local.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[Catalogo-de-Sistemas|Catálogo de sistemas]]
- Lado provedor (IBS): [[01-Sistemas/IBS/IBS-Index|IBS]] · [[01-Sistemas/IBS/Backend/05-API/IBS-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do IBS]] · [[01-Sistemas/IBS/Backend/06-Seguranca/IBS-Backend-Seguranca-e-Autorizacao|Segurança do IBS]]

## Pendências e próximo passo
- Confirmar dono e contrato oficial do IBS (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]]).
