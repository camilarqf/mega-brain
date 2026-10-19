---
type: business-rule
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - keycloak-cgdf
  - regra
  - usuario
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
---
# Regra: normalização do usuário local

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Objetivo
Documentar o estado em que o usuário local fica após cada login pelo IBS.

## Evidências
- `IbsAuthenticator.normalizeUserForDirectGrant`, `clearRequiredActions`, `updateUser`.

## Informações confirmadas
- ✅ **Condição:** login aprovado pelo IBS com `idUsuario`.
- ✅ **Efeito sobre o usuário (novo ou existente):** `enabled = true`, `emailVerified = true`, todas as required actions removidas (inclui `UPDATE_PASSWORD`, `UPDATE_PROFILE`, `VERIFY_PROFILE`, `VERIFY_EMAIL`, `CONFIGURE_TOTP`).
- ✅ **Efeito sobre a sessão de autenticação:** as mesmas required actions são removidas, para o Direct Grant não ser interrompido.
- ✅ **Dados pessoais:** `firstName` = `nomePessoa` (ou o login informado), `lastName` = `-`; os demais campos são sobrescritos a cada login ([[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]]).

## Inferências e limitações
- 🔶 Um usuário desabilitado manualmente no Keycloak é reabilitado no próximo login aprovado pelo IBS, pois `enabled` é forçado; a regra de desativação passa a depender do IBS. Não há teste desse caso.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Confirmar se o bloqueio de usuário deve ser feito apenas no IBS.
