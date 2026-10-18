---
type: system
system: SICI
repository: sici-backend
status: pendente
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - sici
  - contexto
  - negocio
---
# SICI — contexto do sistema

Voltar: [[01-Sistemas/SICI/SICI-Index|SICI]]

> ⚠️ **Visão a partir do backend apenas.** A visão de negócio compartilhada continua `pendente` até a análise do `sici-frontend` (ver `BRAIN-RULES.md`). Nada aqui foi deduzido do frontend.

## Objetivo
Resumir, em linguagem de negócio, o que o SICI faz, com base no que está confirmado no código do backend.

## Evidências
- Repositório `sici-backend`, commit `1871e32`. Detalhes e símbolos de código em cada nota linkada abaixo.

## Informações confirmadas
- **Domínio**: apoio ao **controle interno** (auditoria, consultoria e inspeção) — [[01-Sistemas/SICI/Backend/02-Dominio/Enums-e-Estados|Enums e estados]].
- **Planejamento**: ações de controle agrupadas em um plano anual (POAC), ligadas a unidade de auditoria interna, área executora, unidades auditadas e programa/objetivos do PPA — [[01-Sistemas/SICI/Backend/03-Modulos/Acao-de-Controle|Ação de Controle]], [[01-Sistemas/SICI/Backend/03-Modulos/POAC|POAC]].
- **Ordens de Serviço (OS)**: atos formais sobre a ação (abertura, designação, exclusão, prorrogação, substituição de coordenador, cancelamento) e OS genéricas; ciclo criada → enviada → (devolvida) → assinada/cancelada — [[01-Sistemas/SICI/Backend/03-Modulos/Ordem-de-Servico|Ordem de Serviço]], [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Ciclo-de-Vida-OS|Ciclo de vida da OS]].
- **Assinatura eletrônica**: feita pelo SUBCI titular ou substituto vigente; gera número oficial, PDF, QR Code e código verificador — [[01-Sistemas/SICI/Backend/03-Modulos/Assinatura-Digital|Assinatura digital]], [[01-Sistemas/SICI/Backend/03-Modulos/SUBCI-e-Substitutos|SUBCI e substitutos]].
- **Atores e perfis**: auditores autenticados via Keycloak; perfis SUBCI, COORDENADOR, DIRETOR e AUDITOR — [[01-Sistemas/SICI/Backend/03-Modulos/Auditores-Coordenadores-Perfis|Auditores, coordenadores e perfis]], [[01-Sistemas/SICI/Backend/04-Fluxos/Fluxo-Autenticacao|Autenticação]].
- **Termos**: [[01-Sistemas/SICI/Backend/01-Visao-Geral/Glossario|Glossário]].

## Inferências e limitações
- Expansões de siglas (SICI, OSI, POAC, SUBCI, RP/RPM/RM) não constam no código — ver [[01-Sistemas/SICI/Backend/01-Visao-Geral/Glossario|Glossário]].
- Telas, jornadas de usuário e regras validadas só no frontend: **não identificadas**.
- Riscos conhecidos (backend): [[01-Sistemas/SICI/Backend/08-Qualidade/Debitos-Tecnicos|Débitos técnicos e riscos]].

## Relacionamentos
- [[01-Sistemas/SICI/Repositorios|Repositórios]] · [[01-Sistemas/SICI/Backend/00-Backend-Index|Índice do Backend]]

## Pendências e próximo passo
- Revisar e consolidar esta nota depois da análise do `sici-frontend`.
- Confirmar siglas e regras de negócio com o time ([[01-Sistemas/SICI/Backend/99-Controle/Pendencias|Pendências]]).
