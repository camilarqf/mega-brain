---
type: persistence
aliases:
  - "Banco de dados e migrations"
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: parcial
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
sources:
  - src/main/resources/sql
  - src/main/resources/changelog-master.xml
  - src/main/resources/changelog
  - src/main/resources/schema-h2.sql
  - src/main/resources/data-h2.sql
  - src/main/resources/data.sql
  - src/main/resources/sqlPosDump07072016.sql
  - src/main/resources/META-INF/persistence.xml
  - src/main/java/br/gov/df/transparencia/util/JdbcUtil.java
  - pom.xml
---
# Banco de dados e migrations

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/Portal-Transparencia/Backend/02-Dominio/Portal-Transparencia-Backend-Modelo-de-Dominio|Modelo-de-Dominio]]

> Sem credenciais, hosts ou usuários.

## Objetivo
Descrever o banco usado, como as consultas são organizadas e o que existe de migrations.

## Evidências
Contagem e leitura por amostragem de `resources/sql` (547 arquivos), `changelog-master.xml` e `changelog/db.changelog-1.0` a `1.11`, `schema-h2.sql`, `data*.sql`, `JdbcUtil.java`, `persistence.xml` (só o nome do banco e o driver) e `pom.xml`.

## Informações confirmadas
- ✅ **SQL Server** (`jdbc:sqlserver`/`jtds`), banco do portal `DB_PRT_TRANSPARENCIA` (nome citado em `persistence.xml` e em 10 referências cruzadas dentro dos `.vm`). A conexão do datasource vem de `spring.datasource.url` por variável de ambiente (Docker Secrets).
- ✅ **Consultas como arquivos Velocity** em `src/main/resources/sql`: 17 pastas por área e 547 arquivos (`despesa` 149, `prestando-contas` 102, `data-atualizacao` 56, `servidor` 52, `receita` 39, `licitacoes-contratos` 37, `patrimonio` 30, `convenio` 23, `remuneracao` 16, `orcamento` 14, `comum` 14, `enquete` 6, `expulsao` 4, `acesso-informacao` 1, `mascaramento` 1, `relatorio` 1, `textos-explicativos` 1) mais `selectCount.vm`.
- ✅ **Schemas SQL referenciados** nas consultas (contagem aproximada de `from`/`join`): `Despesa` (746), `Servidor` (108), `Receita` (46), `Compras` (45), `Patrimonio` (36), `Carga` (31), `Prestando_Contas` (25), `Remuneracao` (24), `Emendas_Fundo_Fundo` (19), `Beneficiario` (19), `Portal` (15), `Contrato` (15), `Sucor` (14), `MilitaresCedidos` (10), `Convenio` (10), `Empresa_Punida` (9), `BolsaAlimentacao` (9), `Integridade` (8), `Emendas_Pix` (8).
- ✅ Leitura predominante: a aplicação consulta tabelas/views de carga. **Escrita** identificada só em `Portal.Registro_Contato` e `Portal.Registro_Pesquisa` (formulários de contato e pesquisa de satisfação). A enquete tem tabelas no changelog (`Enquete_*`) e consultas de leitura em `sql/enquete`, mas `EnqueteService` é um esqueleto (`recuperarResultado` e `salvar` retornam `null`) e não grava nada.
- ✅ Tabela de medidas protetivas lida pelo mascaramento: `[Servidor].[TB_MEDIDA_PROTETIVA]` (colunas `TX_CONSULTA`, `TX_COLUNA`, `TX_IDENTIFICADOR`). Ver [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]].
- ✅ **Liquibase**: `changelog-master.xml` inclui 12 arquivos (`db.changelog-1.0` a `1.11`), autor `Diogo` nos que foram amostrados; criam, por exemplo, `Orgao_Deliberativo` (schema `Prestando_Contas`) e tabelas `CategoriaRelatorio`, `Enquete_Alternativa`, `Enquete_Pergunta`, `Enquete_Voto`, `Principal`, `Relatorio`, `Tabela_Remuneracao`; vários usam `<sql>` cru. Os caminhos nos `include` são `src/main/resources/changelog/...` (execução a partir da raiz do repositório).
- ✅ **Não há** dependência nem plugin do Liquibase no `pom.xml`, e a aplicação não o executa na subida.
- ✅ Arquivos para H2: `schema-h2.sql` (229 linhas; schemas `Servidor`, `Remuneracao`, `Expulsao`, `Empresa`, `Despesa`), `data-h2.sql` (159), `data.sql` (21) e `sqlPosDump07072016.sql` (64). H2 1.4.186 consta no `pom.xml`.

## Inferências e limitações
- 🔶 Os changelogs são mantidos como histórico e aplicados à mão ou por ferramenta externa (por exemplo, a linha de comando do Liquibase) — nenhuma evidência de quem os executa.
- 🔶 Os arquivos H2 parecem herança de testes locais; os testes versionados, porém, usam o contexto completo com SQL Server (ver [[01-Sistemas/Portal-Transparencia/Backend/09-Qualidade/Portal-Transparencia-Backend-Testes-e-Cobertura|Testes-e-Cobertura]]). Uso atual dos arquivos H2 não confirmado.
- ❓ As tabelas/views de carga (`Carga`, `Despesa`, `Servidor`…) não são criadas por este repositório; DDL e processo de carga não identificados.
- ❓ Existência de índices, volume e desempenho das consultas não analisados.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Arquitetura-em-Camadas|Arquitetura-em-Camadas]] · [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]]

## Pendências e próximo passo
- Confirmar quem aplica os changelogs Liquibase e qual é o processo que popula os schemas de carga.
