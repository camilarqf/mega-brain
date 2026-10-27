---
type: reference
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: completa
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
tags:
  - portal-transparencia
  - backend
  - stack
sources:
  - pom.xml
  - Dockerfile
  - inject-docker-secrets-entrypoint.sh
  - src/main/java/br/gov/df/transparencia/Application.java
---
# Stack e dependências

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Objetivo
Registrar a stack e as dependências relevantes do `portal-transparencia-backend`.

## Evidências
Leitura de `pom.xml` (groupId `br.gov.df.transparencia`, artifactId `transparencia`, versão `1.0-SNAPSHOT`), `Dockerfile` e `Application.java`.

## Informações confirmadas
| Item | Valor | Evidência |
|---|---|---|
| Linguagem / build | Java 1.8, Maven | `pom.xml` (`java.version`) |
| Framework | Spring Boot **1.3.0.RELEASE** (parent), Spring MVC com `@EnableWebMvc`, AOP, `@EnableAsync`, `@EnableRabbit` | `pom.xml`, `Application.java` |
| Web | `spring-boot-starter-web`, `starter-data-rest`, `starter-velocity` | `pom.xml` |
| Acesso a dados | `starter-jdbc` (`JdbcTemplate`) e `starter-data-jpa` (6 entidades); pool **HikariCP 3.3.1**; `tomcat-jdbc` excluído | `pom.xml`, `util/JdbcUtil.java` |
| Banco | SQL Server; drivers `jtds 1.3.1` e `mssql-jdbc 6.2.2.jre8`; H2 1.4.186 (scripts `schema-h2.sql`/`data-h2.sql`) | `pom.xml`, `resources/` |
| Templates de SQL e relatórios | Apache Velocity (`/sql/**/*.vm`, `/relatorios/*.vm`) | `util/JdbcUtil.java`, `util/ReportUtil.java` |
| Geração de PDF | iText (`xmlworker 5.5.6`) | `pom.xml`, `util/ReportUtil.java` |
| Mapeamento | MapStruct 1.3.0.Final; Lombok 1.16.6; `hibernate-jpamodelgen` | `pom.xml` |
| Cache | Guava 18.0 via `GuavaCacheManager` | `cache/CacheConfig.java` |
| Mensageria | `starter-amqp` (RabbitMQ); `json-simple 1.1.1` | `pom.xml`, `servico/mascaramento/MascaramentoAMQService.java` |
| HTTP cliente | OkHttp 4.9.1 | `servico/comum/SendMailService.java` |
| Storage de objetos (MinIO) | `io.minio:minio 8.5.7` declarada no `pom.xml` (adicionada na `feat/servico-minio`), mas **sem uso no código** (nenhum `import io.minio`); o acesso ao MinIO é por `RestTemplate` | `pom.xml`, `servico/comum/storage/*` |
| Google | `google-api-client` 1.22.0 e `google-api-services-analytics v3` | `pom.xml`, `api/comum/PortalAnalyticsService.java` |
| Observabilidade | `starter-actuator 3.0.4` (versão declarada, **incompatível com o Boot 1.3** 🔶), Prometheus `simpleclient 0.16.0`, agente New Relic (`newrelic.jar` versionado) | `pom.xml`, `config/prometheus/`, `resources/newrelic/` |
| Plugin de build | `spring-jdbc-maven-plugin 1.2.0-SNAPSHOT` (`br.com.basis.maven`) gera `br.gov.df.transparencia.jdbc.Sql` a partir de `resources/sql` em `generate-sources` | `pom.xml` |
| AOP | AspectJ 1.9.6 | `pom.xml` |
| Imagem | build `maven:3.5.2-jdk-8-alpine`; runtime `amazoncorretto:8-alpine`; `tzdata` America/Sao_Paulo; `HEALTHCHECK` em `/healthcheck`; testes **pulados** no build (`-Dmaven.test.skip=true`) | `Dockerfile` |
| Segredos em runtime | entrypoint exporta cada arquivo de `/run/secrets/*` como variável de ambiente (Docker Swarm Secrets) | `inject-docker-secrets-entrypoint.sh`, `application.properties` |

## Inferências e limitações
- 🔶 O `starter-actuator` na versão `3.0.4` junto de Boot `1.3.0` parece erro de versão (a numeração 3.0.x é de outra linha); não foi verificado qual versão o Maven resolve.
- 🔶 `spring-jdbc-maven-plugin` está como dependência e como plugin; sendo `SNAPSHOT` de repositório privado (`settings.xml`), o build depende desse repositório. Conteúdo de `settings.xml` não lido.
- ✅ A dependência `io.minio:minio` está no `pom.xml` e não é importada em nenhum arquivo de `src`; é peso morto até que o storage use o cliente oficial (ver [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]).
- ❓ Não há dependência do Liquibase no `pom.xml` (ver [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]).

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Confirmar a versão real do actuator resolvida pelo Maven (`mvn dependency:tree`).
