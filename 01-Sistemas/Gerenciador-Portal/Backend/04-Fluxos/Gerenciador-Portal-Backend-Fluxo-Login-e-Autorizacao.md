---
type: flow
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - backend
  - fluxo
  - login
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/api/LoginController.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/LoginService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/SsoAuthClient.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/JwtService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/services/auth/AutorizacaoService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/handler/ResourceExceptionHandler.java
---
# Fluxo de login e autorização

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Descrever, passo a passo, o que acontece em `POST /login`.

## Evidências
`LoginController` → `LoginService.autenticar` → `SsoAuthClient` → `JwtService` → `AutorizacaoService`.

## Informações confirmadas
| # | Passo | Resultado |
|---|---|---|
| 1 | O cliente envia `{login, senha}` com `x-client-id` | sem o cabeçalho, `400` |
| 2 | Se coincide com `dev.usuario.cpf` e `dev.usuario.senha` | devolve `UsuarioDTO` "DEVELOPER", `servidorSUTCS=true`; **fim, sem SSO** |
| 3 | `SsoAuthClient` envia `POST` form-urlencoded ao `so.auth.url` (`grant_type=password`, `client_id`, `client_secret`, `username`, `password`, `idOrgao`) | `TokenResponse` ou erro |
| 4 | Erro 401 do SSO → `AutenticacaoException`; outro 4xx → idem; 5xx ou falha de rede → idem | o handler responde `401` em todos os casos |
| 5 | Sem `access_token` na resposta | `RuntimeException` → `500` |
| 6 | `JwtService` decodifica o token (sem verificar assinatura) e preenche `UsuarioDTO` | claims `nomePessoa`, `login` (também usado como CPF), `matricula`, `siglaOrgao`, `idOrgao`, `nomeOrgao`, `autenticado`, `unidades[]` |
| 7 | `AutorizacaoService`: `idOrgao == autorizacao.id-orgao` **e** alguma unidade em `autorizacao.id-unidades` | senão `AcessoNegadoException` → `403` |
| 8 | Sucesso | `200` com o `UsuarioDTO`; nenhum token nem sessão é criado |

- ✅ A claim `autenticado` do JWT alimenta o campo `servidorSUTCS` do DTO; no usuário "DEVELOPER" ele é `true`.
- ✅ O gerenciador não guarda estado de login: o cliente repassa o `usuarioLogado` nas chamadas seguintes.

## Falhas e dependências
Ver [[01-Sistemas/Gerenciador-Portal/Backend/06-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança]] (usuário de desenvolvimento, JWT sem assinatura verificada, SSO via `http`, status `401` único).

## Inferências e limitações
- 🔶 O cliente web usa o `UsuarioDTO` devolvido para exibir o nome e preencher o `usuarioLogado` (o último commit chama-se "corrige usuário logado para admin"; o conteúdo não foi lido).
- ❓ Como o cliente protege a sessão e se ele envia o token a outro serviço.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|Integração com o SSO]]

## Pendências e próximo passo
- Ler o diff do commit `14b185f` caso a regra do "usuário logado" precise ser documentada.
