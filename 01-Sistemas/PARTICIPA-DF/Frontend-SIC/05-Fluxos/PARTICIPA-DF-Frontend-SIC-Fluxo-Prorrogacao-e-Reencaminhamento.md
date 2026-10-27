---
type: flow
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - fluxo
  - prorrogacao
  - reencaminhamento
sources:
  - app/caixa-entrada/detalhamento-pedido-ctrl.js
  - app/caixa-entrada/detalhamento-pedido.html
---

# Frontend SIC — prorrogação de prazo e reencaminhamento

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Origem: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/05-Fluxos/PARTICIPA-DF-Frontend-SIC-Fluxo-Caixa-de-Entrada-e-Detalhamento|Caixa de entrada e detalhamento]]

## Objetivo
Registrar as duas ações administrativas do detalhe do pedido que não geram resposta ao cidadão.

## Evidências
`detalhamentoPedidoCtrl` e `detalhamento-pedido.html`, commit `5518a81`. Regras de prazo do backend: [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Regras-de-Prazo-do-SIC|Regras-de-Prazo-do-SIC]] e [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Regras-de-Prazo-e-Prorrogacao|Regras-de-Prazo-e-Prorrogacao]] (não reconferidas).

## Informações confirmadas

### Prorrogação de prazo (`PRG_PDD`)
1. ✅ O botão **Prorrogar Prazo** (visível com `Acoes.PRG_PDD`) abre o editor (`inicializarEditorProrrogacaoPrazo`), fechando os editores de resposta e de reencaminhamento.
2. ✅ O operador informa a **justificativa** (`prorragacaoPrazo.Justificativa`; nome da variável com erro de grafia no código).
3. ✅ Confirmação "Confirma a prorrogação de prazo do pedido?" → `POST acesso-informacao/pedido/prorrogar-prazo` com `{Justificativa, Pedido}` → fecha o editor e recarrega o detalhe.
4. ✅ **Diferente do front de Ouvidoria**, o SIC não envia quantidade de dias: só a justificativa. 🔶 A quantidade e as condições ficam por conta do backend.

### Reencaminhamento (`RRE_PDD`)
1. ✅ O botão **Reencaminhar** (`Acoes.RRE_PDD`) carrega as unidades candidatas por `POST unidade/ouvidorias-ativas` com `{AtivoModuloSIC: true}` (somente unidades com o módulo SIC ativo).
2. ✅ O operador escolhe `UnidadeDestino` e informa a `Motivacao`.
3. ✅ Confirmação "Confirma o reencaminhamento do pedido?" → `POST acesso-informacao/pedido/reencaminharPedido` com `{UnidadeDestino, Motivacao, Pedido}` → navega para `/caixa-entrada/` (o pedido sai da lista da unidade, 🔶).

## Inferências e limitações
- 🔶 O fluxo de erro depende do `exceptionInterception` (400 → `custom-exception`); não há tratamento específico no controller.
- ❓ Limite de prorrogações, prazos e efeito no `PrazoVigenteTermino` são regras do backend.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/07-Integracoes/PARTICIPA-DF-Frontend-SIC-Chamadas-de-API|Chamadas-de-API]] · Equivalente: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/05-Fluxos/PARTICIPA-DF-Frontend-Ouvidoria-Fluxo-Prorrogacao-de-Prazo|Prorrogação no Frontend Ouvidoria]]

## Pendências e próximo passo
- Confirmar no backend as regras de prorrogação aplicáveis ao SIC e o efeito do reencaminhamento. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
