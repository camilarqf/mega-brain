---
type: reference
aliases:
  - "PeoplesCheck Serviço — deploy e ambientes"
system: PeoplesCheck
component: Servico
repository: cgdf-peoples-check-api
status: confirmado
coverage: parcial
analyzed_commit: 21dbf0b20b6a902e6ec879beff09db3c72300514
updated: 2026-10-19
sources:
  - .docker/Dockerfile
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/Jenkinsfile.jobs
  - .jenkins-pipelines/prod.env.yml
  - .jenkins-pipelines/staging.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - src/main/resources/application.properties
  - pom.xml
---
# PeoplesCheck Serviço — deploy e ambientes

Voltar: [[01-Sistemas/PeoplesCheck/Servico/PeoplesCheck-Servico-Index|Índice do Serviço]]

## Objetivo
Registrar como a imagem é construída e implantada e quais ambientes existem. Valores de configuração **não** são registrados; apenas nomes.

## Evidências
- `.docker/Dockerfile`, `.jenkins-pipelines/*` e `pom.xml` (perfis Maven).

## Informações confirmadas
**Imagem (`Dockerfile`)**
- ✅ Dois estágios: build com `maven:3.8.3-openjdk-11-slim` (`mvn -Dmaven.test.skip=true -P SPRING_PROFILES_ACTIVE package`, testes **ignorados** no build) e execução com `adoptopenjdk:11-jre-hotspot`, copiando `target/peoplescheckapi.jar`.
- ✅ Fuso `America/Sao_Paulo` e atualização de tzdata (`tzupdater.jar`, base `tzdata2021d`, baixada da IANA no build).
- ✅ `ENTRYPOINT ["java", "-jar", "/peoplescheckapi.jar"]` (sem `-javaagent`). O `HEALTHCHECK` do Docker está comentado.

**Pipeline (`deployment.params.yml`)**
| Ambiente | Cluster | Réplicas | Memória | Restrições |
|---|---|---|---|---|
| Staging | `nonprod-cluster-1` | 1 | 1 GB | `role: worker`, rótulo `env==staging` |
| Sandbox | `nonprod-cluster-1` | 1 | 1 GB | `role: worker`, rótulo `env==sandbox` |
| Produção | `prod-cluster` | 2 | 2 GB | `role: worker` |

- ✅ Branch principal `master`; imagem `peoples-check-api-img`; porta interna 8080; rede `nginx-ingress-network`; endpoint de saúde `healthcheck`; logs do contêiner limitados a 5 arquivos de 5 MB.
- ✅ Cada ambiente tem um `*.env.yml` com as variáveis `SPRING_PROFILES_ACTIVE`, `NEW_RELIC_ENABLED`, `NEW_RELIC_APP_NAME` e `NEW_RELIC_LICENSE_KEY` (valores omitidos).
- ✅ Perfis Spring/Maven: `dev` (padrão), `hom` e `prod`, com `application-<perfil>.properties` (chaves de MongoDB e de API key por perfil; valores omitidos).
- ✅ `Jenkinsfile.jobs`: pipeline que dispara `DELETE {url}/jobs/{jobName}` com o cabeçalho de chave de API recebido por parâmetro; é o mecanismo de agendamento da limpeza (ver [[01-Sistemas/PeoplesCheck/Servico/03-Modulos/PeoplesCheck-Servico-Desafio-de-Identidade|Desafio de identidade]]).

## Inferências e limitações
- 🔶 As restrições de papel e rótulo e a rede indicam implantação em cluster Docker Swarm atrás de um Nginx de entrada (os repositórios `cgdf-cluster-swarm*` existem na pasta de aplicações, mas não foram analisados).
- 🔶 O `Dockerfile` passa `-P SPRING_PROFILES_ACTIVE` ao Maven, que é um **nome literal** de perfil (a variável não é expandida) e não existe no `pom.xml`; o perfil Spring efetivo em execução vem da variável de ambiente `SPRING_PROFILES_ACTIVE` do `*.env.yml`. Como `application.properties` usa `spring.profiles.active=@activatedProperties@` (filtro do Maven), o valor efetivo no JAR não foi verificado.
- 🔶 O agente New Relic não é anexado pelo `ENTRYPOINT`; só há `newrelic.jar` e `newrelic.yml` em `src/main/resources/newrelic`. Se há `-javaagent` por outro meio é ❓.
- ❓ URLs, DNS e exposição por ambiente; agendamento do job de limpeza e quem o dispara.
- 🔴 Arquivos de propriedades por perfil e `*.env.yml` versionados trazem valores de URI de banco, chave de API e licença (não literais aqui). Ver [[01-Sistemas/PeoplesCheck/Servico/09-Qualidade/PeoplesCheck-Servico-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Observabilidade-e-Logs|Observabilidade]] · [[01-Sistemas/PeoplesCheck/Servico/01-Visao-Geral/PeoplesCheck-Servico-Stack-e-Dependencias|Stack]]

## Pendências e próximo passo
- Confirmar o perfil efetivo por ambiente e a presença do agente New Relic.
