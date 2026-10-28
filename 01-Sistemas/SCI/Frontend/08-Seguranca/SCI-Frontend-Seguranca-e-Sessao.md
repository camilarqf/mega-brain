---
type: security
aliases:
  - "SCI Frontend — segurança e sessão"
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - autenticacao
sources:
  - src/app/core/guard/auth.guard.ts
  - src/app/core/guard/alterar-pip.guard.ts
  - src/app/core/interceptors
  - src/app/store/services/usuario.service.ts
  - src/app/store/reducers/meta.reducer.ts
  - src/app/components/layout/sidenav/sidenav.component.ts
---
# SCI Frontend — segurança e sessão

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar como o frontend guarda o token, protege rotas e reage a erros de autenticação. Sem valores sensíveis.

## Evidências
- `core/guard/auth.guard.ts`, `core/guard/alterar-pip.guard.ts`, `core/interceptors/*.ts`, `store/services/usuario.service.ts`, `store/effects/usuario.effects.ts`, `store/reducers/meta.reducer.ts`, `components/layout/sidenav/sidenav.component.ts`.

## Informações confirmadas
### Token e sessão
- ✅ `UsuarioService.login` faz `POST security/auth` com `{ login, senha }` e grava o `token` devolvido no cookie `_userData` (`path: '/'`), via `ngx-cookie-service`. Os demais dados do usuário (perfil, unidade, órgão) ficam só no estado NgRx, em memória.
- ✅ O cookie é lido e escrito por JavaScript; **não** é `HttpOnly`. O `set` não informa `Secure` nem `SameSite`; o `delete` usa `SameSite=Lax`.
- ✅ `AuthInterceptor` acrescenta `Authorization: Bearer <cookie _userData>` em **toda** requisição HTTP, inclusive a chamadas fora da API, se existissem (a única base usada é `apiUrl`).
- ✅ Troca de perfil/unidade no menu lateral: `POST usuario/alternar-permissao` devolve novo token; o cookie é substituído e `GET usuario` recarrega o usuário.
- ✅ `logout` apaga o cookie e `clearStateMetaReducer` zera o estado NgRx.

### Proteção de rotas
- ✅ `AuthGuard`: sem usuário no estado, usa o cookie para chamar `GET usuario`; falha → apaga cookie, `logoutSuccess` e vai a `/auth/login`. Com usuário, compara `user.perfil` com `route.data.role` (lista ou valor único); sem permissão → `/auth/acesso-negado`; sem `data.role` → libera.
- ✅ `AlterarPipGuard`: nas rotas de edição de fato do PIP, carrega o PIP (`GET pip/{id}?includeDetails=true`) e redireciona para `listar-fatos` se o `idFato` não existir.
- ✅ O menu lateral oculta grupos por perfil (`podeExibir*`); botões de ação nas telas também são condicionados a perfil e a status (por exemplo, só `Apoio Correcional` aceita ou recusa denúncia).

### Tratamento de erros (`ErrorInterceptor`)
- 401 ou 403: apaga o cookie, dispara `logout` e navega para `auth/login`; o erro não é exibido ao usuário.
- 400 em `GET .../usuario`: trata como usuário inválido, apaga o cookie e `logoutSuccess`.
- Demais erros ≥ 400: exibidos pelo `GlobalErrorService` no formato `{status, requestId, title, detail, instance}`; status `0` mostra "erro de conexão". Corpo `Blob` é convertido em JSON ou texto.

### Outros controles
- ✅ `cpfValidator` valida o CPF digitado no login (apenas no cliente).
- ✅ Conteúdo rico (fundamentação, descrição) é exibido por `[innerHTML]`, com a sanitização padrão do Angular.
- ✅ `DomSanitizer.bypassSecurityTrustResourceUrl` é usado em dois pontos: URL de blob do anexo PDF em `analisar-denuncia` e o `iframe` do painel de gestão.

## Inferências e limitações
- 🔶 Toda a autorização do cliente (guards, menu, botões) é só conveniência; a decisão real depende das políticas do backend ([[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização do backend]]). As rotas `denuncias` e `encaminhados` não têm `data.role`.
- 🔶 Cookie sem `HttpOnly` e sem `Secure` explícito amplia o impacto de XSS e de tráfego sem TLS; o impacto real depende de o site ser servido só por HTTPS (não verificado).
- ❓ Expiração do token: não há renovação nem checagem de expiração no cliente; `jwt-decode` não foi encontrado em uso nos arquivos lidos.
- Riscos listados em [[01-Sistemas/SCI/Frontend/09-Qualidade/SCI-Frontend-Debitos-Tecnicos|Débitos técnicos]].

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/05-Fluxos/SCI-Frontend-Fluxo-Autenticacao|Fluxo de autenticação]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Rotas-e-Telas|Rotas e telas]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Perfis-e-Ambientes|Perfis e ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
