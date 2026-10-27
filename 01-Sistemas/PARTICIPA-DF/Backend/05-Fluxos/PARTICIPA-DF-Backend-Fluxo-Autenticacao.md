---
type: flow
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: completa
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - fluxo
  - autenticacao
  - senha
sources:
  - src/OuvDF.Api/Controllers/Shared/SecurityController.cs
  - src/OuvDF.Api/Controllers/Shared/UsuarioController.cs
  - src/OuvDF.Shared/Domain/Commands/AutenticarUsuario/AutenticarUsuarioHandler.cs
  - src/OuvDF.Shared/Domain/Commands/CancelarToken/CancelarTokenHandler.cs
  - src/OuvDF.Shared/Domain/Commands/NotificarAutenticacao/NotificarAutenticacaoHandler.cs
  - src/OuvDF.Shared/Domain/Commands/RecuperarSenha/RecuperarSenhaHandler.cs
  - src/OuvDF.Shared/Domain/Commands/ConcluirRecuperacaoSenha/ConcluirRecuperacaoSenhaHandler.cs
  - src/OuvDF.Shared/Domain/Commands/AlterarSenha/AlterarSenhaHandler.cs
---

# Fluxo de autenticação e senha

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]], [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Bloqueio-de-Usuario|Bloqueio-de-Usuario]]

## Objetivo
Descrever passo a passo, com atores e estados, o login, o login assistido por sessão, o logout e a recuperação/alteração de senha.

## Evidências
Handlers e controllers em `sources`, commit `4901ad5`. Cobertura `completa` para o que está no repositório; o comportamento do SDK (geração e validação do JWT) é ❓.

## Informações confirmadas

### 1. Login (`POST /security/auth`)
```mermaid
sequenceDiagram
    participant U as Cliente (cidadão ou operador)
    participant C as SecurityController
    participant H as AutenticarUsuarioHandler
    participant DB as SQL Server
    participant T as ITokenService (SDK)
    U->>C: login + senha
    C->>H: AutenticarUsuario
    H->>DB: busca Usuario por Login
    alt login inexistente ou senha inválida
        H-->>U: 400 "Login ou Senha inválido"
    else válido
        H->>DB: ConsultarBloqueioUsuario
        alt há bloqueio
            H-->>U: 400 "Usuário bloqueado" + id do motivo
        else sem bloqueio
            H->>DB: existe OperadorSO / OperadorSIC / OperadorWS?
            H->>T: GenerateToken(claims Sid, Email, Name, Roles)
            H->>DB: atualiza DataUltimoLogin
            H-->>U: login, token, nome
        end
    end
```
1. ✅ Validação de entrada: senha e login obrigatórios (`AutenticarUsuario.Validate`); a senha é `[JsonIgnore]` na serialização do comando (não vai para o log de auditoria).
2. ✅ Mensagem única para login ou senha inválidos.
3. ✅ A verificação de bloqueio acontece **depois** da validação da senha.
4. ✅ Papéis incluídos conforme a existência do registro de operador (independente de o operador estar ativo: o handler não consulta `Ativo`; 🔶 a desativação precisa ser tratada em outro ponto, como as consultas ou o job).

### 2. Login assistido por sessão
```mermaid
sequenceDiagram
    participant A as Cliente A (já autenticado)
    participant B as Cliente B (sem sessão)
    participant S as SecurityController
    participant K as Cache distribuído (SQL Server)
    A->>S: POST /security/notify {sessionId, token}
    S->>K: grava token (expira em 30 s)
    B->>S: GET /security/token-retrieve/{sessionId}
    S->>K: lê sessionId
    alt existe
        S-->>B: token
    else expirou
        S-->>B: 401
    end
```
- ✅ `notify` exige autenticação; `token-retrieve` é anônimo.
- 🔶 Uso provável: autenticar um segundo cliente a partir de uma sessão já iniciada (ex.: retorno de um login externo). O consumidor não está neste repositório (❓).

### 3. Logout
`GET /security/logout`: se há cabeçalho `Authorization`, grava o token em `TokenCancelado`; sem cabeçalho devolve `200`. ✅ A verificação do token cancelado (`ValidateTokenFilter`) não está ligada no repositório (🔶 ver nota de segurança).

### 4. Recuperação de senha
1. ✅ `POST /usuario/recuperar-senha` (anônimo): localiza o usuário pelo login (CPF/CNPJ). Se não existe, erro "Não foi possível localizar um usuário com o …". Se existe, responde com o e-mail **mascarado** e envia o e-mail "Recupere sua senha" pelo MailService.
2. ✅ O link contém `id` e `dtexp` criptografados (`JsonEncryptConverter`) e vale **30 minutos**.
3. ✅ `POST /usuario/concluir-recuperacao-senha` (anônimo): descriptografa a data (erro "Operação inválida" se falhar), recusa se vencida, calcula o fator de complexidade e chama `Usuario.AtualizarSenha`.
4. 🔶 `RecuperarSenhaHandler` não trata `usuario.Email` nulo: o trecho que tratava isso está comentado (bloco antigo).
5. 🔶 Em `ConcluirRecuperacaoSenhaHandler` o aviso de link expirado é adicionado, mas a validação de complexidade e a troca continuam a rodar; o resultado depende de `command.IsValid` na saída do handler.

### 5. Alteração de senha (`POST /usuario/alterar-senha`, autenticado)
✅ Confere a senha atual; calcula a complexidade (simples para cidadão, complexa para operador ativo); recusa a senha igual à atual ou às anteriores; grava o histórico via `HistoricoSenha` (🔶 `AtualizarHistoricoDeSenha` está comentado).

### Estados do usuário relevantes ao fluxo
| Estado | Efeito no login |
|---|---|
| Sem bloqueio | autentica |
| Com `BloqueioUsuario` | recusa e informa o motivo ([[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/Bloqueio-de-Usuario|Bloqueio-de-Usuario]]) |
| `RedefinirSenha = true` | ✅ campo existe e é limpo ao trocar a senha; ❓ onde o cliente é forçado a trocar |

## Inferências e limitações
- ❓ Geração, assinatura e validade do token (SDK).
- 🔶 Os pontos sinalizados aqui são analisados em [[01-Sistemas/PARTICIPA-DF/Backend/08-Seguranca/PARTICIPA-DF-Backend-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]].

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/03-Modulos/Usuarios-Operadores-Perfis|Usuarios-Operadores-Perfis]]

## Pendências e próximo passo
- Confirmar com o time o uso do login assistido e a exigência de troca de senha (`RedefinirSenha`).
- Lote 7: documentar MailService e PeoplesCheck como integrações.
