---
type: technical-debt
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: parcial
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - debito-tecnico
  - seguranca
sources:
  - package.json
  - Dockerfile
  - src/app/core/services/authentication.service.ts
  - src/app/core/services/auth.guard.ts
  - src/app/core/interceptors/jwt.interceptor.ts
  - src/app/core/interceptors/exception-interceptor.ts
  - src/app/core/pipes/safe-pipe.ts
  - src/app/pages/login/login.component.ts
  - src/app/layout/components/upload/upload.component.ts
---

# Frontend Cidadão — débitos técnicos e riscos

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]]

## Objetivo
Separar dos fatos as **recomendações** de melhoria e os riscos. Cada item cita o fato que o originou (✅ verificado) e a recomendação (🔶).

## Evidências
Arquivos em `sources`, commit `d250804`. Gravidade: 🔴 alta · 🟠 média · 🟡 baixa. Estimativas de risco são julgamento da análise, não medições.

## Informações confirmadas (fatos)
| # | Gravidade | Fato (✅) | Recomendação (🔶) |
|---|---|---|---|
| 1 | 🔴 | O JWT fica em `localStorage` (`_userData`) e o `JwtInterceptor` o anexa a **toda** requisição, inclusive à URL externa de localização. | Restringir o `Bearer` ao `apiUrl`; avaliar cookie `HttpOnly` ou sessão no backend; revisar com o time de segurança. |
| 2 | 🔴 | Logout apenas apaga o `localStorage`; nenhuma chamada invalida o token no servidor (existe `CancelarToken` no backend). | Chamar o cancelamento de token no logout. |
| 3 | 🟠 | `storeUserDataSubApplications` usa `postMessage(token, '*')`; não há chamadas hoje. | Remover o método ou fixar o `targetOrigin`. |
| 4 | 🟠 | Login assistido: `sessionId = MD5(token)`, enviado ao backend junto com o token; MD5 não é um segredo aleatório. | Pedir ao backend um identificador de sessão aleatório de uso único. |
| 5 | 🟠 | CPF/CNPJ vão em query string (`security/count-try`, `security/check`, `check-cpf-vinculado-pj`). | Usar `POST` com corpo para documentos pessoais. |
| 6 | 🟠 | Angular 13 e Node 16 (fora de suporte); `@ng-bootstrap` em beta; build com `npm install --force`. | Planejar atualização de versão; usar `npm ci` com o lockfile. |
| 7 | 🟠 | Testes quase inexistentes (9 specs, 11 casos) — [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Testes-e-Cobertura\|Testes-e-Cobertura]]. | Cobrir `Api`, `AuthGuard`, interceptors e os fluxos de registro primeiro. |
| 8 | 🟡 | `AuthGuard`: com pendência de LGPD/senha o código navega para `gerenciar-validacao` e logo depois para `auth` (sem `return`). | Reorganizar o `if/else` para um único redirecionamento; cobrir com teste. |
| 9 | 🟡 | `login.component.ts` lê `e.error.ExceptionDetails.Id` sem checar nulo. | Usar `e?.error?.ExceptionDetails?.Id`. |
| 10 | 🟡 | `ExceptionInterceptor` não está registrado (código morto); `RequestInterceptor` importa `@angular/core/testing` (`tick`) e o compilador sem uso. | Remover importações e a classe sem uso. |
| 11 | 🟡 | `SafePipe` expõe `bypassSecurityTrust*` genérico; a página LGPD usa `innerHTML` com texto do backend. | Restringir o pipe a tipos necessários e sanitizar na origem. |
| 12 | 🟡 | Rascunhos (manifestação, pedido, credenciais) em `localStorage` sem expiração; o texto da manifestação pode conter dados sensíveis. | Definir prazo de validade e limpar no logout. |
| 13 | 🟡 | 95 usos de `any`; 148 `subscribe(` e 1 uso de `unsubscribe/takeUntil/ngOnDestroy`; 6 `console.log` (um registra `response.error` do `500`). | Tipar modelos; usar `async` pipe/`takeUntilDestroyed`; remover logs. |
| 14 | 🟡 | Nome do arquivo `pedido-state-manager.service.ts.service.ts` e `Dockerfile` com BOM; README padrão do Angular. | Renomear (com `git mv`) e escrever o README do projeto. |
| 15 | 🟡 | O envio da manifestação ocorre no construtor da tela `finalizar`, sem trava contra repetição (recarga). | Mover para ação explícita e idempotente. |

## Inferências e limitações
- 🔶 A gravidade dos itens 1, 2 e 4 depende de o backend impor expiração curta e de `is-auth` verificar cancelamento (pendência já listada no backend: [[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências do Backend]]).
- Contagens (`any`, `subscribe`) são buscas textuais, não análise estática.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/04-Seguranca/PARTICIPA-DF-Frontend-Cidadao-Seguranca-e-Sessao|Seguranca-e-Sessao]] · [[01-Sistemas/PARTICIPA-DF/Backend/08-Qualidade/PARTICIPA-DF-Backend-Debitos-Tecnicos|Débitos técnicos do Backend]]

## Pendências e próximo passo
- Priorizar com o time os itens 1 a 5 ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]).
