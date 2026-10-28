---
type: module
aliases:
  - "SCI Frontend — módulo JAD (processo de admissibilidade)"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
sources:
  - src/app/pages/jad
  - src/app/store/services/jad.service.ts
  - src/app/store/services/analise.service.ts
  - src/app/store/effects/jad.effects.ts
  - src/app/store/effects/analise.effects.ts
  - src/app/core/enums/status-jad-enum.ts
---
# SCI Frontend — módulo JAD (processo de admissibilidade)

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Documentar as telas do processo de admissibilidade (a sigla JAD aparece nos nomes de rota e de serviço): cadastro, caixas de entrada por perfil, análise, revisão e nota técnica.

## Evidências
- `pages/jad` (`jad-cadastro`, `caixa-entrada-jad`, `jad-analise`), `jad.service.ts` e `analise.service.ts`, efeitos `jad.effects.ts` e `analise.effects.ts`, enum `status-jad-enum.ts`.

## Informações confirmadas
### Cadastro (`/pages/jad/cadastro`)
- ✅ Lista de processos (`jad-list`), visualização e, por processo, o cadastro de **fatos**, **envolvidos** (agente público, pessoa física/jurídica, não identificado; busca de pessoa e servidor), **condutas** e **evidências** (com upload). Envolvidos usam `GET pessoa/pesquisar`, `GET servidor/pesquisar`, `GET pessoa-juridica/pesquisar` e `GET cargo/por-usuario`.
- ✅ Concluir cadastro: `POST processo-admissibilidade/concluir-cadastro-jad`; reabrir: `POST .../reabrir-jad`; atualizar: `PUT processo-admissibilidade`.

### Caixas de entrada (`/pages/jad/caixa-entrada`)
- ✅ Uma caixa por perfil, cada uma com sua visão paginada: gestor, autoridade, assessor da autoridade, apoio, analista e revisor (`GET processo-admissibilidade/visao-*`).
- ✅ Ações: distribuir para analista (`distribuir-para-analista`), redistribuir (`redistribuir-jad`), registrar número SEI (`atualizar-dados-sei`), nota técnica (visualizar, assinar `assinar-nota-tecnica`, invalidar `invalidar-nota-tecnica`), concluir (`concluir`) e encaminhar (`POST encaminhamento`, via `EncaminhamentoService.encaminhar`).
- ✅ Assessor da autoridade: criar, atualizar e concluir **nota de admissibilidade** (`analise-admissibilidade/criar-nota-admissibilidade`, `atualizar-nota-admissibilidade`, `concluir-nota-admissibilidade`).

### Análise e revisão (`/pages/jad/analise/:idJad`)
- ✅ Matriz (`jad-matriz`) de envolvidos × condutas, registro por envolvido com recomendação, fundamentação e conclusão (`PUT analise-admissibilidade`, `POST analise-admissibilidade/concluir`).
- ✅ Revisão: `revisao-admissibilidade/reprovar-revisao`, `concluir-revisao-admissibilidade` e `atualizar-revisao` (rascunho), com telas de revisão preliminar e de análise.
- ✅ Catálogos de apoio: tipificação, recomendação, situação funcional, conduta (cada um no seu `store` e serviço).

### Status do processo no cliente (`StatusJadEnum` / `STATUS_PROCESSO_ADMISSIBILIDADE_OPTIONS`)
`AD` Aguardando distribuição, `AC` Aguardando cadastro, `EC` Em cadastro, `AA` Aguardando análise, `EA` Em análise, `ERG` Em revisão — Gestor, `ERA` Em revisão — Autoridade, `AAAN`/`AAG`/`AAAU`/`AARE` Aguardando assinatura (Analista, Gestor, Autoridade, Revisor), `AF` Aguardando finalização, `PC` Processo concluído, `ERR` Em revisão — Revisor, `AE` Aguardando encaminhamento, `FES` Finalizado — encaminhado via SEI.

### Regras aplicadas no cliente (caixa do gestor, `caixa-entrada-gestor`)
- ✅ Nota técnica disponível nos status `ERG, ERA, AAAN, AAG, AAAU, AARE, AF, PC, ERR, AE, FES`.
- ✅ Redistribuição permitida nos status `AC, EC, AA, EA, ERG, ERA, AAAN, AAG, AAAU, ERR, AARE`.
- ✅ Revisão pelo gestor só no status `ERG`.
- 🔶 São regras de exibição de botão no cliente; a regra efetiva está no backend ([[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Processo-de-Admissibilidade|módulo do backend]]).

## Inferências e limitações
- ❓ Expansão de JAD e de várias siglas (já pendência do backend).
- 🔶 `processo-admissibilidade/encaminhar` existe em `jad.service.ts` mas o fluxo de nota técnica usa `EncaminhamentoService`; uso do método do JAD não verificado, e o endpoint não existe no backend analisado.
- Corpo da maioria dos componentes de análise e revisão não foi lido linha a linha.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Encaminhamento-e-Gerenciador|Encaminhamento e gerenciador]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Assinatura-e-Validacao|Assinatura e validação]] · [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-Denuncia-e-Demanda|Denúncia e demanda]] · [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
