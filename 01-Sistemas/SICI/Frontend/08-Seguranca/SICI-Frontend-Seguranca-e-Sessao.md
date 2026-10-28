---
type: security
aliases:
  - "Segurança e sessão — SICI Frontend"
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - src/core/services/auth/auth.service.ts
  - src/core/services/auth/auth.guard.ts
  - src/core/services/auth/role.guard.ts
  - src/core/services/auth/authorization.config.ts
  - src/core/services/interceptor/permission.service.ts
  - src/core/services/interceptor/http-token.service.ts
  - src/core/services/interceptor/auth-error.interceptor.ts
  - src/core/services/assinatura-popup-context.service.ts
  - src/core/services/keycloak/keycloak.service.ts
  - src/core/services/token/token.service.ts
  - src/core/services/auth/user-info.service.ts
  - src/app/components/layout/assinatura-autenticacao/assinatura-autenticacao.component.ts
---

# Segurança e sessão — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Fluxo: [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Autenticacao|Fluxo-Autenticacao]] · Relacionado: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Rotas-e-Telas|Rotas-e-Telas]], [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]] · Backend: [[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao do Backend]]

> Análise **estática**. Nenhum token, usuário, senha ou endereço foi lido ou registrado; só nomes de chaves.

## Objetivo
Documentar como o frontend autentica, guarda a sessão e restringe telas por perfil, e o que isso **não** garante.

## Evidências
Arquivos em `sources`; contrato do backend em [[01-Sistemas/SICI/Backend/06-API/SICI-Backend-Catalogo-de-Endpoints|Catálogo de endpoints]].

## Informações confirmadas ✅
### Autenticação
- O frontend **não** fala com o Keycloak diretamente em nenhum caminho ativo. O login envia `POST {urlApi}/auth/login` (usuário e senha) ao **backend**, que atua como proxy do Keycloak ([[01-Sistemas/SICI/Backend/05-Fluxos/SICI-Backend-Fluxo-Autenticacao|Fluxo do Backend]]). Em seguida chama `GET /auth/account` e `GET /me`.
- A resposta do login modela `refresh_token` e `id_token`, mas **só `access_token` é usado**; nenhuma chamada de renovação foi encontrada. Ao expirar o JWT a sessão é encerrada e o usuário volta ao login.
- Expiração: `AuthService` agenda `logout` no instante de `exp` do JWT (`@auth0/angular-jwt`), e `getToken()` limpa a sessão se o token já expirou.
- `AuthGuard` (rota `pages`) só verifica que existe token **não expirado**; não valida assinatura (impossível no cliente).

### Armazenamento no navegador
| Chave | Conteúdo | Onde |
|---|---|---|
| `auth.access_token` | JWT | `sessionStorage` **e** `localStorage` |
| `auth.account` | dados da conta (nome, e-mail, `preferred_username`) | idem |
| `auth.roles` | perfis normalizados | idem |
| `assinatura_popup_ctx_<uuid>` | contexto da assinatura (tipo, id da OS e, na genérica, o corpo da OS) | `localStorage`; removida ao finalizar |
| `assinatura_toast` | mensagem de resultado da assinatura | `localStorage` |

Leitura: `sessionStorage` primeiro, depois `localStorage`. O `localStorage` mantém a sessão entre abas e o popup de assinatura; também a deixa persistir após fechar o navegador até o token expirar.

### Autorização no cliente
- Perfis (*roles*): normalizados removendo `ROLE_` e em maiúsculas. Origem inicial: claims do JWT (`authorities`, `roles`, `realm_access.roles`, `resource_access.*.roles`); depois `GET /me` (timeout de 5 s, em caso de falha mantém o cache) sobrescreve e persiste.
- `PermissionProfiles` (`authorization.config.ts`) liga permissões a quatro perfis (`SUBCI`, `COORDENADOR`, `DIRETOR`, `AUDITOR`):

| Permissão | Perfis |
|---|---|
| `CRIAR_ACAO`, `EDITAR_ACAO`, `EXCLUIR_ACAO` | SUBCI, COORDENADOR, DIRETOR |
| `CONSULTAR_ACAO` | SUBCI, COORDENADOR, DIRETOR, AUDITOR |
| `EMITIR_OS`, `EDITAR_OS`, `CONSULTAR_OS_POR_AC` | SUBCI, COORDENADOR, DIRETOR, AUDITOR |
| `LISTAR_OS`, `EDITAR_PERFIL` | SUBCI |
| `SOLICITAR_CANCELAMENTO_OS`, `CANCELAR_OS` | SUBCI, COORDENADOR, DIRETOR |

- `GuardPerfil` (rotas) e `PermissaoService.possuiPermissao` (menu e botões) usam essa tabela. Sem permissão, o guard redireciona para `acesso-negado`.
- Tratamento de erro: `401` → logout e login; `403` é só repassado (sem tela específica).
- Interceptor de token: anexa o `Bearer` apenas a URLs da mesma origem ou da origem de `urlApi`; não anexa a `/auth/login` nem a `/assets/`.

### Reautenticação na assinatura
Para assinar, o popup pede usuário e senha de novo, chama `POST /auth/login` **sem interceptors** (`HttpBackend`), confere que o `preferred_username` do novo token é o do usuário logado e usa **esse** token só na chamada de assinatura. O fluxo completo está em [[01-Sistemas/SICI/Frontend/05-Fluxos/SICI-Frontend-Fluxo-Assinatura-OS|Fluxo-Assinatura-OS]].

### Código de autenticação sem uso ✅ (busca textual)
`KeycloakService` (`keycloak-js`, `login-required`), `TokenService` (chave `token` no `localStorage`) e `UserInfoService` (`GET /api/me`, chave `user-info`) não são importados por nenhum arquivo da aplicação além de seus próprios `spec`. O `KeycloakService` lê `environment.keycloak`, que **não existe** nos arquivos de ambiente.

## Inferências e limitações 🔶
- **A restrição por perfil no frontend é de conveniência.** Qualquer endpoint exige só o que o backend verifica; o backend deixa 46 endpoints sem controle de perfil ([[01-Sistemas/SICI/Backend/08-Seguranca/SICI-Backend-Seguranca-e-Autorizacao|achados S1 e S4]]). Em especial, a tela de gestão SUBCI exige `EDITAR_PERFIL` (SUBCI), mas `POST /subci/cadastrar` e `POST /subci/{id}/substitutos` aceitam qualquer autenticado: o bloqueio da tela não impede a chamada direta.
- A permissão `EXCLUIR_ACAO` do frontend inclui `DIRETOR`, e o backend permite a inativação de ação só a SUBCI e COORDENADOR (`DELETE /acao-controle/inativar`); `CRIAR_ACAO`/`EDITAR_ACAO` coincidem. Divergência para confirmar nas [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
- Token e perfis em `localStorage`/`sessionStorage` ficam expostos a qualquer XSS. Não foi encontrado `bypassSecurityTrust*`; o único `innerHTML` está em `CkeditorComponent` (estilos). Conteúdo do CKEditor persistido e exibido em outras telas não foi rastreado.
- 🔶 A rota pública `validacao` chama `GET /assinaturas/validacao`, que **exige token** no backend; sem login, o `401` leva ao login. Ver [[01-Sistemas/SICI/Frontend/03-Modulos/SICI-Frontend-Assinatura-e-Validacao|Assinatura-e-Validacao]].
- O `localStorage` guarda o corpo da OS genérica durante a assinatura; é removido ao finalizar, mas permanece se o popup for fechado antes.
- Cabeçalhos de segurança do nginx (CSP, HSTS etc.) não aparecem em `nginx.conf` (🔶 podem estar em outra camada).
- Cobertura parcial: templates HTML e componentes de tela não foram varridos em busca de outros pontos de entrada de dados.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]] · [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Chamadas-de-API|Chamadas-de-API]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
