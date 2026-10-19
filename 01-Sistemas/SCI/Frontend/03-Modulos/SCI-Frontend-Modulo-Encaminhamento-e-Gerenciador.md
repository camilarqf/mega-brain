---
type: module
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - modulo
  - encaminhamento
  - gerenciador
sources:
  - src/app/pages/encaminhados
  - src/app/pages/gerenciador
  - src/app/store/services/encaminhamento.service.ts
  - src/app/store/services/processos-pessoa.service.ts
  - src/app/store/effects/processo-pessoa.effects.ts
---
# SCI Frontend — módulo Encaminhamento e Gerenciador

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Documentar a tela de encaminhados (processos enviados a outras unidades) e o gerenciador de processos por pessoa.

## Evidências
- `pages/encaminhados` (`encaminhados`, `encaminhamento-visualizar`), `pages/gerenciador/gerenciador-processos`, `encaminhamento.service.ts`, `processos-pessoa.service.ts`.

## Informações confirmadas
### Encaminhados (`/pages/encaminhados`)
- ✅ Três listas paginadas (15 por página): **recebidos** (`GET encaminhamento/recebidos`), **enviados pela unidade** (`enviados-pela-unidade`) e **devolvidos** (`devolvidos`); detalhe em `visualizar/:idProcesso` (`por-processo-admissibilidade`).
- ✅ Ações: aceitar (`POST encaminhamento/aceitar`), reprovar com motivo (`reprovar`), devolver (`devolver`), rejeitar devolução com motivo (`rejeitar-devolucao`) e enviar (`enviar`). O envio inicial a partir da nota técnica usa `POST encaminhamento`.
- ✅ O componente aceita resposta paginada ou lista simples (normaliza).
- ✅ A rota é protegida só por autenticação; o menu mostra o item apenas à Autoridade Correcional.

### Gerenciador (`/pages/gerenciador/buscar-processos`; Autoridade e Gestor Admissibilidade)
- ✅ Campo de nome → `GET pessoa/processos?key=` (via NgRx `processo-pessoa`) e lista de processos; cada processo abre um modal com o processo de admissibilidade e a demanda associada.
- ✅ Tipos de processo: `ProcessoAdmissibilidade` (1) e `ProcessoInvestigativoPreliminar` (2); tipos de envolvido: agente público, ente privado, não identificado.

## Inferências e limitações
- ❓ O backend analisado não possui `GET pessoa/processos` (ver [[01-Sistemas/SCI/Frontend/04-API-e-Integracoes/SCI-Frontend-Chamadas-de-API|Chamadas de API]]).
- 🔶 O significado de "reprovar", "devolver" e "rejeitar devolução" vem dos nomes dos endpoints e dos modais; as regras de transição estão no backend ([[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Encaminhamento|módulo do backend]]).

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/03-Modulos/SCI-Frontend-Modulo-JAD-Admissibilidade|JAD]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
