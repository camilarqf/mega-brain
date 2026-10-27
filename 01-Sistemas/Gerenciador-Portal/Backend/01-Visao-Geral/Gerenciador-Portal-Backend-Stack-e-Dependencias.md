---
type: reference
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - backend
  - stack
sources:
  - pom.xml
  - src/main/java/br/gov/df/cgdf/gerenciador/GerenciadorPortalApplication.java
---
# Stack e dependências

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Registrar a stack e as dependências relevantes do backend (versões do `pom.xml`).

## Evidências
- `pom.xml`: `groupId` `br.gov.df.cgdf`, `artifactId` `GerenciadorPortal` `0.0.1-SNAPSHOT`, pai `spring-boot-starter-parent` `1.5.8.RELEASE`, `java.version` 1.8, `finalName` `novoGerenciador` (jar `novoGerenciador.jar`).
- `GerenciadorPortalApplication`: `@SpringBootApplication` + `@EnableScheduling` (nenhum `@Scheduled` encontrado no código principal).

## Informações confirmadas
| Área | Dependência (versão) | Uso |
|---|---|---|
| Web | `spring-boot-starter-web`, `spring-boot-starter-data-rest` | API REST; Spring Data REST presente (ver [[01-Sistemas/Gerenciador-Portal/Backend/08-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|débitos]]) |
| Persistência SQL | `spring-boot-starter-data-jpa`, `spring-boot-starter-jdbc`, `HikariCP` 3.4.1, `mssql-jdbc` 6.2.2.jre8, `jtds` 1.3.1 | SQL Server; `tomcat-jdbc` excluído |
| Persistência NoSQL | `spring-boot-starter-data-mongodb` | coleção `indices` |
| Armazenamento | `software.amazon.awssdk:s3` e `url-connection-client` 2.17.290 | cliente S3 para MinIO |
| Autenticação | `spring-security-jwt` 1.0.10.RELEASE | só `JwtHelper.decode` (sem starter de segurança) |
| HTTP/JSON | `httpclient` 4.3.6, `jackson-databind` 2.5.3, `gson` 2.6.2, `json-simple` 1.1.1 | cliente HTTP do RabbitMQ; log em JSON |
| Observabilidade | `spring-boot-starter-actuator` 1.5.22, `simpleclient*` 0.16.0 (Prometheus) | `/healthcheck`, `/prometheus` |
| Outros | `javax.mail` 1.6.0, `commons-fileupload` 1.3.1, `commons-io` 2.5, `validation-api` 1.1.0, `lombok` 1.16.16 | `javax.mail` sem uso identificado |
| Testes | `spring-boot-starter-test`, `json-path` | 2 classes versionadas, 3 testes (ver [[01-Sistemas/Gerenciador-Portal/Backend/08-Qualidade/Gerenciador-Portal-Backend-Testes-e-Cobertura|Testes]]) |

- ✅ Perfis Maven `desenvolvimento` (`dev`), `producao` (`prod`), `homologacao` (`homolog`) e `local` (`local`) definem `activatedProperties`, que `application.properties` repassa a `spring.profiles.active`.
- ✅ Também existem `new relic` (`newrelic.jar`/`newrelic.yml`) e `tzupdater.jar` em `src/main/resources`; não há `-javaagent` na imagem (ver [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Deploy-e-Pipeline|Deploy]]).

## Inferências e limitações
- 🔶 Spring Boot 1.5.x e Java 8 estão fora de suporte upstream; versões antigas de `jackson-databind`, `httpclient` e `commons-fileupload` foram fixadas à mão. Vulnerabilidades específicas **não foram verificadas**.
- ❓ `javax.mail`, `springloaded` (perfil `producao`) e o `@EnableScheduling`: uso real não identificado.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Arquitetura-em-Camadas|Arquitetura em camadas]]
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Perfis-e-Ambientes|Perfis e ambientes]]

## Pendências e próximo passo
- Rodar uma verificação de dependências (OWASP/`mvn dependency-check`) para listar CVEs; não executado.
