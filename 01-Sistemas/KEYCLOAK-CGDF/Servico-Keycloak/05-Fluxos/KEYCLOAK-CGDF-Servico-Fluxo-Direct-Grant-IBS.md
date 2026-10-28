---
type: flow
aliases:
  - "Fluxo Direct Grant com IBS"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: completa
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/client/IbsApiClient.java
  - providers/src/test/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticatorTest.java
---
# Fluxo Direct Grant com IBS

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Arquitetura-SPI|Arquitetura-SPI]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/06-API/KEYCLOAK-CGDF-Servico-Contrato-Token-Endpoint|Contrato-Token-Endpoint]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]]

## Objetivo
Descrever passo a passo o login por *password grant* (Direct Grant) executado por `IbsAuthenticator`.

## Evidências
- `IbsAuthenticator.authenticate` → `action`; `IbsApiClient.login`; testes em `IbsAuthenticatorTest` (7 cenários).

## Informações confirmadas
**Pré-condição (README):** o fluxo Direct Grant do realm contém só o execution `IBS Authenticator` como `REQUIRED`; `Password`, `OTP` e `Condition user configured` ficam `DISABLED`. A configuração do realm não está no repositório.

**Atores:** cliente OIDC (chamador do token endpoint), Keycloak (`IbsAuthenticator`), IBS.

**Passos (`IbsAuthenticator.action`):**
1. Lê `username`, `password` e `idOrgao` do formulário. Se algum estiver vazio, ou `idOrgao` não for inteiro → `invalid_grant` (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Validacao-do-Formulario|Regra-Validacao-do-Formulario]]).
2. Resolve `ibsBaseUrl`, `ibsTimeoutSeconds` e segredo (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]).
3. Chama o IBS: `POST {ibsBaseUrl}/auth` com `login`, `senha`, `idOrgao`.
4. Se o IBS responde sem autenticar (`claims` ausente ou `autenticado` ≠ `true`) → `invalid_grant` 401, com a `message` do IBS ou "Credenciais inválidas.".
5. Se `claims.idUsuario` for vazio → `invalid_grant`; nenhum usuário é criado ([[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Username-Interno-IdUsuario|Regra-Username-Interno-IdUsuario]]).
6. Busca o usuário pelo username = `idUsuario`; se não existe, cria ([[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Normalizacao-do-Usuario|Regra-Normalizacao-do-Usuario]]).
7. Atualiza atributos do usuário com as claims do IBS e grava as notas de sessão ([[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]]); remove required actions da sessão de autenticação.
8. `context.success()`: o Keycloak emite o token; o `IbsClaimsProtocolMapper` acrescenta as claims.

**Saídas de erro:**

| Situação | Resposta ao cliente |
|---|---|
| Formulário inválido, IBS não autenticou, `idUsuario` ausente | HTTP 401, `error=invalid_grant` |
| IBS com HTTP diferente de 200/401, timeout, falha de conexão, resposta inválida, `RuntimeException` | HTTP 500, `error=server_error`, "Servico de autenticacao indisponivel." |

Cobertura de teste (`IbsAuthenticatorTest`): sucesso com notas e `success()`, criação de usuário, username igual ao `idUsuario`, `idUsuario` ausente sem criar usuário, credencial inválida, campo ausente, erro técnico.

## Inferências e limitações
- 🔶 Por leitura do código, um HTTP 401 do IBS com corpo que não seja JSON do contrato lança exceção e cai em `server_error`; não há teste para esse caso.
- Não verificado em execução: este lote é leitura estática.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Pendências e próximo passo
- O 403 do IBS vira erro técnico, ao contrário do que diz o README (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]]).
