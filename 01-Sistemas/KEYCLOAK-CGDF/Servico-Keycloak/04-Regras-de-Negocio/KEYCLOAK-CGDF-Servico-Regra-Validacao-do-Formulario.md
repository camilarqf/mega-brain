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
  - validacao
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticatorTest.java
---
# Regra: validação do formulário do token endpoint

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-API/KEYCLOAK-CGDF-Servico-Contrato-Token-Endpoint|Contrato-Token-Endpoint]]

## Objetivo
Registrar as condições que o authenticator exige antes de chamar o IBS.

## Evidências
- `IbsAuthenticator.action` e `isNumeric`; teste `campoObrigatorioAusenteRetornaFailureChallengeInvalidGrant`.

## Informações confirmadas
- ✅ **Condição:** `username`, `password` e `idOrgao` presentes (não vazios) e `idOrgao` conversível por `Integer.parseInt`.
- ✅ **Efeito se violada:** HTTP 401 `invalid_grant` ("Credenciais inválidas."), sem chamada ao IBS; o log registra quais campos estavam presentes (nunca a senha).
- ✅ O `idOrgao` é enviado ao IBS como texto, mesmo sendo validado como inteiro.

## Inferências e limitações
- 🔶 Não há validação de tamanho nem de formato de `username`/`password`.
- O teste citado cobre campo ausente; não há teste de `idOrgao` não numérico.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Nenhuma.
