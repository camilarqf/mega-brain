---
type: reference
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - stack
  - dependencias
sources:
  - providers/pom.xml
  - .docker/Dockerfile
  - integra-login/login/theme.properties
---
# Stack e dependências

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Build-e-Deploy|Build-e-Deploy]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Arquitetura-SPI|Arquitetura-SPI]]

## Objetivo
Registrar linguagens, versões e dependências do repositório `keycloak`.

## Evidências
- `providers/pom.xml`, `.docker/Dockerfile`, `integra-login/login/theme.properties`, `integra-login/login/login.ftl`.

## Informações confirmadas
| Item | Valor | Fonte |
|---|---|---|
| Artefato Maven | `br.gov.df.cg:ibs-keycloak-extension:1.0.0` (jar) | `pom.xml` |
| Java (compilação) | `maven.compiler.release` = 21 | `pom.xml` |
| Keycloak (compilação) | `keycloak.version` = 26.3.2 (`keycloak-server-spi`, `-spi-private`, `-services`, `-core`, todos `provided`) | `pom.xml` |
| Jackson | `jackson-databind` 2.19.2 (`provided`) | `pom.xml` |
| Testes | JUnit Jupiter 5.10.3, Mockito 5.12.0, WireMock 3.9.1 (escopo `test`) | `pom.xml` |
| Plugins Maven | compiler 3.13.0, surefire 3.2.5, exec 3.6.3 (executa `IbsManualLoginRunner` no classpath de teste) | `pom.xml` |
| Imagem de build | `maven:3.9-eclipse-temurin-21` | `Dockerfile` |
| Imagem de runtime | `quay.io/keycloak/keycloak:25.0.2` | `Dockerfile` |
| Banco | Microsoft SQL Server; driver `mssql-jdbc` 13.4.0.jre11 baixado do Maven Central no build; `kc.sh build --db=mssql` | `Dockerfile` |
| Tema de login | Keycloakify (Angular) 11.9.2, `themeName` `integra-login`, `parent=keycloak`, `darkMode=true`, 30 locales | `login.ftl`, `theme.properties` |

## Inferências e limitações
- ❓ A versão de runtime (25.0.2 na imagem) difere da versão de compilação (26.3.2) e da citada no `README.md`; ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]] e [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Débitos técnicos]].
- Dependências de runtime do Keycloak (Jackson, SPI) são `provided`: o jar não as empacota.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]]

## Pendências e próximo passo
- Confirmar qual versão do Keycloak roda nos ambientes.
