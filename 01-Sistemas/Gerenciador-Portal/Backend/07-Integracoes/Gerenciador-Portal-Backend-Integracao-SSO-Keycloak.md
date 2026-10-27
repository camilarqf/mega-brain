---
type: integration
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
consumer: Gerenciador-Portal
provider: Keycloak
tags:
  - gerenciador-portal
  - integracao
  - sso
  - keycloak
  - oidc
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/SsoAuthClient.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/JwtService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/TokenResponse.java
  - src/main/resources/application.properties
  - src/main/resources/application-homolog.properties
  - src/main/resources/application-prod.properties
---
# Integração Gerenciador-Portal → SSO (Keycloak)

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas do Gerenciador-Portal Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Gerenciador-Portal` (`gerenciador-portal-backend`) | `Keycloak` (🔶 instância do [[01-Sistemas/KEYCLOAK-CGDF/KEYCLOAK-CGDF-Index|KEYCLOAK-CGDF]]) | HTTP `POST` form-urlencoded (`RestTemplate`), OIDC token endpoint | `grant_type=password` com `client_id`, `client_secret`, `username`, `password`, `idOrgao`; resposta `TokenResponse` (`access_token`, `refresh_token`, `expires_in`, `refresh_expires_in`, `token_type`, `session_state`, `scope`) | saída |

## Evidências
`SsoAuthClient` (propriedades `so.auth.url`, `so.auth.client-id`, `so.auth.client-secret`, `so.auth.id-orgao`), `JwtService`, `LoginService`.

## Informações confirmadas
- ✅ **Endpoint**: caminho `.../realms/<realm>/protocol/openid-connect/token` (realms `cgdf-realm-sandbox` em `homolog` e `cgdf-realm-production` em `prod`; host omitido). O esquema configurado é `http`.
- ✅ **Cliente OIDC**: `client_id` `gerenciador-portal-client`; o segredo vem de `${SSO_CLIENT_SECRET}` (secret do Swarm `…-gerenciador-portal-transparencia-sso-client-secret-v1`).
- ✅ **`idOrgao`** enviado = `so.auth.id-orgao` (17 nos perfis versionados); a autorização local compara a claim `idOrgao` com `autorizacao.id-orgao` (também 17) e as unidades com `autorizacao.id-unidades` (duas unidades configuradas).
- ✅ **Claims lidas**: `nomePessoa`, `login`, `matricula`, `siglaOrgao`, `idOrgao`, `nomeOrgao`, `autenticado`, `unidades[{idUnidade, siglaUnidade, descricaoUnidade}]`.
- ✅ **Tratamento de erros**: 401 e demais 4xx, 5xx e falha de rede viram `AutenticacaoException`, e o handler responde sempre `401` ([[01-Sistemas/Gerenciador-Portal/Backend/06-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança]]). Não há *timeout*, *retry* nem *circuit breaker* (`RestTemplate` padrão).
- ✅ Desvio: o usuário de desenvolvimento configurado autentica **sem** chamar o SSO.

## Falhas e dependências
- ✅ O JWT é decodificado sem verificar assinatura nem validade (`exp`).
- ✅ Credenciais do usuário trafegam por `http` quando o endpoint é o configurado nos perfis versionados.
- ✅ A indisponibilidade do Keycloak impede o login (exceto o usuário de desenvolvimento).

## Inferências e limitações
- 🔶 Provedor: o caminho `realms/.../openid-connect` e as claims `idOrgao`/`unidades` coincidem com o [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/02-Dominio/KEYCLOAK-CGDF-Servico-Modelo-de-Claims|modelo de claims do KEYCLOAK-CGDF]] (que usa o IBS como origem). O próprio catálogo registra que a identificação da instância do Keycloak veio do usuário, não do código.
- ❓ Escopo do cliente OIDC, expiração do token e se a URL `http` é interna ou termina TLS num proxy.

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/Gerenciador-Portal/Backend/04-Fluxos/Gerenciador-Portal-Backend-Fluxo-Login-e-Autorizacao|Fluxo de login]] · [[01-Sistemas/IBS/IBS-Index|IBS]] (autenticação por trás do Keycloak, 🔶)

## Pendências e próximo passo
- Confirmar a instância do Keycloak e se o tráfego `http` está restrito à rede interna.
