---
type: architecture
aliases:
  - "Arquitetura em camadas"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
sources:
  - src/main/java/br/gov/df/transparencia/Application.java
  - src/main/java/br/gov/df/transparencia/util/JdbcUtil.java
  - src/main/java/br/gov/df/transparencia/util/ReportUtil.java
  - src/main/java/br/gov/df/transparencia/handler/ResourceExceptionHandler.java
  - src/main/java/br/gov/df/transparencia/servico/servidor/RemuneracaoService.java
  - src/main/java/br/gov/df/transparencia/api/servidor/RemuneracaoRelatorioController.java
  - pom.xml
---
# Arquitetura em camadas

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Stack-e-Dependencias|Stack-e-Dependencias]]

## Objetivo
Descrever a estrutura do `portal-transparencia-backend`: pacotes, camadas e o caminho de uma consulta, para orientar leituras e mudanças.

## Evidências
Leitura de `Application.java`, `util/JdbcUtil.java`, `util/ReportUtil.java`, `handler/ResourceExceptionHandler.java`, `servico/servidor/RemuneracaoService.java`, `api/servidor/RemuneracaoRelatorioController.java` e do `pom.xml` (plugin gerador de `Sql`). Contagem de arquivos `.java` por pacote em `src/main/java/br/gov/df/transparencia`.

## Informações confirmadas
- ✅ Aplicação monolítica Spring Boot (`@SpringBootApplication`, `@EnableWebMvc`, `@EnableAspectJAutoProxy`, `@EnableRabbit`, `@EnableAsync`), pacote raiz `br.gov.df.transparencia`, com locale padrão `pt-BR` definido no `main`.
- ✅ Pacotes principais e tamanho (arquivos `.java`): `api` 74 (controllers), `servico` 65, `modelo` 122, `dto` 10, `enums` 7, `util` 9, `repositorio` 6, `persistencia` 3, `filtro` 3, `cache` 2, `aop` 1, `annotations` 2, `handler` 2, `externalServices` 4, `config/prometheus` 2.
- ✅ **Caminho de uma consulta** (padrão dominante):
  1. Controller em `api/<área>` (a maioria é `@RestController` com `GET`; ver [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]). Os parâmetros de filtro chegam como bean de modelo (ex.: `Remuneracao`) mais `Pageable`.
  2. Serviço em `servico/<área>` monta um `Map<String,Object>` de parâmetros e chama `JdbcUtil`.
  3. `JdbcUtil` renderiza um **template Velocity** em `resources/sql/**.vm` (`VelocityEngineUtils.mergeTemplateIntoString`), executa com `JdbcTemplate`, mapeia por `BeanPropertyRowMapper` e devolve `Page`/`CustomPage` (com totalizador); a contagem usa `sql/selectCount.vm` sobre a query sem `ORDER BY`. Há também `EntityConsumer`, para exportação em fluxo sem carregar tudo em memória.
  4. Alguns serviços usam a classe gerada `br.gov.df.transparencia.jdbc.Sql` (gerada de `resources/sql` pelo `spring-jdbc-maven-plugin` em `generate-sources`; fica em `target/generated-sources`), com métodos como `listArquivosPorCategoria`.
  5. Métodos de serviço anotados `@Mascaravel` passam pelo `MascaramentoAspect` (ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]]).
- ✅ **Relatórios**: controllers `*RelatorioController` estendem `util/RelatorioController` (`responseWrapper`) e respondem com `StreamingResponseBody` gerado por `ReportUtil` (PDF por iText + Velocity em `resources/relatorios/*.vm`, ou CSV). Ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Relatorios-e-Exportacao|Relatorios-e-Exportacao]].
- ✅ **JPA** é minoritário: 6 entidades (`PesquisaSatisfacao`, `RegistroContato`, `NotaLancamentoEvento`, `Expulsao`, `Conselheiro`, `ReceitaPrincipal`) e 3 repositórios Spring Data (`@EnableJpaRepositories` em `br.gov.df.transparencia.repositorio`). As gravações (`RegistroContatoPersistence`, `RegistroPesquisaPersistence`) estendem `PersistenceHelper`, que cria um `EntityManagerFactory` próprio pela unidade `bdPortalProd` de `META-INF/persistence.xml` (ver [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Debitos-Tecnicos|Debitos-Tecnicos]]).
- ✅ **Filtros** (ordem): `CorsFilter` (precedência máxima), `ClienteIdFilter` (máxima + 1), `PrometheusMetricsFilter`. Ver [[01-Sistemas/Portal-Transparencia/Backend/08-Seguranca/Portal-Transparencia-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].
- ✅ **Tratamento de erros**: `ResourceExceptionHandler` (`@ControllerAdvice`) devolve `StandardError` (timestamp, status, erro, mensagem, caminho) para `ObjectNotFoundException` (404), parâmetro ausente (400), falha de conexão JDBC (504), `UncategorizedSQLException` (500, mensagem genérica), `NullPointerException` (500) e `IndexOutOfBoundsException` (retorna status **204**, o que mascara um erro de programação como "sem conteúdo"). Há ainda `NegocioException` (checked, sem tratador específico encontrado).
- ✅ **Cache** em memória com Guava (3 gerenciadores) e **mensageria** RabbitMQ somente para invalidar um cache; ver módulo de cache.
- ✅ **Observabilidade**: `PrometheusMetricsFilter` (contador e histograma por método/URI/status), `PrometheusMetricsController` (`/prometheus`), `Healthcheck` (`/healthcheck`), agente New Relic versionado em `resources/newrelic`.

## Inferências e limitações
- 🔶 O desenho é uma "API de consulta sobre views/tabelas de carga": a lógica de negócio vive nos `.vm` (547 arquivos em `resources/sql`, 17 pastas de área) e não em objetos de domínio. Não houve leitura dos SQL um a um.
- 🔶 `synchronized` em alguns métodos de controller de relatório (ex.: `relatorioRemuneracao`) serializa as requisições desse endpoint; impacto não medido.
- ❓ Não há camada de segurança (Spring Security) nem versionamento formal de API além do prefixo `v2/` em alguns controllers (convivem `v1` implícito e `v2`).

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]] · [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco-e-Migrations]] · [[01-Sistemas/Portal-Transparencia/Backend/06-API/Portal-Transparencia-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]

## Pendências e próximo passo
- Módulos por área: ver o [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]]; falta leitura dirigida dos `.vm`.
