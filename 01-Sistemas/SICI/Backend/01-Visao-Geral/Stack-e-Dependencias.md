---
type: reference
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
created: 2026-10-16
updated: 2026-10-18
tags:
  - sici
  - stack
  - dependencias
sources:
  - pom.xml
  - .docker/Dockerfile
  - settings.xml
---

# Stack e dependências

Voltar: [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/01-Visao-Geral/Arquitetura-Hexagonal|Arquitetura-Hexagonal]], [[01-Sistemas/SICI/Backend/01-Visao-Geral/Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Núcleo ✅
| Item | Versão / valor | Evidência |
|---|---|---|
| Java | 21 | `pom.xml` → `<java.version>` |
| Spring Boot (parent) | 3.3.0 | `pom.xml` → `spring-boot-starter-parent` |
| Build | Maven + wrapper (`mvnw`) | `pom.xml`, `.mvn/wrapper` |
| Artefato | `sici.jar` (`finalName`) | `pom.xml` → `spring-boot-maven-plugin` |
| Classe principal | `SiciApplication` (`@SpringBootApplication`) | `src/main/java/br/gov/df/cg/sici/SiciApplication.java` |

## Dependências por finalidade ✅
| Finalidade | Dependências |
|---|---|
| Web/REST | `spring-boot-starter-web`, `spring-boot-starter-validation` |
| Persistência | `spring-boot-starter-data-jpa`, `hibernate-core 6.2.3.Final` (fixado), `mssql-jdbc` (runtime), `h2` (runtime), HikariCP |
| Migrations | `flyway-sqlserver` → `src/main/resources/db/migrations` |
| Segurança | `spring-boot-starter-security`, `oauth2-resource-server`, `oauth2-client` |
| Mapeamento | `mapstruct 1.5.2.Final` + `mapstruct-processor`, `lombok` |
| Documentação API | `springdoc-openapi-starter-webmvc-ui 2.3.0` (Swagger UI) — config em `api/config/OpenSwagger.java` |
| PDF / templates | `spring-boot-starter-thymeleaf` (HTML) + API externa de PDF via `okhttp 4.9.1` (`application/service/comum/PdfService.java`) |
| QR Code | `com.google.zxing:core` e `javase 3.5.2` (`application/utils/QRCodeGenerator.java`, `ImagemUtils.java`) |
| Observabilidade | `spring-boot-starter-actuator`, `micrometer-registry-prometheus` |
| Outros | `spring-boot-starter-aop`, `spring-boot-starter-cache`, `spring-boot-devtools` |
| Testes | `spring-boot-starter-test`, `spring-security-test`, `spring-boot-testcontainers`, `testcontainers:junit-jupiter`, `testcontainers:postgresql` |

## Observações
- 🔶 `spring-boot-starter-cache` e `-aop` estão declarados, mas não foram encontrados `@Cacheable`, `@EnableCaching` nem aspectos próprios na varredura inicial — possivelmente não utilizados. Confirmar no lote 6.
- 🔶 `hibernate-core` fixado em 6.2.3 enquanto o Boot 3.3 gerencia uma versão mais nova (6.5.x) → risco de incompatibilidade. Ver [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Debitos-Tecnicos]].
- ✅ Testcontainers usa **PostgreSQL**, mas o banco da aplicação é **SQL Server** (`application-*.properties` → `SQLServerDriver`).
- ✅ Dialeto configurado: `SQLServer2012Dialect` (obsoleto no Hibernate 6).

## Build e container ✅
Fonte: `.docker/Dockerfile`
- Multi-stage: `maven:3-eclipse-temurin-21-alpine` (build) → `eclipse-temurin:21-jdk-alpine` (runtime).
- Build: `mvn -Dmaven.test.skip=true -P SPRING_PROFILES_ACTIVE package` — **testes são pulados** no build da imagem.
- Timezone do container: `America/Sao_Paulo`.
- `HEALTHCHECK` via `curl` em `/healthcheck` na porta 8080.
- 🔶 O argumento `-P SPRING_PROFILES_ACTIVE` é passado como **texto literal** (sem `${}`), portanto não ativa nenhum profile Maven existente; o profile efetivo dependerá do `activeByDefault` (`desenvolvimento`) e/ou da variável de ambiente em runtime. Ver [[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendencias]].
- CI/CD: pipelines Jenkins em `.jenkins-pipelines/` (sandbox, staging, prod) com arquivo de parâmetros de deployment (cluster, réplicas, memória, healthcheck). Conteúdo de variáveis não registrado.
