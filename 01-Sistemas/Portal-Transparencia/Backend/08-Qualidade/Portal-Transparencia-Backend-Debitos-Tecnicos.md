---
type: technical-debt
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: e98fcc38c21e0f2063bf0c2c9377d4b492ee5062
updated: 2026-10-21
tags:
  - portal-transparencia
  - backend
  - debito-tecnico
  - riscos
sources:
  - pom.xml
  - Dockerfile
  - src/main/resources/META-INF/persistence.xml
  - src/main/java/br/gov/df/transparencia/persistencia/PersistenceHelper.java
  - src/main/java/br/gov/df/transparencia/api/comum/GoogleAnalyticsConstantes.java
  - src/main/java/br/gov/df/transparencia/handler/ResourceExceptionHandler.java
  - src/main/java/br/gov/df/transparencia/filtro/CorsFilter.java
  - src/main/java/br/gov/df/transparencia/servico/mascaramento/MascaramentoAMQService.java
  - src/main/java/br/gov/df/transparencia/api/comum/StorageController.java
  - src/main/java/br/gov/df/transparencia/servico/comum/storage
---
# Débitos técnicos e riscos

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

> Separa **fatos observados** de **recomendações**. Severidade: 🔴 alta · 🟠 média-alta · 🟡 média · 🟢 baixa. Valores sensíveis não são reproduzidos.

## Objetivo
Listar débitos e riscos do `portal-transparencia-backend` com evidência, para priorização.

## Evidências
Leitura estática dos arquivos de `sources` e das demais notas deste componente. Nada foi executado.

## Informações confirmadas (fatos)
| # | Sev. | Fato | Evidência |
|---|---|---|---|
| 1 | 🔴 | Credenciais do banco (URL, usuário e senha) em texto no `META-INF/persistence.xml`, usadas pelo `PersistenceHelper` para criar um `EntityManagerFactory` próprio (unidade `bdPortalProd`), **fora** do datasource configurado por secrets. | `persistence.xml`, `persistencia/PersistenceHelper.java` |
| 2 | 🔴 | Conta de serviço do Google: identificador, senha do certificado e caminho do `.p12` em constantes Java; o `.p12` está versionado e é copiado para a imagem. | `api/comum/GoogleAnalyticsConstantes.java`, `Dockerfile` |
| 3 | 🔴 | Ausência total de autenticação; endpoints operacionais e de integração (`/cache-expire/*`, `/integracao/*`, `/send-email`) abertos. | [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]] |
| 3b | 🔴 | Injeção de SQL: 860 referências de texto bruto em 103 arquivos SQL e 5 rotas POST com fluxo direto ao SQL (fluxo confirmado por análise estática; exploração não testada). Detalhes em [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]]. | `src/main/resources/sql`, `util/JdbcUtil.java`, `api/orcamento/OrcamentoController.java`, `api/patrimonio/PatrimonioController.java`, `api/despesa/DespesaController.java` |
| 3c | 🔴 | `/integracao/*` devolve CPF (campo `[NR-CPF]`) de servidores sem autenticação e sem filtro de medida protetiva; `MilitaresCedidos` sem `@Mascaravel`; programas sociais devolvem NIS e CPF sem máscara no SQL. Ver [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Dados-Pessoais-Expostos|Dados pessoais expostos]]. | `api/comum/IntegracaoSistemasController.java`, `resources/sql/comum`, `resources/sql/prestando-contas` |
| 4 | 🟠 | CORS `Access-Control-Allow-Origin: *`; `x-client-id` obrigatório mas sem validação. | `filtro/CorsFilter.java`, `filtro/ClienteIdFilter.java` |
| 5 | 🟠 | Stack desatualizada: Spring Boot 1.3.0 (2015), Java 8, Hibernate/Velocity antigos, Guava 18, jTDS 1.3.1, mssql-jdbc 6.2.2, imagem de build `maven:3.5.2`. | `pom.xml`, `Dockerfile` |
| 6 | 🟠 | Credenciais do RabbitMQ em `application-dev/hom/prod.properties` versionados. | `src/main/resources/application-*.properties` |
| 7 | 🟡 | `starter-actuator` declarado como `3.0.4` junto de Boot 1.3.0. | `pom.xml` |
| 8 | 🟡 | `spring-jdbc-maven-plugin` `1.2.0-SNAPSHOT` (de repositório privado) é requisito de build; sem o repositório a classe `Sql` não é gerada. | `pom.xml`, `settings.xml` |
| 9 | 🟡 | `IndexOutOfBoundsException` é convertida em `204 No Content`; `NullPointerException` em `500` com a mensagem original; erros de programação ficam disfarçados. | `handler/ResourceExceptionHandler.java` |
| 10 | 🟡 | Dois mecanismos de acesso ao banco para escrita (datasource Hikari do Spring e `EntityManagerFactory` manual por `PersistenceHelper`), e `RegistroContatoPersistence` injeta `@PersistenceContext` por cima do campo herdado. | `persistencia/*` |
| 11 | 🟡 | Testes são pulados no build da imagem (`-Dmaven.test.skip=true`); os testes de controller exigem banco real. | `Dockerfile`, `src/test` |
| 12 | 🟡 | `MascaramentoAMQService` registra falhas com `System.err`/`printStackTrace` em vez de logger; filas anônimas (`AnonymousQueue`) sem reentrega. | `servico/mascaramento/MascaramentoAMQService.java` |
| 13 | 🟡 | `System.out.println` em `DownloadController`; `@Log4j` e SLF4J misturados em classes diferentes. | `api/comum/DownloadController.java`, `handler/ResourceExceptionHandler.java` |
| 14 | 🟡 | `hibernate.show_sql=true` em `prod`. | `application-prod.properties` |
| 15 | 🟢 | `GET /send-email` com `@RequestBody` (verbo incorreto). | `api/comum/SendMailController.java` |
| 16 | 🟢 | Controllers e entidades comentados e legados no código (`UserInterceptorFilter` e `comum/PesquisaSatisfacaoController` totalmente comentados; `afterReturning` comentado no aspecto). | `filtro/UserInterceptorFilter.java`, `api/comum/PesquisaSatisfacaoController.java`, `aop/MascaramentoAspect.java` |
| 17 | 🟢 | Binários e logs no diretório do projeto: `newrelic.jar` e `.p12` versionados; `portal2016.log*`, `runtime-8081*.log` e `hs_err_pid*.log` existem na raiz (não versionados). | `git ls-files`, raiz do repositório |
| 18 | 🟡 | O `HealthIndicator` `Healthcheck` sempre responde UP (não testa banco, RabbitMQ nem dependências); o `HEALTHCHECK` do `Dockerfile` chama `/healthcheck` e só prova que o processo responde. | `api/comum/Healthcheck.java`, `Dockerfile` |
| 19 | 🟢 | Changelogs Liquibase presentes sem dependência/plugin Liquibase no `pom.xml` (ver [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]]). | `resources/changelog*`, `pom.xml` |
| 20 | 🟡 | Módulo de storage: dependência `io.minio:minio 8.5.7` sem uso; `storage.endpoint` (`hom`) sem leitura; `printStackTrace` em `StorageService`; `RestTemplate` instanciado na classe, sem timeout; `@Value` de `storage.url`/`storage.bucket` sem valor padrão (ausentes em `dev`/`test`, 🔶 risco de falha de subida); `/storage/url` devolve o host interno e não valida o nome do arquivo. | `pom.xml`, `servico/comum/storage/*`, `api/comum/StorageController.java`, `application-*.properties` |

## Inferências e limitações
- ✅ Risco de **injeção de SQL** pela interpolação Velocity: fluxo confirmado por análise estática (item 3b); a exploração real e o privilégio do usuário de banco continuam não verificados.
- 🔶 Possível leitura fora do diretório em `/download/arquivos/{nome}` (a verificar).
- 🔶 `synchronized` em métodos de controller de relatório pode limitar concorrência.

## Recomendações (não são fatos do código)
1. Rotacionar e retirar do repositório as credenciais dos itens 1, 2 e 6 (usar os Docker Secrets já adotados); remover o `.p12` do repositório e da imagem.
2. Definir se o portal deve ou não exigir autenticação nos endpoints operacionais e de integração (`/cache-expire`, `/integracao`, `/send-email`); no mínimo protegê-los por rede ou gateway.
3. Parametrizar as consultas (parâmetros `?`/`NamedParameterJdbcTemplate`) e validar entrada antes de renderizar os `.vm`.
4. Planejar migração do Spring Boot/Java com testes de regressão; começar por um ambiente de testes com banco descartável.
5. Trocar o acesso JPA manual por `EntityManager` gerenciado pelo Spring.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Stack-e-Dependencias|Stack-e-Dependencias]] · [[01-Sistemas/Portal-Transparencia/Backend/08-Qualidade/Portal-Transparencia-Backend-Testes-e-Cobertura|Testes-e-Cobertura]]

## Pendências e próximo passo
- Revisar à mão as 126 referências não resolvidas e validar a injeção em ambiente de teste (ver [[01-Sistemas/Portal-Transparencia/Backend/06-Seguranca/Portal-Transparencia-Backend-Revisao-de-Injecao-de-SQL|Revisão de injeção de SQL]]).
