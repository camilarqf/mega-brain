---
type: module
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - modulo
  - subci
  - perfis
sources:
  - src/app/pages/gestao-subci/gestao-subci-cadastrar/gestao-subci-cadastrar.component.ts
  - src/app/pages/gestao-subci/gestao-auditor-perfil/auditor-perfil.component.ts
  - src/app/pages/gestao-subci/gestao-subci-routing.module.ts
  - src/core/services/gestao-subci-service/gestao-subci.service.ts
  - src/core/services/gestao-subci-service/auditor-perfil.service.ts
  - src/core/services/auth/authorization.config.ts
---

# Módulo — Gestão SUBCI e perfis (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Backend: [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-SUBCI-e-Substitutos|SUBCI-e-Substitutos]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Auditores-Coordenadores-Perfis|Auditores-Coordenadores-Perfis]] · Relacionado: [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]

## Objetivo
Área de **Administração** (menu visível a quem tem `EDITAR_PERFIL`, hoje só `SUBCI`): cadastrar o SUBCI titular e seus substitutos e vincular perfis a auditores.

## Evidências
Arquivos em `sources`; leitura dos componentes e serviços.

## Informações confirmadas ✅
- **Gestão do SUBCI** (`gestao-subci`): lista auditores e SUBCIs, identifica o titular (`statusTitular`) e mostra o histórico de substitutos (`GET /subci/{idSubci}/substitutos`).
  - Cadastrar **titular**: abre modal de confirmação com o titular atual; confirmando, envia `POST /subci/cadastrar` (por *action* `cadastrarAuditor` com `statusTitular: true`).
  - Cadastrar **substituto**: envia `POST /subci/{idSubci}/substitutos` com `idAuditorSubstituto`, `dataInicio` e `dataFim`.
  - Nos dois casos, **depois** chama `PUT /auditores/{id}/vincular-perfis` com o perfil de **id fixo `1`** (código na tela, sem consulta ao catálogo de perfis).
- **Auditor ↔ perfil** (`gestao-subci/auditor-perfil`): lista auditores e perfis (`GET /auditor/listar`, `GET /perfis`), mostra auditores **ativos** com seus perfis (`GET /auditores/com-perfil`), permite filtrar por nome, editar o vínculo e salvar (`PUT /auditores/{id}/vincular-perfis` com a lista de ids). Exige ao menos um perfil selecionado.
- **Rotas**: módulo inteiro com `GuardPerfil` e `EDITAR_PERFIL`.

## Inferências e limitações
- 🔶 O perfil de id `1` fixo parece corresponder a SUBCI (para dar acesso ao titular/substituto), mas a correspondência com a tabela de perfis do backend não foi verificada. Se os ids mudarem entre ambientes, a tela vincula o perfil errado.
- 🔶 As duas chamadas (cadastro e vínculo de perfil) são independentes: se a segunda falhar, o auditor fica cadastrado sem o perfil; tratamento de erro não localizado.
- 🔶 O bloqueio por `EDITAR_PERFIL` é só de tela: no backend `POST /subci/cadastrar` e `POST /subci/{id}/substitutos` não têm restrição de perfil (achado S1 em [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]).
- Regras de vigência do substituto (datas) são do backend; o frontend envia as datas escolhidas.

## Relacionamentos
- Quem assina: [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]] · Rotas: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
