---
type: reference
aliases:
  - "Perfis e ambientes"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
sources:
  - pom.xml
  - src/main/resources/application.properties
  - src/main/resources/application-dev.properties
  - src/main/resources/application-hom.properties
  - src/main/resources/application-prod.properties
  - src/main/resources/application-test.properties
  - Dockerfile
  - inject-docker-secrets-entrypoint.sh
  - src/main/java/br/gov/df/transparencia/api/comum/StorageController.java
  - src/main/java/br/gov/df/transparencia/servico/comum/storage
---
# Perfis e ambientes

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Stack-e-Dependencias|Stack-e-Dependencias]]

> Só nomes de chaves e valores não sensíveis. Hosts, usuários, senhas e chaves **não** são reproduzidos (BRAIN-RULES, seção 10).

## Objetivo
Descrever como o perfil é escolhido e o que muda entre `dev`, `hom`, `prod` e `test`.

## Evidências
`pom.xml` (profiles Maven `dev`, `hom`, `test`, `prod`, com `activatedProperties`; `dev` é `activeByDefault`), `application.properties` (`spring.profiles.active=@activatedProperties@`) e os quatro `application-<perfil>.properties`. O `Dockerfile` recebe `SPRING_PROFILES_ACTIVE` como `ARG` e o repassa ao `mvn -P`.

## Informações confirmadas
- O perfil é definido **em tempo de build** (filtragem Maven de `@activatedProperties@`), não por variável de ambiente em runtime: a imagem é gerada por ambiente.
- `application.properties` lê por variável de ambiente (preenchida pelos Docker Secrets): `spring.datasource.url` e `security.api.key.value`. Usuário e senha do datasource não aparecem nos arquivos versionados de `application*.properties`; ❓ origem (provavelmente também secrets).
- Chaves comuns: `spring.datasource.type` (Hikari), `pool-name=PortalHikariCP`, `connection-timeout`, `max-lifetime`, `leak-detection-threshold`, `server.port=8080`, `server.tomcat.max-threads=100`, `spring.data.rest.defaultPageSize`/`maxPageSize`, `spring.velocity.check-template-location=false`, `endpoints.health.id=healthcheck`.
- Chaves de RabbitMQ (`spring.rabbitmq.host/port/username/password/virtual-host`) existem em `dev`, `hom` e `prod`; o `virtual-host` muda por ambiente (`development`, `homolog`, `prod`). Os três apontam para o mesmo host (valor omitido).
- Chaves do cliente de e-mail: `email.service.url`, `security.api.key.header`, `security.api.user.agent.header`, `security.api.user.agent.value` (valores em `dev`/`hom`/`prod`, omitidos).
- Chaves do storage (MinIO): `storage.url` e `storage.bucket` existem em `hom` e `prod`; `hom` ainda tem `storage.endpoint`, que **não é lida** por nenhuma classe. Endereços omitidos. Detalhes em [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]].

| Aspecto | dev | hom | prod | test |
|---|---|---|---|---|
| Pool Hikari (`maximum-pool-size`) | 15 | 15 | 100 (`minimum-idle=15`) | 20 |
| `logging.level.br.gov.df.transparencia` | DEBUG | DEBUG | WARN | DEBUG |
| Endpoints do Actuator desabilitados (`env`, `beans`, `metrics`, `mappings`…) | não | sim | sim | não |
| `spring.data.rest` página padrão / máxima | 30 / 100 | 30 / 100 | 100 / 150 | 30 / 100 |
| `debug=true` | sim | sim | comentado | sim |
| Datasource | só pela env | só pela env | só pela env | `url` e `driverClassName` no arquivo (valor omitido) |
| RabbitMQ | sim | sim | sim | não |
| `hibernate.show_sql=true` | não | não | **sim** | não |
| `storage.url` / `storage.bucket` | **ausentes** | sim | sim | **ausentes** |

## Inferências e limitações
- 🔶 `application-test.properties` guarda a URL JDBC de um SQL Server dentro do repositório; os testes de controller sobem o contexto completo (`@SpringApplicationConfiguration`), portanto dependem de banco real.
- 🔶 `StorageService` e `StorageUrlService` leem `storage.url` e `storage.bucket` por `@Value` **sem valor padrão**, e o perfil `dev` (ativo por padrão no Maven) e o `test` não têm essas chaves. Sem outra fonte (variável de ambiente ou parâmetro de execução), o contexto pode falhar ao subir nesses perfis, inclusive nos testes de controller. Não testado.
- ❓ Como `hom` e `prod` recebem usuário/senha do banco não ficou evidente.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] · [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]

## Pendências e próximo passo
- Confirmar se `dev` e `test` recebem `storage.url`/`storage.bucket` por outro meio (pendência 20).
- Confirmar com o time como usuário e senha do banco chegam ao container (secret?).
