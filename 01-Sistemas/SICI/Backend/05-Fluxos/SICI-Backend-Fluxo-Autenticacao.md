---
type: flow
aliases:
  - "Fluxo — autenticação e autorização"
system: SICI
repository: sici-backend
status: confirmado
coverage: completa
analyzed_commit: 1871e323ebfc26fe75ef8f809af3a2a9e033814a
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - api/config/SecurityConfig.java
  - api/security/AuthController.java
  - api/security/JwtAuthenticationConverterCustom.java
  - api/security/CustomAuthenticationEntryPoint.java
  - api/security/CustomAccessDeniedHandler.java
  - application/service/security/AuthServiceImpl.java
  - application/usecase/security/AutenticarNoKeycloak.java
  - application/usecase/security/BuscarContaNoKeycloak.java
  - infrastructure/external/adapter/KeycloakAuthAdapter.java
  - infrastructure/external/health/KeycloakHealthIndicator.java
---

# Fluxo — autenticação e autorização

Voltar: [[01-Sistemas/SICI/Backend/SICI-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-Auditores-Coordenadores-Perfis|Auditores-Coordenadores-Perfis]], [[01-Sistemas/SICI/Backend/07-Integracoes/SICI-Backend-Integracoes-Externas|Integracoes-Externas]]

## 1. Login (proxy para o Keycloak) ✅

```mermaid
sequenceDiagram
    actor U as Usuário (frontend)
    participant A as AuthController
    participant K as KeycloakAuthAdapter
    participant KC as Keycloak
    U->>A: POST /auth/login {username, password} (público)
    A->>K: autenticar(username, password)
    K->>KC: POST token-uri (form: grant_type=password, client_id, [client_secret], username, password, [scope])
    alt 200
        KC-->>K: access/refresh/id token
        K-->>U: 200 KeycloakTokenResponse
    else 400/401
        K-->>U: 401 "Credenciais inválidas." (BadCredentialsException)
    else outro erro/timeout
        K-->>U: 502 "Não foi possivel autenticar no momento." (AuthenticationServiceException)
    end
```
- Timeouts: connect 5 s / read 10 s (`keycloak.auth.*-timeout-ms`, `RestTemplateBuilder`).
- `/auth/login` é ignorado pelo `BearerTokenResolver` customizado: um header `Authorization` inválido não atrapalha o login.
- ✅ O login **não** confere se o usuário é auditor ativo. Essa checagem ocorre só nas chamadas seguintes (passo 2).
- 🔶 Sem limite de tentativas no backend. A proteção contra força bruta depende da configuração do realm no Keycloak.

## 2. Cada requisição autenticada ✅

```mermaid
flowchart TD
    R["Request + Authorization: Bearer JWT"] --> V{"Resource Server valida<br/>assinatura/emissor (issuer-uri)"}
    V -- inválido/expirado --> E401["401 JSON<br/>code TOKEN_EXPIRED ou UNAUTHORIZED<br/>(CustomAuthenticationEntryPoint)"]
    V -- válido --> C["JwtAuthenticationConverterCustom<br/>username = claim preferred_username"]
    C --> S{"username em security.super-users?"}
    S -- sim --> SU["authorities = [ROLE_SUPER_USUARIO]"]
    S -- não --> DB{"TB_AUDITOR: login ativo?<br/>(buscarPorLoginAtivo)"}
    DB -- não --> E401b["BadCredentialsException → 401"]
    DB -- sim --> RO["authorities = ROLE_ + perfis do auditor<br/>(maiúsculas, espaços → _)"]
    RO --> P{"@PreAuthorize do endpoint?"}
    SU --> P
    P -- sem anotação --> OK["executa"]
    P -- role ok --> OK
    P -- role ausente --> E403["403 JSON (CustomAccessDeniedHandler<br/>ou GlobalExceptionHandler)"]
```

- ✅ As roles vêm **do banco a cada requisição**, não do token. Mudar perfis tem efeito imediato.
- ✅ `ROLE_SUPER_USUARIO` não aparece em **nenhum** `@PreAuthorize`. O super-usuário passa na autenticação mesmo sem cadastro em `TB_AUDITOR`, mas leva 403 em todos os endpoints com role. Na prática, acessa só os endpoints sem anotação, que são a maioria (ver [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]]).
- ✅ Assinar OS **não depende de role**: depende de o login ser o do SUBCI titular ou do substituto vigente ([[01-Sistemas/SICI/Backend/03-Modulos/SICI-Backend-Modulo-SUBCI-e-Substitutos|SUBCI-e-Substitutos]]).

## 3. Conta e sessão ✅
- `GET /auth/account`: repassa o access token ao **userinfo** do Keycloak e devolve os dados da conta (`DadosUsuarioAutenticado`).
- `GET /me`: devolve `username` e `roles` calculados pela aplicação.
- Não há endpoint de refresh nem de logout no backend. 🔶 O frontend provavelmente usa o refresh token devolvido no login direto com o Keycloak.

## 4. Healthcheck ✅
`KeycloakHealthIndicator` consulta `/.well-known/openid-configuration` (derivado do token-uri) a cada chamada de `/healthcheck`.
- 🔶 O Dockerfile chama `/healthcheck` a cada 30 s. Se o Keycloak cair, o container fica **unhealthy** e o orquestrador pode reiniciá-lo, propagando a indisponibilidade do Keycloak para a API.
