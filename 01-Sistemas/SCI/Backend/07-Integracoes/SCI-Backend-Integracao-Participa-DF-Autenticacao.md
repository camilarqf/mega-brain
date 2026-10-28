---
type: integration
aliases:
  - "Integração SCI → PARTICIPA-DF (autenticação)"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
consumer: SCI
provider: PARTICIPA-DF
tags:
  - autenticacao
sources:
  - src/SCI.ParticipaDF.Client/Services/ParticipaDFClient.cs
  - src/SCI.ParticipaDF.Client/Extensions/ServiceCollectionExtensions.cs
  - src/SCI.ParticipaDF.Client/ParticipaDFClientSettings.cs
  - src/SCI.Application/UseCases/AutenticarUsuario/AutenticarUsuarioHandler.cs
---
# Integração SCI → PARTICIPA-DF (autenticação)

Voltar: [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas do SCI Backend]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `SCI` (`sci-backend`) | `PARTICIPA-DF` | HTTP `POST` JSON | `AuthenticateRequest {Login, Senha}` → `AuthenticateResponse`; erro com lista `Notifications[].Message` | saída |

## Evidências
- `ParticipaDFClient.Authenticate`: serializa o request, faz `POST` em `{Uri}/{AuthenticateEndpoint}`, lê `Notifications[0].Message` se o status não for de sucesso.
- Chaves de `ParticipaDFClientSettings`: `Uri`, `Timeout`, `HealthCheckEndpoint`, `AuthenticateEndpoint`, `RetryCount`, `RetryIntervalInSeconds`, `HandledEventsAllowedBeforeBreaking`, `DurationOfBreakInSeconds`, `FallbackMessage` (valores não lidos).

## Informações confirmadas
- ✅ Uso: login do SCI — o `AutenticarUsuarioHandler` envia o CPF formatado como `Login` e a senha digitada; sucesso emite o JWT do SCI ([[01-Sistemas/SCI/Backend/05-Fluxos/SCI-Backend-Fluxo-Autenticacao|Fluxo de autenticação]]).
- ✅ Resiliência (Polly no `HttpClient`): retry com intervalo, circuit breaker, timeout de 5 s por tentativa mais `HttpClient.Timeout` configurável.
- ✅ Existe `HealthCheckEndpoint` configurado (uso no `/health` não confirmado).

## Falhas e dependências
- ✅ Qualquer exceção ou resposta de erro vira `AuthenticationFailedException` com a mensagem do provedor.
- ✅ Indisponibilidade do `PARTICIPA-DF` impede o login (exceto a exceção de bypass descrita em [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]]).

## Inferências e limitações
- 🔶 A rota real corresponde, provavelmente, a `security/auth` do `PARTICIPA-DF` (catalogada em [[01-Sistemas/PARTICIPA-DF/Backend/06-API/PARTICIPA-DF-Backend-Catalogo-de-Endpoints|Catálogo de endpoints do PARTICIPA-DF]], anônima). O valor de `AuthenticateEndpoint` não foi lido.
- ❓ Se o `PARTICIPA-DF` conhece o SCI como consumidor desse endpoint.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança]]

## Pendências e próximo passo
- Confirmar o endpoint com o time do `PARTICIPA-DF`.
