---
type: security
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - seguranca
  - autenticacao
  - autorizacao
sources:
  - src/OuvDF.Api/Startup.cs
  - src/OuvDF.Api/Controllers/Shared/SecurityController.cs
  - src/OuvDF.Api/Controllers/Shared/UsuarioController.cs
  - src/OuvDF.Api/Controllers/Shared/v2/UsuarioController.cs
  - src/OuvDF.Api/Controllers/Shared/OperadorSOController.cs
  - src/OuvDF.Api/Controllers/Shared/IntegracaoController.cs
  - src/OuvDF.Api/Controllers/Shared/JobController.cs
  - src/OuvDF.Api/Filters/ValidateTokenFilter.cs
  - src/OuvDF.Api/Filters/LogAudit.cs
  - src/OuvDF.Shared/Domain/ClaimsOptions.cs
  - src/OuvDF.Shared/Domain/Commands/AutenticarUsuario/AutenticarUsuarioHandler.cs
  - src/OuvDF.Shared/Domain/Commands/CancelarToken/CancelarTokenHandler.cs
  - src/OuvDF.Shared/Domain/Commands/NotificarAutenticacao/NotificarAutenticacaoHandler.cs
  - src/OuvDF.Shared/Domain/Commands/RecuperarSenha/RecuperarSenhaHandler.cs
  - src/OuvDF.Shared/Domain/Commands/ConcluirRecuperacaoSenha/ConcluirRecuperacaoSenhaHandler.cs
  - src/OuvDF.Shared/Domain/Commands/AlterarSenha/AlterarSenhaHandler.cs
  - src/OuvDF.Shared/Domain/Commands/GravarOperadorWS/GravarOperadorWSHandler.cs
  - src/OuvDF.Shared/Domain/Entities/Usuario.cs
  - src/OuvDF.Shared/Domain/Entities/OperadorWS.cs
  - src/OuvDF.Shared/Domain/Entities/TokenCancelado.cs
  - src/OuvDF.Shared/Domain/Enums/FuncionalidadeEnum.cs
---

# Segurança e autorização

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]], [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Bloqueio-de-Usuario|Bloqueio-de-Usuario]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Objetivo
Registrar como o backend autentica, autoriza e audita, e quais pontos de atenção aparecem no código. **Sem segredos**: nada de chaves, senhas ou valores de configuração.

## Evidências
Arquivos em `sources`, commit `4901ad5`. Partes do mecanismo vivem no SDK interno `CGDF.DotNet.SDK.*` (`UseCgdfSecurity`, `AddJwtSecurity`, `ITokenService`, a classe `Senha`), que não está no repositório e **não foi lido**.

## Informações confirmadas

### Autenticação
- ✅ `POST /security/auth` (anônimo): `AutenticarUsuarioHandler` busca o `Usuario` pelo `Login`, valida a senha (`Usuario.IsSenhaValida`) e, em caso de erro, responde sempre "Login ou Senha inválido" (não diferencia login e senha).
- ✅ Antes de emitir o token consulta bloqueios (`ConsultarBloqueioUsuario`); se houver, responde "Usuário bloqueado" com o id do motivo em `ExceptionDetails`.
- ✅ Claims do token: `Sid` (id), `Email` (se houver), `Name` (nome da pessoa física ou razão social) e papéis `OperadorSO`, `OperadorSIC` e `OperadorWS` conforme a existência do operador (`ClaimsOptions`). O token é gerado por `ITokenService.GenerateToken`.
- ✅ Em caso de sucesso `DataUltimoLogin` é atualizada (base da desabilitação de operadores após 90 dias, ver [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]]).
- ✅ JWT configurado por `Jwt` (`Secret`, `ExpirationDays`) e `SecuritySecret` (nomes de chaves; valores omitidos).
- ✅ `GET /security/is-auth` informa `User.Identity.IsAuthenticated`.

### Logout
- ✅ `GET /security/logout` (autenticado) grava o cabeçalho `Authorization` em `TokenCancelado` (`CancelarToken`, sem duplicar).
- ✅ `ValidateTokenFilter` responde `401` quando o token enviado consta em `TokenCancelado`.

### Login assistido por sessão
- ✅ `POST /security/notify` (autenticado, `NotificarAutenticacao`) grava o token no cache distribuído com chave `SessionId` e validade de **30 segundos**.
- ✅ `GET /security/token-retrieve/{sessionId}` (anônimo) devolve o token do cache ou `401`.
- ✅ Hub SignalR `/notification-auth` (`NotificarAutenticacaoMessage`) com `SendAsync` para todos os clientes.

### Autorização
- ✅ **Papéis** (`[Authorize(Roles=…)]`): `OperadorSO`, `OperadorSIC`, `OperadorWS`. Exemplos: `operador-so` inteiro exige `OperadorSO`; `v1/…` (`IntegracaoController`) exige `OperadorWS`; bloquear/desbloquear usuário e buscas por nome/login exigem `OperadorSO`.
- ✅ **Funcionalidades** por perfil: `Perfil.Funcionalidades` + `OperadorSO/SIC/WS.CheckPermissao(FuncionalidadeEnum)`, usadas dentro de handlers (94 usos no código). O enum tem 64 valores: SO de 1 a 50 e SIC de 201 a 220.
- ✅ Módulos de perfil: `SERVICO_OUVIDORIA = 1` e `SERVICO_INFORMACAO_CIDADAO = 2`. Um perfil só aceita funcionalidades do próprio módulo.
- ✅ Perfis do cidadão: usuário autenticado sem papel de operador.

### Endpoints anônimos relevantes (`[AllowAnonymous]`)
`POST /security/auth`, `GET /security/token-retrieve/{sessionId}`, `GET /security/check`, `GET /security/count-try`, `POST /security/challenge`, `GET /security/check-cpf-vinculado-pj` (usam o PeoplesCheck), `POST /usuario/recuperar-senha`, `POST /usuario/concluir-recuperacao-senha`, `GET /usuario/{obterInfoOperadorSIC}/{obterInfoOperadorSO}` e `GET /v2/usuario/…`, `POST /pessoa-fisica` (cadastro), `POST /pessoa-juridica`, `…/existe`, `…/desbloquear-dados-inconsistentes`, `GET /politica/vigente` e **`POST /operador-so/operador-ws`**.

### Senhas
- ✅ Complexidade: `ConsultarFatorComplexidadeSenhaHandler` aplica `FatorComplexidadeSenha.Complexa` se o usuário é operador SIC/SO **ativo**, senão `Simples`.
- ✅ Recuperação: `POST /usuario/recuperar-senha` envia por e-mail (MailService) um link com o id do usuário e a data de expiração **criptografados**, válido **30 minutos**; a resposta traz o e-mail mascarado (`MixedValue`). `concluir-recuperacao-senha` descriptografa, confere o prazo e aplica a nova senha.
- ✅ `Usuario.AtualizarSenha` recusa a senha atual ou anterior (`IsSenhaAtualOrAnterior`); `RedefinirSenha` passa a `false`.
- ✅ `OperadorWS` é criado com expiração de **1 ano** (`DataExpiracao`) e o comando `GravarOperadorWS` devolve `Senha.DecryptValue` (valor em claro).

### Auditoria e logs
- ✅ `[LogAudit]` grava `GravarLogAuditoria` (payload serializado, nome do comando, rota e usuário) após a ação, se o comando é válido; falhas só são logadas.
- ✅ `ExceptionHandlingFilter` mascara campos de senha e o `Relato` nos logs de erro, mas **não** está ligado (ver abaixo).

## Inferências e pontos de atenção
Fatos acima; abaixo, o que **não** é confirmado ou merece atenção. As recomendações ficam para o lote 8.
- 🔴 **Logout sem efeito comprovado.** `ValidateTokenFilter` não é referenciado em nenhum projeto do repositório (nem `AddMvc`, `[ServiceFilter]` ou `[TypeFilter]`). Se o SDK não faz essa checagem, o token cancelado continua válido até expirar. ❓ confirmar no SDK.
- 🔴 **`POST /operador-so/operador-ws` é anônimo** e usa `User.Id()` para registrar o autor. 🔶 O handler faz `loginExistente != null` sobre uma consulta (sempre verdadeiro), então tende a rejeitar sempre com "login já cadastrado"; o resultado real não foi testado.
- 🔴 **Senha reversível**: `GravarOperadorWS` devolve `DecryptValue`. A classe `Senha` é do SDK (❓ algoritmo); o armazenamento reversível é indício, não prova.
- 🔶 **Link de recuperação reaproveitável** dentro dos 30 minutos: não há token de uso único, só `id` + validade criptografados.
- 🔶 **Enumeração de usuários**: `recuperar-senha` diferencia login inexistente (mensagem própria) de existente (devolve e-mail mascarado).
- 🔶 **Sem limite de tentativas** de login no handler. O `count-try` do PeoplesCheck serve ao desafio (❓).
- 🔶 **Token do login assistido** pode ser lido por qualquer um que conheça o `sessionId` enquanto estiver no cache (30 s).
- 🔶 **Hub SignalR** sem `[Authorize]` visível e `Clients.All`.
- 🔶 **Histórico de senhas**: a rotina `AtualizarHistoricoDeSenha` está comentada (`//TODO: Revisar`), logo a regra "três senhas anteriores" pode não ser aplicada (a mensagem existe, mas o histórico só é preenchido se a rotina o fizer).
- 🔶 `/jobs/*` sem `[Authorize]` visível. Se o SDK impõe autenticação global, ❓ não confirmado.
- 🔶 A regra "falecido não pode ser desbloqueado" parece sem efeito ([[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Bloqueio-de-Usuario|Bloqueio-de-Usuario]]).
- 🔶 Nome no token: `claims.First(Name)` quebra para usuário que não seja pessoa física/jurídica (ex.: `OperadorWS`).
- ❓ Rotação de segredos e política de expiração em produção; valores em `Jwt.ExpirationDays`.
- ❓ Se a autorização por funcionalidade ocorre para todos os endpoints de operador (muitos têm só `[Authorize]`).

## Relacionamentos
- Fluxo detalhado: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao]].
- Entidades e endpoints: [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]].
- Bloqueios: [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Bloqueio-de-Usuario|Bloqueio-de-Usuario]].
- PeoplesCheck e MailService (lote 7): [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]].

## Pendências e próximo passo
- Confirmar no SDK (`UseCgdfSecurity`, `AddJwtSecurity`, `Senha`) se há checagem de token cancelado, autenticação global e como a senha é guardada.
- Registrar as recomendações no lote 8 ([[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]]).
