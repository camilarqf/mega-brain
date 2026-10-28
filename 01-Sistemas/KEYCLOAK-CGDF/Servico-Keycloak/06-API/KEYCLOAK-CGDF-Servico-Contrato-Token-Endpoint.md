---
type: api
aliases:
  - "Contrato do token endpoint (fluxo IBS)"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - README.md
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/authenticator/IbsAuthenticator.java
  - providers/src/main/java/br/gov/df/cg/ibs/keycloak/mapper/IbsClaimsProtocolMapper.java
  - .jenkins-pipelines/prod.env.yml
---
# Contrato do token endpoint (fluxo IBS)

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/05-Fluxos/KEYCLOAK-CGDF-Servico-Fluxo-Direct-Grant-IBS|Fluxo-Direct-Grant-IBS]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/04-Regras-de-Negocio/KEYCLOAK-CGDF-Servico-Regra-Validacao-do-Formulario|Regra-Validacao-do-Formulario]]

## Objetivo
O repositório não implementa endpoints próprios: usa os do Keycloak. Esta nota documenta o contrato do token endpoint quando o realm usa o fluxo `ibs-authenticator`. Os demais endpoints OIDC são padrão do Keycloak e não são detalhados.

## Evidências
- `README.md` (seção "Requisicao Token"), `IbsAuthenticator`, `IbsClaimsProtocolMapper`, `prod.env.yml` (`KC_HTTP_RELATIVE_PATH`).

## Informações confirmadas
| Item | Valor |
|---|---|
| Endpoint | `POST /realms/{realm}/protocol/openid-connect/token` (em produção, sob o prefixo relativo configurado em `KC_HTTP_RELATIVE_PATH`) |
| Corpo | `application/x-www-form-urlencoded`: `grant_type=password`, `client_id`, `client_secret` (se o client exigir), `username`, `password`, `idOrgao` (inteiro) |
| Sucesso | resposta OIDC padrão; `access_token`/`id_token` com as claims do [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|Modelo-de-Claims]] se o mapper `ibs-claims-protocol-mapper` estiver no client scope |
| Credencial inválida / formulário inválido | HTTP 401, `error=invalid_grant`, `error_description` = mensagem do IBS ou "Credenciais inválidas." |
| Falha técnica | HTTP 500, `error=server_error`, "Servico de autenticacao indisponivel." |

Configuração necessária no Admin Console (README): execution `IBS Authenticator` como `REQUIRED` no fluxo Direct Grant; mapper adicionado ao client scope dedicado com os toggles *access token*, *ID token* e *userinfo*.

## Inferências e limitações
- ❓ Realms, clients, escopos e o fluxo de cada ambiente não estão no repositório.
- 🔶 A mensagem do IBS é repassada ao cliente em `error_description` (commit `a5502d9`, 2026-08-28); conteúdo possível ❓.
- Endpoints de authorization code, userinfo, logout etc. dependem do Keycloak e do tema; não analisados.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/07-Integracoes/KEYCLOAK-CGDF-Servico-Integracao-IBS|Integracao-IBS]]

## Pendências e próximo passo
- Exportar (sem segredos) a configuração do realm para documentar clients e fluxos.
