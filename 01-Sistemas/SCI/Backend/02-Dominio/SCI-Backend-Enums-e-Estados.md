---
type: domain
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: completa
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
updated: 2026-10-23
tags:
  - sci
  - backend
  - enums
  - estados
sources:
  - src/SCI.Domain/GestaoAdmissibilidade/Enums
  - src/SCI.Domain/GestaoPIP/Enums
  - src/SCI.Domain/GestaoProcessual/Enums
  - src/SCI.Domain/Identidade/Enums/PerfilEnum.cs
  - src/SCI.Domain/Organizacional/Enums
---
# SCI Backend — enums e estados

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Listar os enums do domínio e os estados (siglas) de cada processo. Os valores textuais vêm do atributo `[Description]`.

## Evidências
- Arquivos listados em `sources`. Todos os enums de `SCI.Domain` foram lidos.

## Informações confirmadas
### Denúncia (`StatusAnaliseDenunciaEnum`)
A denúncia **não tem mais status próprio**: o estado vem da `AnaliseDenuncia` — sem análise = pendente; `Aceita` (2) ou `Recusada` (3); `Unknown` (1). Origem: `OrigemDenunciaEnum` = `ParticipaDf`. Nas consultas, o filtro de status usa o id `0` como "pendente" (sem análise).

**Histórico**: até `8e3c8648`, `StatusDenunciaEnum` com `AA` Aguardando análise → `AC` Aceita | `RE` Recusada, coluna `ID_STATUS_DENUNCIA` (seed com ids 0–3); renomeado e substituído em `29989114`.

### Demanda (`StatusDemandaEnum`)
`AA` Aguardando análise · `EA` Em análise · `CPA` Concluída – Processo Admissibilidade · `CM` Concluída – MPTCE · `CPAM` Concluída – ambos · `CR` Criada (demanda gerada por denúncia, ainda incompleta; passa a `AA` quando os dados obrigatórios são preenchidos). Tratamento (`TipoTratamentoDemanda`): EncaminharProcessoAdmissibilidade, EncaminharMPTCE, EncaminharAmbos, e as variantes "…E Distribuir". `TipoDemandante`: Anonimo, Identificado.

### Processo de Admissibilidade (`StatusProcessoAdmissibilidadeEnum`)
| Sigla | Estado |
|---|---|
| `AD` | Aguardando distribuição |
| `AC` / `EC` | Aguardando cadastro / Em cadastro |
| `AA` / `EA` | Aguardando análise / Em análise |
| `ERR` / `ERG` / `ERA` | Em revisão – Revisor / Gestor / Autoridade |
| `AAAN` / `AARE` / `AAG` / `AAAU` | Aguardando assinatura – Analista / Revisor / Gestor / Autoridade |
| `AF` | Aguardando finalização |
| `AE` | Aguardando encaminhamento |
| `PC` | Processo concluído |
| `FES` | Finalizado – encaminhado via SEI |

Análise (`StatusAnaliseAdmissibilidadeEnum`): AI, EA, ER, AP, RE, NTI (nota técnica invalidada). Nota (`StatusNotaAdmissibilidadeEnum`): Criada, Aceita, Recusada. Revisão: `TipoRevisaoAdmissibilidade` = Preliminar, Admissibilidade, Tecnica; `StatusRevisaoAdmissibilidade` = EmAndamento, Reprovada, NaoAdmitida, Admitida.

### Encaminhamento (`StatusEncaminhamentoEnum`)
`AA` Aguardando envio · `EO` Aguardando ciência da autoridade · `AD` Aguardando decisão da devolução · `RE` Reprovado · `AP` Aprovado.

### PIP (`StatusPipEnum`)
Aguardando designação dos investigadores · `ACM` Aguardando conclusão da minuta · `ADA` Aguardando despacho da autoridade · `ARS` Aguardando registro no SEI · `EC` Em cadastro · `EA` Em análise · `ERR`/`ERG`/`ERA` Em revisão (revisor/gestor/autoridade) · `AAI`/`AAR`/`AAG`/`AAA` Aguardando assinatura (investigador/revisor/gestor/autoridade) · `AF` Aguardando finalização · `PC` Processo concluído · `FES` Finalizado – encaminhado via SEI.
Análise do PIP (`StatusAnalisePipEnum`): AI, EA, ER, AP, RE. Revisão do PIP: `TipoRevisaoPip` = Preliminar, Tecnica, Final.

### Processo / recomendação
- `TipoProcessoEnum`: ProcessoAdmissibilidade, ProcessoInvestigativoPreliminar.
- `RecomendacaoEnum` (13 valores): ROO, TCE, SPA, SIN, PIP, IPF, PAD, REF, DMC, TAC, PCT, RCG, ARQ (descrições no arquivo `RecomendacaoEnum.cs`).
- `TipoEnvolvido`: AgentePublico, EntePrivado, NaoIdentificado. `TipoAgente`: AgentePublico, AgentePrivado, Ambos, Nenhum. `TipoRelatoria`: Indefinida, Individual, Comissao.

### Organizacional e identidade
- `PerfilEnum` (11): Administrador (-1), AutoridadeCorrecional, AnalistaAdmissibilidade, GestorAdmissibilidade, ApoioCorrecional, InvestigadorPip, RevisorPip, RevisorJad, GestorPip, GestorGerencial, AssessorAutoridade.
- `TipoDocumentoEnum`: NotaTecnica, Minuta, Relatorio_Pip. `TipoUnidadeEnum`: Orgao, Subsecretaria, Coordenacao. `TipoVinculoUnidadeEnum`: SEI, SIGRH, SIGGO, PARTICIPA_DF.

## Inferências e limitações
- 🔶 "JAD" aparece em nomes (`RevisorJad`, políticas `jad.*`, rotas `reabrir-jad`) e parece designar o processo de admissibilidade; a expansão não consta no código.
- 🔶 Siglas ROO, SPA, IPF, PAD, REF, DMC, TAC, PCT, RCG: ver as descrições; não há expansão adicional no código.
- Há tabelas de status em banco (`TB_STATUS_*`) populadas por scripts; os valores dos seeds não foram lidos.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Glossario|Glossário]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo denúncia → admissibilidade]]

## Pendências e próximo passo
- Confirmar expansão de "JAD" e das siglas de recomendação com o time.
