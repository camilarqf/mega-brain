---
type: flow
aliases:
  - "SCI Backend — fluxo de autenticação"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: completa
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - autenticacao
sources:
  - src/SCI.Api/Controllers/SecurityController.cs
  - src/SCI.Application/UseCases/AutenticarUsuario/AutenticarUsuarioHandler.cs
  - src/SCI.Infrastructure.Services/Auth/TokenService.cs
  - src/SCI.ParticipaDF.Client/Services/ParticipaDFClient.cs
---
# SCI Backend — fluxo de autenticação

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Passo a passo do login por CPF e senha (sem a POC de SSO, fora do escopo).

## Evidências
- `AutenticarUsuarioHandler.Handle`, `ParticipaDFClient.Authenticate`, `TokenService.CreateToken`.

## Informações confirmadas
1. `POST /security/auth` (anônimo) recebe CPF e senha.
2. Busca o usuário por CPF; se não existe → `AuthenticationFailedException` "Usuário não encontrado.".
3. Se o usuário não tem `PermissaoAtual` → "Usuário sem permissão de acesso.".
4. Valida a credencial no `PARTICIPA-DF` (`POST` com login = CPF formatado e senha; [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracao-Participa-DF-Autenticacao|integração]]). Qualquer exceção do cliente vira `AuthenticationFailedException` com a mensagem recebida.
5. **Exceção de bypass**: existe no código uma lista fixa de CPFs que, combinada a uma senha fixa, **dispensa** a chamada ao `PARTICIPA-DF` (valores não reproduzidos aqui; ver [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]]).
6. Emite o JWT do SCI com id, unidade, perfil, nome e role da permissão atual.
7. Resposta: id, CPF formatado, descrição do perfil, descrição e sigla da unidade e o token.
8. Troca de perfil/unidade: `POST /usuario/alternar-permissao` gera novo token ([[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Identidade-e-Permissoes|Identidade]]).
9. `GET /security/is-auth` informa se a requisição está autenticada.

## Inferências e limitações
- 🔶 `AuthenticationFailedException` é tratada por `HandleAuthenticationFailedException`; o código HTTP devolvido não foi conferido.
- Prazo do token vem de `JwtSettings.ExpirationDays` (valor não registrado).

## Relacionamentos
- [[01-Sistemas/SCI/Backend/08-Seguranca/SCI-Backend-Seguranca-e-Autorizacao|Segurança e autorização]]

## Pendências e próximo passo
- Conferir o código HTTP da falha de autenticação.
