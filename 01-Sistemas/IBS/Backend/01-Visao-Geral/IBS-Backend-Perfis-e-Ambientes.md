---
type: reference
aliases:
  - "IBS Backend — perfis e ambientes"
system: IBS
component: Backend
repository: identity-broker-service
status: confirmado
coverage: completa
analyzed_commit: cf0959ae140844926755b218a8452d34f3970ed3
updated: 2026-10-18
sources:
  - src/main/resources/application.properties
  - src/main/resources/application-dev.properties
  - src/main/resources/application-hom.properties
  - src/main/resources/application-prod.properties
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/prod.env.yml
  - .docker/inject-docker-secrets-entrypoint.sh
---
# IBS Backend — perfis e ambientes

Voltar: [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]]

## Objetivo
Registrar perfis Spring, chaves de configuração e ambientes de deploy, sem valores sensíveis.

## Evidências
- Arquivos `application*.properties`, pipelines Jenkins, `Dockerfile` e script de entrypoint.

## Informações confirmadas
| Perfil | Origem do datasource |
|---|---|
| `local` | `application-local.properties`, **ignorado pelo Git** (existe só na máquina; ver Pendências) |
| `dev`, `hom`, `prod` | `spring.datasource.url=${SPRING_DATASOURCE_URL}`; driver SQL Server, Hikari, dialeto `SQLServerDialect` |

- ✅ `spring.profiles.active=@spring.profiles.active@` (filtragem Maven do `pom.xml`); o pipeline define `SPRING_PROFILES_ACTIVE=prod` em produção.
- ✅ Chaves de configuração própria: `catalogo.timeout-padrao-ms`, `fonte-autenticacao.cache.intervalo-recarga-ms`, `fonte-autenticacao.cache.carregar-ao-iniciar`, `ibs.ldap.timeout-ms`, `ibs.autenticacao.fonte-recente-ttl-ms` (valores em [[01-Sistemas/IBS/Backend/01-Visao-Geral/IBS-Backend-Stack-e-Dependencias|Stack]]).
- ✅ Ambientes do pipeline (`deployment.params.yml`): **Staging** e **Sandbox** (cluster não produtivo, 1 réplica, 1G) e **Produção** (cluster de produção, 2 réplicas, 2G); rede `nginx-ingress-network`, porta interna 8080, endpoint de saúde `healthcheck`, logs com rotação (5 arquivos de 5 MB).
- ✅ Cada ambiente recebe a URL do datasource por secret do Docker, injetado em `SPRING_DATASOURCE_URL` (secrets `stg-…`, `sbx-…` e `ibs-spring-datasource-url-v1`). O script `inject-docker-secrets-entrypoint.sh` (no `ENTRYPOINT`) exporta como variável de ambiente cada arquivo de `/run/secrets/` e imprime no log o nome (não o valor) de cada secret carregada.
- ✅ Fuso `America/Sao_Paulo` na imagem.

## Inferências e limitações
- ❓ Usuário e senha do banco nos perfis `dev/hom/prod`: não aparecem nos `.properties`; presume-se que venham da URL do secret ou de outra variável (não verificado).
- ❓ Hostnames e URLs externas dos ambientes não estão no repositório.
- O conteúdo de `*.env.yml` além de `SPRING_PROFILES_ACTIVE` não foi detalhado.

## Relacionamentos
- [[01-Sistemas/IBS/Backend/IBS-Backend-Index|Índice]] · [[01-Sistemas/IBS/Backend/99-Controle/IBS-Backend-Pendencias|Pendências]]

## Pendências e próximo passo
- Confirmar com a equipe como usuário/senha do banco chegam ao contêiner.
