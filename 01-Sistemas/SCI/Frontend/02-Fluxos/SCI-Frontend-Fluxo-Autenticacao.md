---
type: flow
system: SCI
component: Frontend
repository: sci-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5e20fda1ec781719cb277c36d160db2efd5a6c1b
updated: 2026-10-19
tags:
  - sci
  - frontend
  - fluxo
  - autenticacao
sources:
  - src/app/auth/login/login.component.ts
  - src/app/auth/login/login.component.html
  - src/app/store/services/usuario.service.ts
  - src/app/store/effects/usuario.effects.ts
  - src/app/core/guard/auth.guard.ts
  - src/app/components/layout/sidenav/sidenav.component.ts
---
# SCI Frontend — fluxo de autenticação

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Descrever login, recarga da página, troca de perfil e saída, do ponto de vista do cliente.

## Evidências
- `auth/login/login.component.ts` e `.html`, `store/services/usuario.service.ts`, `store/effects/usuario.effects.ts`, `core/guard/auth.guard.ts`, `components/layout/sidenav`.

## Informações confirmadas
1. **Login.** O formulário pede `login` (validado como CPF por `cpfValidator`) e `senha`. Formulário inválido só mostra erros; válido dispara a ação `login`, o efeito chama `POST security/auth` e o serviço grava o token no cookie `_userData`.
2. **Estado.** Em caso de sucesso, `loginSuccess` coloca o usuário (perfil, unidade, órgão) no NgRx. O componente observa o perfil e navega para `/home` (que cai em `pages/home` por redirecionamentos). Em erro, limpa o formulário e mostra mensagem do backend.
3. **Recarga da página.** O estado se perde; o `AuthGuard` vê o cookie e chama `GET usuario`; sucesso → recompõe o estado e verifica o perfil; falha → apaga cookie e vai ao login.
4. **Troca de perfil/unidade.** O usuário abre o seletor no menu, `GET usuario/permissoes` lista as permissões agrupadas por unidade, e a confirmação chama `POST usuario/alternar-permissao`; o token novo substitui o cookie e `GET usuario` atualiza a identidade.
5. **Saída.** Apaga o cookie e zera a store. 401/403 de qualquer chamada leva ao mesmo resultado e redireciona para `auth/login`.
6. **Links externos na tela de login.** "Esqueci minha senha" e "Novo cadastro" abrem em nova aba endereços sob `participaUrl` (`pages/conta/recuperar-senha` e `pages/conta/direcionar-usuario`). Ver [[01-Sistemas/SCI/Frontend/04-API-e-Integracoes/SCI-Frontend-Integracoes|Integrações]].

## Inferências e limitações
- 🔶 O login usa credenciais CPF e senha enviadas ao backend do SCI, que no código do backend valida contra o `PARTICIPA-DF` ([[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|Integração SCI → PARTICIPA-DF]]); o frontend não conhece essa etapa.
- ❓ Não há tela de recuperação de senha no SCI; a recuperação depende do outro sistema, e o endereço real de `participaUrl` não foi registrado.
- O fluxo de recarga e o de troca de perfil foram lidos só no cliente; o comportamento do backend vem das notas dele.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/05-Seguranca/SCI-Frontend-Seguranca-e-Sessao|Segurança e sessão]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Autenticacao|Fluxo de autenticação do backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
