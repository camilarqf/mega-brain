---
type: integration
aliases:
  - "Integração Gerenciador-Portal → SQL Server do Portal"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
consumer: Gerenciador-Portal
provider: SQL-Server-Portal
sources:
  - pom.xml
  - src/main/resources/application.properties
  - src/main/java/br/gov/df/cgdf/gerenciador/dao
  - src/main/java/br/gov/df/cgdf/gerenciador/repository
---
# Integração Gerenciador-Portal → SQL Server do Portal

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas do Gerenciador-Portal Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Gerenciador-Portal` (`gerenciador-portal-backend`) | `SQL-Server-Portal` (banco `DB_PRT_TRANSPARENCIA`; dono não identificado) | JDBC (`mssql-jdbc` 6.2.2, Hikari) com JPA/Hibernate e `JdbcTemplate` | tabelas dos esquemas `Servidor`, `Portal`, `Carga`, `arquivo`, `Remuneracao`, `Despesa`, `Expulsao`, `Prestando_Contas` | saída (leitura e escrita) |

## Evidências
`spring.datasource.*` por perfil, `application.properties` (Hikari), DAOs, repositórios; tabelas em [[01-Sistemas/Gerenciador-Portal/Backend/02-Dominio/Gerenciador-Portal-Backend-Banco-e-Persistencia|Banco e persistência]].

## Informações confirmadas
- ✅ Um único `DataSource` (Hikari `GerenciadorHikariCP`, até 4 conexões). Escrita nas tabelas de relatório, imagem, texto, órgão LAI, medida protetiva e log; leitura nas demais (cargas, remuneração, credores, expulsões, conselheiros, funções).
- ✅ O nome do banco é `DB_PRT_TRANSPARENCIA` nos três ambientes, em servidores distintos (um por ambiente, hosts omitidos) e com usuários de aplicação diferentes por ambiente.
- ✅ Todo o esquema é externo ao repositório (sem migrations).

## Falhas e dependências
- ✅ Credenciais do banco versionadas, inclusive comentadas nos perfis `dev` e na classe `PersistenceConfiguration` (valores não registrados).
- ✅ SQL por concatenação em ao menos `CargaService`, `ArquivoDAO`, `ServidorDAO`, `ServidorMedidaProtetivaDAO`, `CategoriaService` ([[01-Sistemas/Gerenciador-Portal/Backend/09-Qualidade/Gerenciador-Portal-Backend-Debitos-Tecnicos|Débitos]]).
- ✅ Falha de conexão vira `504` (handler); consulta SQL inválida vira `500`.

## Inferências e limitações
- 🔶 O mesmo banco é usado pelo backend do Portal-Transparencia (mesmo nome de banco e esquemas `Servidor`, `Carga`, `Despesa`); ver [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Banco-e-Migrations|Banco do Portal]]. Fica a pergunta de quem é dono do esquema.
- ❓ Privilégios do usuário por esquema; quem aplica DDL.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Cargas|Cargas]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Medida protetiva]]

## Pendências e próximo passo
- Confirmar o dono do esquema e os privilégios do usuário da aplicação.
