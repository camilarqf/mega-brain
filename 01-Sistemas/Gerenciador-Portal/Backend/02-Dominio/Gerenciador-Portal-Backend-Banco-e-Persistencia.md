---
type: persistence
aliases:
  - "Banco e persistência"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/model
  - src/main/java/br/gov/df/cgdf/gerenciador/repository
  - src/main/java/br/gov/df/cgdf/gerenciador/dao
  - src/main/java/br/gov/df/cgdf/gerenciador/config/MongoConfiguration.java
  - src/main/java/br/gov/df/cgdf/gerenciador/config/PersistenceConfiguration.java
  - src/main/resources/application.properties
---
# Banco e persistência

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Mapear os bancos usados, as tabelas por esquema e como o código as acessa.

## Evidências
Anotações `@Table`/`@Document` das entidades, repositórios Spring Data, SQL dos DAOs/serviços e `application.properties`.

## Informações confirmadas
**SQL Server** — banco `DB_PRT_TRANSPARENCIA` (mesmo nome em `dev`, `homolog` e `prod`; hosts e usuários omitidos). Pool Hikari `GerenciadorHikariCP`, máximo de 4 conexões, `connection-timeout` 60s, `max-lifetime` 300s. Não há `spring.jpa.hibernate.ddl-auto` definido e **não há Flyway nem Liquibase**: o esquema não é gerenciado por este repositório.

| Esquema.Tabela | Acesso | Usado por |
|---|---|---|
| `Servidor.Relatorio` | JPA (`Arquivo`) + DAO | arquivos |
| `Servidor.Categoria_Relatorio` / `Servidor.CategoriaRelatorio` | JPA (`Categoria`) / SQL em `CategoriaService` | arquivos |
| `Portal.TD_TEMPO`, `Portal.TD_REFERENCIA_TEMPO` | JPA + DAO | períodos e anos de referência |
| `Portal.Imagem_Pagina_Portal`, `Portal.Imagem_Background_Painel` | JPA + DAO | imagens |
| `Despesa.TD_FUNCAO` | DAO (leitura) | função do painel |
| `Portal.TB_CATEGORIA`, `Portal.TB_SUBCATEGORIA` | DAO / JPA (`TextoConsultaPortal`) | textos das consultas |
| `Portal.Orgaos_LAI` | JPA | órgãos da LAI |
| `Servidor.TB_MEDIDA_PROTETIVA` | JPA + DAO | medida protetiva |
| `arquivo.LOG_ARQUIVOS` | JPA (`Log`) | auditoria |
| `Carga.Controle` | `JdbcTemplate` (leitura) | cargas |
| `Remuneracao.Principal`, `Servidor.Principal`, `Despesa.TD_CREDOR`, `Expulsao.Principal`, `Prestando_Contas.Orgao_Deliberativo` | `JdbcTemplate` (leitura) | busca de pessoas |

**MongoDB** — coleção `indices` (`PalavraChave`), autenticação por usuário/senha configurados; `MongoConfiguration` monta uma URI `mongodb://` com usuário, senha, host e porta concatenados e usa um `DefaultMongoTypeMapper(null)` (sem o campo `_class`). Banco, host e porta vêm de `spring.data.mongodb.*`.

## Falhas e dependências
- ✅ `spring.jpa.show-sql=true` e `format_sql` ficam ativos em todos os perfis (SQL no log); Hikari em `DEBUG`/`TRACE` no `application.properties`.
- ✅ `PersistenceConfiguration` está comentada por inteiro (configuração antiga com URL, usuário e senha em texto, **no comentário**; valores não registrados aqui).
- ✅ Dois drivers SQL Server no classpath (`mssql-jdbc` 6.2.2 e `jtds` 1.3.1); o código não escolhe explicitamente.
- 🔶 `spring.datasource.hikari.maximum-pool-size=4` com até 100 threads do Tomcat (`server.tomcat.max-threads=100`) pode causar fila por conexão sob carga; não medido.
- ✅ `Portal.TD_TEMPO` é mapeada por duas entidades (`AnoReferencia`, `Referencia`).
- ✅ Concatenação de SQL em DAOs e serviços: [[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos]].

## Inferências e limitações
- 🔶 O banco `DB_PRT_TRANSPARENCIA` é compartilhado com o backend do Portal-Transparencia (mesmo nome e esquemas `Servidor`/`Carga`); não há migração aqui, então o esquema pertence a outro processo (ver [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco do Portal]]).
- ❓ Privilégios do usuário de banco (leitura/escrita por esquema).

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SQL-Server|Integração com o SQL Server]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|MongoDB]] · [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Modelo-de-Dominio|Modelo de domínio]]

## Pendências e próximo passo
- Obter o DDL das tabelas e os privilégios do usuário da aplicação.
