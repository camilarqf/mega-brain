---
type: persistence
aliases:
  - "Banco de dados e mapeamentos"
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
sources:
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.Shared/Infra/Config/Maps
  - src/OuvDF.ServicoOuvidoria/Infra/Config/Maps
  - src/OuvDF.ServicoInformacaoCidadao/Infra/Config/Maps
  - src/OuvDF.Shared/Infra/Queries/ConsultarBloqueioUsuario/ConsultarBloqueioUsuarioHandler.cs
  - src/OuvDF.Shared/Infra/Queries/ConsultarUsuarioEstaBloqueado/ConsultarUsuarioEstaBloqueadoHandler.cs
---

# Banco de dados e mapeamentos

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Modelo-de-Dominio|Modelo-de-Dominio]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]]

## Objetivo
Descrever como as entidades são gravadas no SQL Server: mapeamentos, esquemas, tabelas, herança e a ausência de migrations. **Não houve conexão com o banco**; tudo vem do código.

## Evidências
Mapas FluentNHibernate (Shared 33 arquivos, Ouvidoria 34, SIC 37) e `Startup.ConfigureServices` (`AddFluentMapping` nos três namespaces), commit `4901ad5`. A conexão (`database-connection-string`) não foi lida.

## Informações confirmadas

### Mecanismo
- ✅ NHibernate 5.3.8 com FluentNHibernate; `ISessionFactory` singleton; mapeamentos por `ClassMap`/`SubclassMap`; muitos com `Not.LazyLoad()`.
- ✅ Sessão fechada ao fim de cada requisição (`DisposeConnection`); transações pelos `TransactionalCommandHandler` (SDK).
- ✅ Consultas em `Infra/Queries` com `QueryOver` (e SQL Server Query Builder do SDK).
- ✅ Cache distribuído no SQL Server: tabela `dbo.TB_DISTRIBUTED_CACHE`.
- ✅ **Não há migrations nem scripts SQL** no repositório (nenhum `.sql` ou pasta de migrations) e nenhuma chamada a `SchemaUpdate`/`hbm2ddl`: o esquema é mantido fora do código.

### Esquemas e convenções de nome
| Módulo | Esquema/prefixo | Exemplos de tabelas |
|---|---|---|
| Shared | `dbo` (explícito em algumas) e `TB_*` | `Usuario`, `PessoaFisica`, `dbo.PessoaJuridica`, `Operador` (OperadorSO), `dbo.TB_OPERADOR_SIC`, `TB_OPERADORWS`, `TB_BLOQUEIO_USUARIO`, `TB_MOTIVACAO_BLOQUEIO_USUARIO`, `TB_HISTORICO_SENHA`, `TB_TOKEN_CANCELADO`, `TB_LOG_AUDITORIA`, `TB_POLITICA`, `TB_POLITICA_USUARIO`, `dbo.TB_MODULO`, `dbo.TB_NECESSIDADE_ESPECIAL`, `TB_RESPONSAVEL_PESSOA_JURIDICA`, `TB_ARQUIVO_CONTA_USUARIO`, `TB_ESTRANGEIRO`, `dbo.TB_UNIDADE_OPERADOR_SIC`, `dbo.TB_LISTA_OBITO_PARTICIPA_DF` |
| Ouvidoria | tabelas **sem prefixo** e algumas `TB_*` | `Manifestacao`, `Tramite`, `Resposta`, `Prazo`, `ProrrogacaoDePrazo`, `Reclassificacao`, `Invalidacao`, `Historico`, `Providencia`, `Complementacao`, `Assunto`, `Classificacao`, `Tema`, `TipoEntrada`, `SituacaoManifestacao`, `RegiaoAdministrativa`, `Formulario`, `Questao`, `TB_LOCAL_FATO`, `TB_METADADOS_MANIFESTACAO`, `TB_SOLICITACAO_AVALIACAO`, `TB_RESULTADO_SOLICITACAO_AVALIACAO`, tabelas de associação (`ClassificacoesToAssuntos`, `ClassificacaoToQuestao`, `SituacaoManifestacaoToQuestao`, `RelLocalizacaoPeriodo`) |
| SIC | esquema `AcessoInformacao` com `TB_*` | `TB_PEDIDO`, `TB_RECURSO`, `TB_RECURSO_PRIMEIRA/SEGUNDA/TERCEIRA_INSTANCIA`, `TB_RESPOSTA`, `TB_SITUACAO_PEDIDO`, `TB_PRORROGACAO_PRAZO`, `TB_NOTIFICACAO_OMISSAO_RESPOSTA`, `TB_DECISAO_*`, `TB_EVENTO_PEDIDO`, `TB_FERIADO`, `TB_FORMULARIO`, `TB_QUESTAO`, `TB_PESQUISA_SATISFACAO`, `TB_VISUALIZACAO_PEDIDO`, `TB_TRAMITE`, `TB_VINCULO_PEDIDO_SEI` (fora do esquema) |

### Padrões de mapeamento
- ✅ **Herança de usuário**: `UsuarioMap : ClassMap<Usuario>` (tabela padrão `Usuario`, `Id` por *identity*); `PessoaFisicaMap`, `PessoaJuridicaMap` e `OperadorWSMap` como `SubclassMap` com `KeyColumn("Id")` (uma tabela por subclasse unida pelo `Id`).
- ✅ **Operador = pessoa física**: `OperadorMap` (`Operador`) usa `Id` atribuído (`Assigned`) e `References(PessoaFisica).Column("Id").ReadOnly()`.
- ✅ **Objetos de valor como componentes**: `Senha` grava `Senha`, `Salt` e `DataAtualizacaoSenha` em colunas da tabela `Usuario`; `Email` grava a coluna `Email`; em `Pedido`, `Texto`, `Prazo` e `PrazoVigente` também são componentes.
- ✅ **Cascatas**: `Usuario` → `Bloqueios` (`AllDeleteOrphan`), `SenhasAnteriores` e `Telefones` (`SaveUpdate`); `Manifestacao` → `Arquivos`, `Tramites`, `AtributosComplementares`, `Historicos`, `Prazos`, `Reclassificacoes` e outros em cascata; `Pedido` → `Eventos`, `Arquivos`, `Respostas`, `Visualizacoes`, `Recursos`.
- ✅ Datas: `DataUltimoLogin` mapeada com tipo `datetime`.
- ✅ Consultas de bloqueio: o usuário está bloqueado quando existe `BloqueioUsuario` com `DataDesbloqueio` nulo (`ConsultarUsuarioEstaBloqueado`); `ConsultarBloqueioUsuario` devolve o último bloqueio ainda sem `DataDesbloqueio`. O desbloqueio pela entidade `BloqueioUsuario` **preserva** a linha (histórico).
- ✅ Tabela de óbitos: `UsuarioFalecido` → `dbo.TB_LISTA_OBITO_PARTICIPA_DF`, usada pelo job de bloqueio (alimentação ❓ externa).

## Inferências e limitações
- 🔶 Nomes de tabela em três convenções (sem prefixo, `TB_*`, `AcessoInformacao.TB_*`) e esquema ora explícito, ora implícito: reflete evolução do banco, que pertence a gestão externa.
- 🔶 `Usuario.IsBloqueado()`/`IsFalecido()` olham a coleção `Bloqueios` inteira (inclusive bloqueios já desbloqueados), enquanto as consultas filtram `DataDesbloqueio == null`: pode haver divergência em quem usa a propriedade.
- 🔶 `TB_VINCULO_PEDIDO_SEI` e `TB_QUESTAO_ALTERNATIVA` do SIC não usam o esquema `AcessoInformacao` no mapa.
- ❓ Chaves estrangeiras, índices, constraints e tipos reais: não há DDL no repositório.
- ❓ Origem e frequência de carga de `TB_LISTA_OBITO_PARTICIPA_DF`.
- ❓ Valor e origem da `database-connection-string` por ambiente.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]] · [[01-Sistemas/PARTICIPA-DF/Backend/02-Dominio/PARTICIPA-DF-Backend-Enums-e-Estados|Enums-e-Estados]]

## Pendências e próximo passo
- Obter o DDL (ou a documentação do banco) com o time para confirmar chaves, índices e dono do esquema.
- Lote 8: registrar a ausência de migrations versionadas como débito.
