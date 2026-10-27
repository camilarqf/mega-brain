---
type: flow
system: SICI
repository: sici-frontend
status: confirmado
coverage: completa
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - fluxo
  - autenticacao
  - login
sources:
  - src/app/auth/login/login.component.ts
  - src/core/services/auth/auth.service.ts
  - src/core/services/auth/auth.guard.ts
  - src/core/services/auth/role.guard.ts
  - src/core/services/interceptor/http-token.service.ts
  - src/core/services/interceptor/auth-error.interceptor.ts
  - src/app/components/layout/barra-superior/barra-superior.component.ts
---

# Fluxo — autenticação (frontend)

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]], [[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao do Backend]], [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]]

## Objetivo
Descrever a sequência de login, restauração de sessão, autorização de rotas e logout no frontend.

## Evidências
Arquivos em `sources`. Contrato do backend em [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catalogo-de-Endpoints]] (`/auth/login`, `/auth/account`, `/me`).

## Informações confirmadas ✅
### Login
```mermaid
sequenceDiagram
    participant U as Usuário
    participant L as LoginComponent
    participant A as AuthService
    participant B as sici-backend
    U->>L: usuário e senha (ambos obrigatórios)
    L->>A: login(usuario, senha)
    A->>B: POST /auth/login {username, password} (sem Bearer)
    B-->>A: access_token (+ campos não usados)
    A->>A: guarda token (sessionStorage + localStorage), agenda logout em exp
    A->>B: GET /me (força recarga, timeout 5 s)
    B-->>A: roles
    A->>B: GET /auth/account
    B-->>A: dados da conta
    A->>A: persiste conta e perfis, despacha authProfile no NgRx
    L->>U: navega para /pages/home
```
- Erro no login: `401` vira "Credenciais inválidas."; qualquer outro erro vira "Não foi possível autenticar no momento." (`AuthErrorInterceptor`).
- Se `/me` falhar ou expirar, `AuthService` mantém os perfis em cache; os perfis iniciais vêm das claims do JWT.

### Restauração e guarda de rotas
1. Ao iniciar, `AuthService` lê token, conta e perfis do armazenamento e reidrata o estado (`authProfile`).
2. `AuthGuard` em `pages`: sem token válido (inexistente ou expirado) → `/login`.
3. `GuardPerfil` nas rotas com `permissions`: garante os perfis carregados (`ensureRolesLoaded`) e confere `PermissionProfiles`; sem permissão → `/acesso-negado`.
4. Cada requisição ao backend recebe `Authorization: Bearer` (`HttpTokenService`).

### Fim da sessão
- Logout manual (barra superior): limpa chaves, zera o estado, despacha `authClear` e navega para `/login`.
- Expiração do JWT: temporizador chama `logout` e vai ao login.
- Resposta `401` em qualquer chamada (exceto login): `logout(false)` e navegação para `/login`.

## Inferências e limitações
- 🔶 A tela de login não recebe nem guarda a URL pretendida: após login sempre vai a `/pages/home`.
- 🔶 Sem renovação de token (ver [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]): a sessão dura o tempo de vida do `access_token`.
- Fluxo não executado.

## Relacionamentos
- Módulos que dependem dos perfis: [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Ordem-de-Servico|Ordem-de-Servico]], [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Gestao-SUBCI-e-Perfis|Gestao-SUBCI-e-Perfis]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
