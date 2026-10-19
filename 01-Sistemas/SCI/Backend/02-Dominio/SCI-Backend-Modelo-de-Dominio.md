---
type: domain
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
  - dominio
  - entidades
sources:
  - src/SCI.Domain/GestaoAdmissibilidade/Entities
  - src/SCI.Domain/GestaoPIP/Entities
  - src/SCI.Domain/GestaoProcessual/Entities
  - src/SCI.Domain/Organizacional/Entities
  - src/SCI.Domain/Identidade
---
# SCI Backend — modelo de domínio

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Mapear os agregados, entidades e relações do `SCI.Domain`.

## Evidências
- Pastas de `SCI.Domain` por contexto: `GestaoAdmissibilidade`, `GestaoPIP`, `GestaoProcessual`, `Organizacional`, `Identidade`, `EventStore`, `_SharedKernel`. Propriedades lidas por reflexão textual; corpo dos métodos lido só nas entidades de [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|Admissibilidade]] e [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-PIP|PIP]].

## Informações confirmadas
### Hierarquia de processos
- `Processo` (abstrato; `AggregateEventManager`, `IAggregate<int>`): `Sequencial`, `IdentificadorProcessual`, `Fatos`, `Origem` (Unidade), `Relatorias`, `Documentos`, datas de criação/atualização/conclusão/exclusão.
- `ProcessoAdmissibilidade : Processo` (selada): `Status`, `Relator` (Usuario), `ConfiguracaoProcesso`, `DemandaOriginaria`, `Distribuicoes`, `Encaminhamentos`, `NumeroProcessoSei`.
- `PIP : Processo`: `Status`, `ConfiguracaoProcesso`, `ProcessoAdmissibilidadeOriginario`, `AtoCompetenciaAutoridade`, `NumeroProcessoSei`, `DataDodf`.
- Numeração: `Numerar(sequencial, NumeroVinculo)` monta o identificador a partir do vínculo da unidade (`TB_UNIDADE_VINCULADA`) e do ano, com prefixos de `DomainConstants`.

### Entrada
- `Denuncia`: `IdentificadorExterno` (id da denúncia no `PARTICIPA-DF`), `ProtocoloRelacionado`, `Unidade`, `Identificada`, `OrigemDenuncia`, `Status`, `MotivoRecusa`.
- `Demanda`: origem (Unidade), documento de origem (`DocumentoOrigemDemanda`), `Assunto`, `Descricao`, tipo de demandante, período da ocorrência, `TipoAgenteEnvolvido`, `Anexos`, `DocumentosVinculados`, `Status`.

### Análise
- `Fato` (do processo) → `Envolvido` (`AgentePublico`, `EntePrivado`, `EnvolvidoNaoIdentificado`; `Condutas`, `Evidencias`, `ValorVantagemIndevida`) → `Evidencia` (+ `AnexoEvidencia`).
- `AnaliseAdmissibilidade` / `AnalisePip`: `Itens` (cada item com `Tipificacoes`, `Recomendacoes`, `ElementoFaltantes`), `Fundamentacao`, `Notas`, versionamento (`AnaliseAdmissibilidadeOriginaria`, `Versao`).
- `RevisaoAdmissibilidade` / `RevisaoPip` ligadas à análise.
- `Diligencia` (PIP): descrição, data, resultado, `Investigador`, `Envolvido`, `Participantes`, `Anexos`, flag `Vinculada` (matriz).
- `Encaminhamento`: `ProcessoOrigem`, `ProcessoDestino`, `Remetente`/`Destinatario` (Unidade), `Observacao`, `Justificativa`, `Status`.
- `Relatoria` (`TipoRelatoria`), `Distribuicao`, `VigenciaPunitiva`.

### Documentos
- `DocumentoAssinado`: `Processo`, `TipoDocumento`, `ConteudoDocumentoAssinado`, `HashVerificador`, `Assinaturas`, `DocumentoInvalidado`. `Assinatura`: `Usuario`, `Cargo`, `Perfil`, `DataAssinatura`.

### Organizacional e identidade
- `Unidade` (Id texto, `Sigla`, `PossuiEstruturaCorrecional`, `Cargos`, `UnidadesVinculadas`, `ConfiguracoesProcesso`), `ConfiguracaoProcesso` (por `TipoProcesso`) e `ConfiguracaoRevisaoProcesso` (perfil responsável pela revisão), `Servidor`, `Cargo`, `SituacaoFuncional`, `Pessoa` (`PessoaFisica`, `PessoaJuridica`), `Endereco`.
- `Usuario` (CPF, e-mail, matrícula, `Permissoes`, `PermissaoAtual`), `Permissao` (perfil + unidade + `Atual`), `Perfil`. `UsuarioIdentidade` (vínculo com identidade externa) existe como arquivo **não versionado** e fica fora do escopo.
- Value objects: `CPF`, `CNPJ`, `Email`, `NumeroVinculo`, `Periodo`, `Fundamentacao`, `Blob`, `Expediente`, `ObjectID`, `UserIdentity`.

### Base compartilhada (`_SharedKernel`)
`AggregateEventManager`, `IAggregate`, `IRepository`, `IUnitOfWork`, `ISpecification`/`SpecificationRules`, exceções (`InvalidSciOperationException`, `AggregateNotFoundException`, `EntityNotFoundException`, `AuthenticationFailedException`).

## Inferências e limitações
- 🔶 Cardinalidades exatas e constraints estão nos mappings EF ([[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco]]); aqui só a visão do código de domínio.
- Entidades de PIP (participantes, vigência punitiva) e de `GestaoProcessual` lidas só por propriedades.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums e estados]] · [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Arquitetura-CQRS-e-Event-Sourcing|Arquitetura]] · [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Glossario|Glossário]]

## Pendências e próximo passo
- Ler os mappings para confirmar cardinalidades e índices únicos (lote 2).
