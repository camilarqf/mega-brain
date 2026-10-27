---
type: reference
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: completa
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
tags:
  - peoplescheck
  - stack
sources:
  - pom.xml
  - .mvn/wrapper/maven-wrapper.properties
  - .docker/Dockerfile
---
# PeoplesCheck Serviço — stack e dependências

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar linguagem, framework e bibliotecas do repositório.

## Evidências
- `pom.xml` (propriedades `java.version` = 11 e `spring-boot.version` = 2.7.13; pai `spring-boot-starter-parent` 2.7.13; artefato `peoplescheckapi` 0.0.1-SNAPSHOT).
- `.docker/Dockerfile` (build com `maven:3.8.3-openjdk-11-slim`, execução em `adoptopenjdk:11-jre-hotspot`).

## Informações confirmadas
| Item | Valor |
|---|---|
| Linguagem / JDK | Java 11 |
| Framework | Spring Boot 2.7.13 (web, security, actuator, cache, data-mongodb) |
| Build | Maven (com wrapper `mvnw`); perfis `dev` (padrão), `hom` e `prod` definem `activatedProperties` |
| Cliente HTTP do CouchDB | Apache `httpclient` 4.5.13 + Jackson (`jackson-databind`) |
| Banco de desafios | MongoDB, driver via `spring-boot-starter-data-mongodb` |
| Métricas | `micrometer-registry-prometheus` |
| Utilitários | Lombok 1.18.20 |
| Testes | JUnit (Jupiter via `spring-boot-starter-test`), `rest-assured` 3.3.0, `spring-security-test` 5.5.1, `reactor-test` |

- ✅ Dependências sem uso aparente no código lido: `spring-boot-starter-cache` (não há `@EnableCaching` nem `@Cacheable`), `reactor-test`, `jaxb-api`, `jakarta.xml.bind-api`, `javaee-api`, `springloaded` (plugin dos perfis `hom` e `prod`).
- ✅ `spring-boot-devtools` está declarado como dependência de runtime opcional.

## Inferências e limitações
- 🔶 Misturar `javax.*` (`javaee-api` 8.0) e `jakarta.*` (3.0.1) no mesmo classpath é um risco de conflito; não há evidência de uso real.
- 🔶 Spring Boot 2.7 saiu de suporte aberto; ver [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Arquitetura|Arquitetura]] · [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Deploy-e-Ambientes|Deploy e ambientes]]

## Pendências e próximo passo
- Confirmar a versão exata do JDK em produção (a imagem de execução é a do `Dockerfile`).
