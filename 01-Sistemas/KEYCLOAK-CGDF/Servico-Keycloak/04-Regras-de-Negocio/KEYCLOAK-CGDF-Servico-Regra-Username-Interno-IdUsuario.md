---
type: business-rule
aliases:
  - "Regra: username interno = `idUsuario` do IBS"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsLoginResponse.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticatorTest.java
---
# Regra: username interno = `idUsuario` do IBS

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]]

## Objetivo
Documentar como o usuário local é identificado após autenticar no IBS.

## Evidências
- `IbsAuthenticator.action` (verificação de `idUsuario`, `findOrCreateUser`); `IbsLoginResponse` (`idUsuario` da raiz tem precedência sobre `claims.idUsuario`); testes `usernameInternoUsaIdUsuarioRetornadoPeloIbs` e `idUsuarioAusenteRetornaInvalidGrantENaoCriaUsuario`.

## Informações confirmadas
- ✅ **Condição:** o IBS autenticou e devolveu `idUsuario` (raiz da resposta ou dentro de `claims`; o valor da raiz, se não vazio, prevalece).
- ✅ **Efeito:** o username do usuário Keycloak é o `idUsuario` aparado; se o usuário existe com esse username, é reutilizado e atualizado; senão é criado.
- ✅ **Exceção:** `idUsuario` ausente ou vazio → `invalid_grant`, nenhum usuário é criado ou atualizado.
- ✅ O `login` digitado não identifica o usuário; fica no atributo `login`.

## Histórico
- Regra anterior (por mensagem de commit): username interno gerado por hash de login, matrícula e órgão (`33cde3e`, 2026-07-09); substituída por `idUsuario` do IBS em `5c4fe98` (2026-07-17).

## Inferências e limitações
- 🔶 Usuários criados antes de 2026-07-17 podem ter username antigo e coexistir como duplicados; o README orienta remover o usuário antigo para testes. Migração em ambientes reais ❓.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- Confirmar se houve migração dos usuários criados com o username anterior.
