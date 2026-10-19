---
type: persistence
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - banco
  - sql-server
  - migrations
sources:
  - src/SCI.Infrastructure.Data/Contexts
  - src/SCI.Infrastructure.Data/Support/DatabaseOperation.cs
  - src/SCI.Infrastructure.Data/Support/SqlScripts
  - src/SCI.Infrastructure.Data/_SharedKernel
  - src/SCI.Api/Controllers/SupportController.cs
  - src/SCI.Infrastructure.Projections
---
# SCI Backend — banco de dados e criação do esquema

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Descrever os contextos EF, as tabelas, a leitura por Dapper e o mecanismo de criação do banco (sem migrations EF).

## Evidências
- `src/SCI.Infrastructure.Data/Extensions/ServiceCollectionsExtensions.cs`, `Support/DatabaseOperation.cs`, `Support/SqlScripts/*.sql` (nomes lidos; conteúdo dos seeds **não lido**).

## Informações confirmadas
- ✅ **SQL Server**, dois contextos EF: `DefaultDbContext` (58 mappings em `Contexts/Default/Mappings`) e `EventStoreDbContext` (tabela `TB_EVENTO`, mapping `EventMapping`). Ambos usam `EnableRetryOnFailure` e, se `PoolSize > 0`, `AddDbContextPool`.
- ✅ **Tabelas mapeadas** (`ToTable`), por grupo: processos (`TB_PROCESSO`, `TB_PROCESSO_ADMISSIBILIDADE`, `TB_PROCESSO_INVESTIGATIVO_PRELIMINAR`), entrada (`TB_DENUNCIA`, `TB_DEMANDA`, `TB_ORIGEM_DENUNCIA`, anexos), análise (`TB_ANALISE_*`, `TB_ITEM_ANALISE_*` e tabelas de associação com tipificação, recomendação e elemento faltante, `TB_NOTA_*`, `TB_REVISAO_*`), fatos (`TB_FATO`, `TB_ENVOLVIDO*`, `TB_EVIDENCIA`, `TB_AGENTE_PUBLICO`, `TB_ENTE_PRIVADO`, `TB_CONTRATO_FIRMADO`), PIP (`TB_DILIGENCIA`, `TB_PARTICIPANTE`, `TB_VIGENCIA_PUNITIVA`, `TB_RELATORIA*`, `TB_DISTRIBUICAO`), documentos (`TB_DOCUMENTO_ASSINADO`, `TB_CONTEUDO_DOCUMENTO_ASSINADO`, `TB_ASSINATURA`, `TB_DOCUMENTO_INVALIDO`, `TB_DOCUMENTO_VINCULADO`), organizacional (`TB_UNIDADE`, `TB_UNIDADE_VINCULADA`, `TB_CONFIGURACAO_PROCESSO`, `TB_CONFIGURACAO_REVISAO_PROCESSO`, `TB_CARGO`, `TB_SERVIDOR`, `TB_SITUACAO_FUNCIONAL`, `TB_PESSOA*`, `TB_ENDERECO`), identidade (`TB_USUARIO`, `TB_PERFIL`, `TB_PERMISSAO`) e tabelas de status/tipo (`TB_STATUS_*`, `TB_TIPO_*`).
- ✅ **Conversores de valor**: `CPFConverter`, `CNPJConverter`, `EmailConverter`, `BlobConverter`. `EntityLifeCicleMapping` mapeia as datas de criação, atualização, conclusão e exclusão (exclusão lógica por `DataExclusao`).
- ✅ **Sem migrations EF.** O esquema é gerado por `Database.GenerateCreateScript()` dos dois contextos.
- ✅ **`DatabaseOperation.GenerateDatabase`** (chamada por `POST /support/generate-database`): se `CreateDatabase` (padrão `true`) executa `00-Remove-All-Tables.sql` (remove **todas** as FKs e tabelas do schema `dbo`), cria o esquema e depois roda em ordem alfabética os scripts `*.sql` (exceto o `00`, e os de `IgnoredFiles`). Scripts presentes: `01` a `25` (inserções de domínio: assuntos, tipos, condutas, unidades, usuários, recomendações, tipificações, status, fluxos de configuração) e `26` (tabela de identidade da POC; fora do escopo).
- ✅ **Proteção do endpoint**: `[FeatureGate(SupportFeatures.GenerateDatabase)]`, flag `Support.GenerateDatabase` = `false` em `appsettings.json`; o controller é `[AllowAnonymous]`.
- ✅ **Leitura (read model)**: `ReadModelConnection` com `ReadModelDatabaseSettings.ConnectionStringName`; consultas SQL em `Queries/<Área>/…` embutidas como recurso, executadas pelo `Processor`.
- ✅ **Auditoria**: `TB_EVENTO` registra cada evento de domínio ([[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Arquitetura-CQRS-e-Event-Sourcing|Arquitetura]]).

## Inferências e limitações
- 🔶 Como não há migrations, a evolução do esquema em ambientes existentes depende de scripts manuais; o processo não está no repositório. Os valores de `.jenkins-pipelines/*.env.yml` não foram lidos para verificar a flag por ambiente.
- Conteúdo dos seeds (`01`–`25`) não lido por conter potencialmente dados de pessoas (`05-Insert-TB_USUARIO.sql`, `10-Insert-TB_SERVIDOR.sql`).
- Cardinalidades e índices únicos dos mappings não detalhados (cobertura parcial).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/SCI/Backend/06-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança]]

## Pendências e próximo passo
- Usuário informou (2026-10-19) que o endpoint só funciona em dev e local; confirmar o mecanismo no código/pipeline.
