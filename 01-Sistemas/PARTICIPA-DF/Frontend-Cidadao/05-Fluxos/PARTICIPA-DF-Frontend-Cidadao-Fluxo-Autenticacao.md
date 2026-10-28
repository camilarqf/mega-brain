---
type: flow
aliases:
  - "Frontend Cidadão — fluxo de autenticação"
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - autenticacao
sources:
  - src/app/pages/login/login.component.ts
  - src/app/pages/conta/desafio-pesssoa-fisica/desafio-pesssoa-fisica.component.ts
  - src/app/pages/validacao/gerenciar-validacao/gerenciar-validacao.component.ts
  - src/app/pages/conta/recuperar-senha/recuperar-senha.component.ts
  - src/app/pages/conta/redefinir-senha/redefinir-senha.ts
  - src/app/core/enums/validar-cpf.enum.ts
---

# Frontend Cidadão — fluxo de autenticação

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]] · Backend: [[01-Sistemas/PARTICIPA-DF/Backend/05-Fluxos/PARTICIPA-DF-Backend-Fluxo-Autenticacao|Fluxo-Autenticacao do Backend]]

## Objetivo
Descrever as telas e chamadas do login, do desbloqueio por desafio e da recuperação de senha, do ponto de vista do frontend.

## Evidências
Arquivos em `sources`, commit `d250804`. Cobertura `parcial`: lido o login, o desbloqueio e a orquestração do desafio; as telas de recuperação/redefinição foram identificadas pelos endpoints.

## Informações confirmadas

### 1. Login (`/pages/auth`)
```mermaid
sequenceDiagram
    participant U as Cidadão
    participant L as Login
    participant API as Backend
    U->>L: login (3–50) e senha (5–255)
    L->>API: POST security/auth
    alt sucesso
        API-->>L: Token e UserName
        L->>L: grava _userData; navega para validacao/gerenciar-validacao (returnUrl)
    else erro com ExceptionDetails.Id = 1 (PF) ou 5 (PJ)
        L->>API: GET security/count-try?data=<doc>
        alt tentativas > 2
            L-->>U: modal de tentativas esgotadas
        else
            L->>API: GET security/check?data=<doc> (PF)
            L-->>U: tela de desafio
        end
    end
```
- ✅ O `returnUrl` da query string é preservado em todo o fluxo.
- ✅ Para PJ (Id 5), o login leva a `conta/validar-cpf` com `modoValidacao = desbloquearPessoaJuridica`; para PF (Id 1), a `conta/desafio-pessoa-fisica` com `desbloquearPessoaFisica`.
- ✅ `ValidarCPFEnum`: 0 criar conta PF, 1 desbloquear PF, 2 criar conta PJ, 3 desbloquear PJ, 4 atualizar CPF vinculado à PJ.

### 2. Desafio (`conta/desafio-pessoa-fisica`)
- ✅ Recebe o contrato do desafio por `TrocaDadosService` e consulta `security/count-try`. Envia a resposta por `POST security/challenge`.
- ✅ Após resolver: PF/PJ existente (`pessoa-fisica/existe`, `pessoa-juridica/existe`) → desbloqueio de dados inconsistentes (`pessoa-fisica/desbloquear-dados-inconsistentes` / `pessoa-juridica/desbloquear-dados-inconsistentes`, ou `pessoa-juridica/atualizar-responsavel`); inexistente → vai à criação de conta ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Fluxos/PARTICIPA-DF-Frontend-Cidadao-Fluxo-Cadastro-de-Conta|Fluxo-Cadastro-de-Conta]]).
- ✅ Credenciais de login ficam apenas em memória (`UsuarioService.setLoginUsuario`), para reautenticar após o desbloqueio; `POST security/auth` é chamado de novo no fim do desafio.

### 3. Pós-login
- ✅ `validacao/gerenciar-validacao` consulta `GET usuario` e abre, se necessário, o aceite da política LGPD ou a troca de senha; depois navega ao `returnUrl` ou à home ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/08-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]]).

### 4. Recuperação de senha
- ✅ `conta/recuperar-senha` → `POST usuario/recuperar-senha`; `conta/redefinir-senha` → `POST usuario/concluir-recuperacao-senha`; mensagens em `conta/mensagem-redefinir-senha`. Alteração logada: `POST usuario/alterar-senha`.

### 5. Logout
- ✅ `/logout` limpa o `localStorage` local e volta à home; não chama o backend.

## Inferências e limitações
- 🔶 As faixas `ExceptionDetails.Id` 1 e 5 correspondem a "usuário/PJ bloqueado por dados inconsistentes"; o significado vem do backend e deve ser conferido em [[01-Sistemas/PARTICIPA-DF/Backend/04-Regras-de-Negocio/PARTICIPA-DF-Backend-Regra-Bloqueio-de-Usuario|Bloqueio-de-Usuario]].
- 🔶 Se o erro do login não trouxer `ExceptionDetails` (ex.: falha de rede), `e.error.ExceptionDetails.Id` pode lançar exceção no callback (acesso sem verificação nula).
- ❓ O texto das mensagens de erro de credenciais inválidas vem do interceptor (`BadRequest`), não do componente.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Chamadas-de-API|Chamadas-de-API]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/03-Modulos/PARTICIPA-DF-Frontend-Cidadao-Rotas-e-Telas|Rotas-e-Telas]]

## Pendências e próximo passo
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]].
