---
type: reference
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
tags:
  - ibs
  - stack
sources:
  - pom.xml
  - .docker/Dockerfile
  - .jenkins-pipelines/deployment.params.yml
  - src/main/resources/application.properties
  - src/main/java/br/gov/df/cg/ibs/infra/config/IbsApplicationConfig.java
---
# IBS Backend — stack e dependências

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar linguagem, framework, dependências e empacotamento do repositório.

## Evidências
- `pom.xml`, `.docker/Dockerfile`, `application.properties`, `IbsApplicationConfig`, `deployment.params.yml`.

## Informações confirmadas
| Item | Valor |
|---|---|
| Linguagem / build | Java 25, Maven (wrapper `mvnw`), jar único |
| Framework | Spring Boot 4.0.6 (`spring-boot-starter-parent`) |
| Starters | web, actuator, data-jpa, validation, test |
| Documentação de API | springdoc-openapi 3.0.3 (`OpenApiConfig`, título "Identity Broker Service API", v1) |
| Banco | SQL Server (`mssql-jdbc`, runtime), Hikari; acesso por `JdbcTemplate`; `ddl-auto=none` |
| LDAP | JNDI (`com.sun.jndi.ldap.LdapCtxFactory`), sem biblioteca extra |
| Segurança | **não há** `spring-boot-starter-security` nas dependências |
| Porta / perfis | 8080; perfis `local`, `dev`, `hom`, `prod` (`spring.profiles.active=@spring.profiles.active@`) |
| Parâmetros | `ibs.ldap.timeout-ms=3000`; `fonte-autenticacao.cache.intervalo-recarga-ms=1800000`; `fonte-autenticacao.cache.carregar-ao-iniciar=true`; `ibs.autenticacao.fonte-recente-ttl-ms` (padrão no código: 2592000000); `catalogo.timeout-padrao-ms=5000` |
| Actuator | expõe `health,info,metrics,prometheus`; grupos de readiness (`readinessState,db`) e liveness |
| Imagem | build `maven:3.9.15-eclipse-temurin-25-alpine`, runtime `eclipse-temurin:25-jre-alpine-3.22`, usuário não root, healthcheck em `/healthcheck` |
| Deploy | pipeline Jenkins: Staging, Sandbox (1 réplica, 1G) e Produção (2 réplicas, 2G); URL do datasource entregue por secret do Docker |

## Inferências e limitações
- 🔶 `spring.datasource.url` vem de variável de ambiente nos perfis `dev`, `hom` e `prod`; o valor real não está no repositório e não foi registrado.
- O arquivo `application-local.properties` existe localmente (ignorado pelo Git) e contém credenciais; seu conteúdo não foi reproduzido (ver [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Pendencias|Pendências]]).

## Relacionamentos
- [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice do componente]]

## Pendências e próximo passo
- Nenhuma.
