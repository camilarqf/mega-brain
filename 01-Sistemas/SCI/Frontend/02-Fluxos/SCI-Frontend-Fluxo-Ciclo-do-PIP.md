---
type: flow
system: SCI
component: Frontend
repository: sci-frontend
status: inferido
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - fluxo
  - pip
sources:
  - src/app/pages/pip
  - src/app/core/enums/status-pip-enum.ts
  - src/app/store/services/pip.service.ts
---
# SCI Frontend — fluxo do ciclo do PIP (visão do cliente)

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]] · Visão do backend: [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|Fluxo do backend]]

## Objetivo
Ordenar as telas, perfis e status do PIP como o cliente os apresenta.

## Evidências
- Roteadores de `pages/pip`, `StatusPipEnum`, `pip.service.ts`. Nenhuma execução.

## Informações confirmadas
Sequência pelos status do cliente (a primeira coluna é o status; a segunda, quem age e a tela correspondente):

| Status | Quem age e onde |
|---|---|
| `ACM` Aguardando conclusão da minuta | Apoio: `instaurar/iniciar-despacho-pip` |
| `ADA` Aguardando despacho da Autoridade | Autoridade: `instaurar/visualizar-despacho-pip` (assina a minuta) |
| `ARS` Aguardando registro no SEI | Apoio: `instaurar/registrar-pip-sei` |
| `ADI` Aguardando designação dos investigadores | Gestor Pip: `instaurar/designar-investigadores-pip` (redistribuição: `caixa-entrada/redistribuir-relatoria`) |
| `EC` Em cadastro | Investigador: `editar` (fatos, envolvidos, condutas, evidências) e `diligencia` |
| `EA` Em análise | Investigador: `analisar/:idPip` (matriz, registro, fundamentação, providências adicionais) |
| `ERR`, `ERG`, `ERA` Em revisão | Revisor Pip, Gestor Pip e Autoridade, nas telas de revisão (reprovar ou concluir) |
| `AAI`, `AAR`, `AAG`, `AAA` Aguardando assinatura | Investigador, Revisor, Gestor e Autoridade: `editar/assinar-relatorio-pip` e modais |
| `AF` Aguardando finalização | Autoridade ou Apoio finalizam (`POST pip/finalizar`) |
| `PC` Processo concluído | estado final |

O assessor da autoridade registra nota de análise (`analise-assessor`) sobre o PIP. O PIP nasce de uma análise de admissibilidade (`GET pip/recuperar-admissibilidade/{id}` e `analise-admissibilidade/por-pip`).

## Inferências e limitações
- 🔶 A correspondência status ↔ tela vem de nomes e rotas; não foi lido cada componente para saber a quais status cada botão responde.
- 🔶 A ordem exata (por exemplo, entre `ADI` e `ACM`) segue o backend: [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Ciclo-do-PIP|ciclo do PIP no backend]].
- ❓ Significado de "matriz" e "providências adicionais" não está definido no cliente.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-PIP|Módulo PIP]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
