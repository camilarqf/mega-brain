---
type: architecture
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - arquitetura
  - mediator
sources:
  - src/main/java/br/gov/df/cg/ibs/infra/config/IbsApplicationConfig.java
  - src/main/java/br/gov/df/cg/ibs/application/shared/mediator/SpringMediator.java
  - src/main/java/br/gov/df/cg/ibs/infra/cqrs/bus/Bus.java
  - src/main/java/br/gov/df/cg/ibs/api/exceptions/GlobalExceptionHandler.java
---
# IBS Backend — arquitetura em camadas

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Descrever as camadas, o mediator (CQRS) e a montagem dos beans do `identity-broker-service`.

## Evidências
- Pacotes em `src/main/java/br/gov/df/cg/ibs/`: `api`, `application`, `domain`, `infra`; `IbsApplicationConfig`; `SpringMediator`; `GlobalExceptionHandler`.

## Informações confirmadas
| Camada | Conteúdo |
|---|---|
| `api` | Controllers REST (`auth`, `usuarios`, `health`), DTOs de request/response, `GlobalExceptionHandler` |
| `application` | Casos de uso (`Command`/`Query` + handler), serviços (`AutenticacaoService`, `ClaimsService`, `FonteAutenticacaoCacheService`, `ResolverFontesAutenticacaoService`) e o mediator |
| `domain` | Entidades e value objects de fonte de autenticação, identidade institucional, claims, resultado de autenticação e exceções |
| `infra` | Repositórios JDBC, `LdapBindService`, mapper de fontes, `IbsApplicationConfig`, `OpenApiConfig`, `Bus` |

- ✅ **Mediator próprio:** o controller chama `Mediator.send(request)`. `SpringMediator` indexa os handlers pelo tipo de request (resolvido por reflexão sobre os genéricos); lança `MediatorException` quando não há handler ou há mais de um para o mesmo request.
- ✅ **Beans por `@Bean`:** handlers e serviços de `application` não usam `@Component`; são criados em `IbsApplicationConfig`, vários com `@ConditionalOnBean` (cadeia: repositório de fontes → cache → resolver → autenticação). Repositórios e `IdentidadeInstitucionalService`/`FonteAutenticacaoMapper` são `@Repository`/`@Service`/`@Component`.
- ✅ Handlers registrados: `AutenticarUsuario`, `MontarClaims`, `ObterIdentidadeInstitucional`, `ObterFontesPorSufixo`, `ResolverFontesPorOrgao`, `BuscarUsuarios`, `ObterUsuario`.
- ✅ Dependência `application` → `infra` existe (ex.: `AutenticacaoService` usa `LdapBindService` e `IdentidadeInstitucionalService`; `UsuarioController` importa `UsuarioProjection` de `infra`), portanto a separação não é hexagonal estrita.
- ✅ `@EnableScheduling` em `IbsApplicationConfig` (recarga do cache de fontes).
- ✅ Tratamento de erros centralizado em `GlobalExceptionHandler` (ver [[01-Sistemas/IBS/Backend/05-API/IBS-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]]).

## Inferências e limitações
- 🔶 O `README.md` fala em "DDD, CQRS e Event-Driven Domain". Não há eventos em uso: `domain/events/Event`, `application/eventHandlers/EventHandler` e `application/listeners/Listener` são classes vazias/esqueleto, e `Bus` (`infra/cqrs/bus`) é só um delegador ao mediator, registrado como bean sem uso encontrado. Os `.gitkeep` em `infra/services/*` e `infra/data/*` indicam pastas planejadas e vazias.
- ✅ A classe `application.exceptions.Exception` (nome igual ao de `java.lang.Exception`) não é referenciada em nenhum outro arquivo de `src`; ver [[01-Sistemas/IBS/Backend/08-Qualidade/IBS-Backend-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]] · [[01-Sistemas/IBS/Backend/01-Visao-Geral/IBS-Backend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/IBS/Backend/04-Fluxos/IBS-Backend-Fluxo-Autenticacao|Fluxo de autenticação]]

## Pendências e próximo passo
- Nenhuma além das listadas em [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Pendencias|Pendências]].
