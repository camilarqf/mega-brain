---
type: reference
aliases:
  - "SCI Backend — glossário"
system: SCI
component: Backend
repository: sci-backend
status: inferido
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
updated: 2026-10-23
sources:
  - src/SCI.Domain
---
# SCI Backend — glossário

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Termos do código e seu significado **conforme o uso no código**. Expansões de siglas não presentes no código ficam como 🔶 ou ❓.

## Evidências
- Nomes de tipos, enums, políticas e rotas em `src/SCI.Domain` e `src/SCI.Api`.

## Informações confirmadas
| Termo | Significado (evidência) |
|---|---|
| Denúncia | registro recebido do `PARTICIPA-DF`; pendente até receber uma `AnaliseDenuncia` (aceita ou recusada); ao ser aceita gera uma demanda — `Denuncia` |
| Demanda | solicitação a tratar (cadastrada à mão ou gerada por denúncia aceita, caso em que nasce `CR` — Criada); pode gerar Processo de Admissibilidade e/ou ser encaminhada ao MPTCE — `TipoTratamentoDemanda` |
| Processo de Admissibilidade | processo que analisa a demanda e produz a nota técnica — `ProcessoAdmissibilidade` |
| PIP | processo (investigativo preliminar) aberto a partir de um processo de admissibilidade — `TipoProcessoEnum.ProcessoInvestigativoPreliminar`, `PIP` |
| Nota técnica | documento assinado do processo de admissibilidade — `TipoDocumentoEnum.NotaTecnica` |
| Minuta | documento do PIP (ato de instauração) assinado pela autoridade — `TipoDocumentoEnum.Minuta` |
| Relatório do PIP | documento final assinado em cadeia — `TipoDocumentoEnum.Relatorio_Pip` |
| Tipificação, Recomendação, Elemento faltante | componentes de cada item da análise |
| Envolvido, Fato, Evidência, Conduta | estrutura factual do processo |
| Relatoria / Relator | responsável(is) pelo processo; PIP exige ao menos um relator para designar |
| Diligência (matriz) | ato investigativo do PIP; pode ser vinculada/desvinculada à "matriz" |
| Encaminhamento | envio do processo de admissibilidade a outra unidade |
| Unidade vinculada | identificador da unidade em outro sistema: SEI, SIGRH, SIGGO ou PARTICIPA_DF |
| Configuração de processo | define, por unidade e tipo de processo, as revisões (perfis) do fluxo |
| Permissão atual | par perfil + unidade ativo do usuário, usado no token |

## Inferências e limitações
- 🔶 JAD: aparece em `RevisorJad`, políticas `jad.*` e rotas; provável sinônimo de processo de admissibilidade.
- 🔶 SEI: sistema externo de processos; no SCI só o número do processo é registrado (`NumeroProcessoSei`).
- 🔶 MPTCE: destino alternativo de uma demanda (nome em `StatusDemandaEnum`).
- ❓ DODF (`DataDodf` no PIP), SIGRH, SIGGO, SCI: sem expansão no código.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Enums-e-Estados|Enums e estados]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Modelo-de-Dominio|Modelo de domínio]]

## Pendências e próximo passo
- Confirmar expansões com o time (ver [[01-Sistemas/SCI/Backend/99-Controle/SCI-Backend-Pendencias|Pendências]]).
