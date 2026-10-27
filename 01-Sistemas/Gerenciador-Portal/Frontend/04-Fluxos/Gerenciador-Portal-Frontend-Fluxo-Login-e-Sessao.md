---
type: flow
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
tags:
  - gerenciador-portal
  - frontend
  - fluxo
  - login
  - sessao
sources:
  - src/app/components/login/loginCtrl.js
  - src/app/components/login/loginAPI.js
  - src/app/components/navbar.controller.js
  - src/app/index.route.js
  - src/app/token-interceptor.js
---
# Fluxo de login e sessão — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Descrever o que o frontend faz do login até o logout. O lado do servidor está em [[01-Sistemas/Gerenciador-Portal/Backend/04-Fluxos/Gerenciador-Portal-Backend-Fluxo-Login-e-Autorizacao|Fluxo de login do Backend]].

## Evidências
`loginCtrl.js`, `loginAPI.js`, `navbar.controller.js`, `index.route.js`, `token-interceptor.js` (lidos integralmente) e `exclusoesMedidaProtetivaApi.js`, `arquivoCtrl.js`, `imagemCtrl.js` (uso de `$localStorage.usuario`).

## Informações confirmadas
| # | Passo | Resultado |
|---|---|---|
| 1 | O usuário abre `/` e informa `login` e `senha` (Enter também envia, por `ngEnter`) | `LoginController.autenticacaoDoLogin` |
| 2 | `POST /login` com `{login, senha}` e `x-client-id` | `200` com o `UsuarioDTO` |
| 3 | O frontend grava a resposta **inteira** em `$localStorage.usuario` (`ngStorage`, `localStorage` do navegador) | persiste entre abas e reinícios do navegador |
| 4 | Redireciona para `/arquivo` | telas lêem `$localStorage.usuario.login` para auditoria |
| 5 | Falha | mostra `error.data.mensagem` ou "Não foi possível realizar a autenticação."; `console.error` do erro |
| 6 | Logout (item "SAIR" do menu, `NavbarController.logout`) | `$localStorage.$reset()` e volta para `/` |

- ✅ **Nenhum token é guardado nem enviado**: o backend não devolve token (nota do backend) e as chamadas seguintes só levam `x-client-id` mais o login nos parâmetros.
- ✅ **Sem guarda de rota nem expiração de sessão**: a "sessão" é a presença de `usuario` no `localStorage`; ela não expira e nenhum código valida seu conteúdo.
- ✅ `LoginController.main` (limpa todo o `localStorage` e volta para `/`) existe, mas não é referenciado em `login.html` nem por `ng-init`; 🔶 código sem uso.
- ✅ Erros `401`/`403` do backend durante o uso **não** derrubam a sessão (o interceptor só rejeita).

## Falhas e dependências
- Abrir qualquer rota sem ter feito login mostra a tela (`otherwise` só cobre rotas desconhecidas); as telas que dependem do usuário quebram com `TypeError`.
- Quem edita o `localStorage` (por exemplo definindo `usuario.login`) passa a assinar as operações com esse login; o backend não confere.
- O login é digitado em tela própria (e não redireciona ao SSO); a senha trafega para o backend, que a repassa ao Keycloak por `http` segundo a configuração dele.

## Inferências e limitações
- 🔶 O arquivo não versionado `src/app/sessao-sso.service.js` (fábrica `sessaoSso`: `iniciar`, `obterLogin`, `estaAutenticada`, `encerrar`) sugere uma refatoração da sessão em andamento; **fora do escopo** por decisão do usuário e sem uso no código versionado.
- ❓ Campos do `UsuarioDTO` que o frontend consome: `login` e `nome` (`$scope.nomeUsuario = vm.usuario.nome`); a claim equivalente no backend se chama `nomePessoa`, então é preciso confirmar se o DTO expõe `nome`.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/06-Seguranca/Gerenciador-Portal-Frontend-Seguranca-e-Sessao|Segurança e sessão]] · [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|Integração do Backend com o SSO]] · [[01-Sistemas/Gerenciador-Portal/Frontend/05-API-e-Integracoes/Gerenciador-Portal-Frontend-Integracao-API-Backend|Integração com o Backend]]

## Pendências e próximo passo
- Confirmar o formato do `UsuarioDTO` e o destino da refatoração `sessaoSso`.
