---
type: quality
system: SICI
repository: sici-frontend
status: confirmado
coverage: completa
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - testes
  - cobertura
sources:
  - angular.json
  - tsconfig.spec.json
  - src/app/components/layout/botoes/botao-acao/botao-acao.component.spec.ts
  - src/core/services/interceptor/http-token.service.spec.ts
  - src/core/services/keycloak/keycloak.service.spec.ts
  - src/core/services/token/token.service.spec.ts
---

# Testes e cobertura — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]] · Backend: [[01-Sistemas/SICI/Backend/09-Qualidade/SICI-Backend-Testes-e-Cobertura|Testes do Backend]]

## Objetivo
Registrar o que existe de teste automatizado no frontend e o que não é coberto.

## Evidências
Arquivos em `sources`. Executados em 2026-10-18 no commit `418642f` (Chrome Headless 155, Windows): `ng test` e `ng build --configuration=production`. Saídas e arquivos temporários removidos; o repositório não foi alterado.

## Informações confirmadas ✅
- Ferramentas: Karma + Jasmine (`karma-coverage` instalado); `ng test` usa `tsconfig.spec.json` (inclui `src/**/*.spec.ts`). Não há `karma.conf.js` próprio (configuração padrão do Angular CLI) nem relatório de cobertura configurado.
- Existem **4** arquivos `.spec.ts`, cada um com **um** teste (`should create`/`should be created`), 71 linhas no total:

| Spec | Alvo |
|---|---|
| `botao-acao.component.spec.ts` | componente de botão de ação |
| `http-token.service.spec.ts` | interceptor de token |
| `keycloak.service.spec.ts` | `KeycloakService` (código sem uso) |
| `token.service.spec.ts` | `TokenService` (código sem uso) |

### Resultado da execução ✅
- **`ng build --configuration=production`**: concluiu com sucesso. Avisos: orçamento excedido na folha de fontes do Google (333,8 kB e 340,9 kB, limite 307,2 kB), módulos CommonJS do CKEditor (`fuzzysort`, `color-convert`, `color-name`) e 9 regras CSS ignoradas por seletor inválido (Bootstrap/CKEditor).
- **`ng test` (comando padrão): não roda.** Erro de compilação TS2339 em `keycloak.service.ts` (`environment.keycloak` não existe), 4 ocorrências. O Karma aborta com `Found 1 load error` e nenhum teste executa. `--exclude` do spec não resolve (o arquivo continua no `tsconfig.spec.json`).
- **Execução alternativa** (tsconfig temporário fora do repositório, sem o Keycloak, e `--include` dos outros 3 specs): **3 testes, 1 passou, 2 falharam**.

| Spec | Resultado | Causa |
|---|---|---|
| `TokenService` | ✅ passou | — |
| `BotaoAcaoComponent` | ❌ falhou | `NG0303`: `pTooltip` não é propriedade conhecida de `i` (o teste não importa o módulo do tooltip do PrimeNG) |
| `HttpTokenService` | ❌ falhou | `NullInjectorError`: sem provider de `HttpClient` (via `AuthService`) |
| `KeycloakService` | ⛔ não compila | `environment.keycloak` inexistente |

- **Cobertura (3 specs rodados):** instruções 5,26% (15/285), ramos 0%, funções 0%, linhas 5%. Medida só sobre o código carregado por esses testes, não sobre a aplicação inteira.

- Nenhum teste cobre telas, serviços HTTP, reducers/efeitos, guards ou o fluxo de assinatura.
- Não há testes de ponta a ponta (o `README` cita `ng e2e`, sem pacote configurado).

## Inferências e limitações
- O `ng test` quebra só porque o `tsconfig.spec.json` inclui todos os `.spec.ts` e o do Keycloak importa código que não compila; o `tsconfig.app.json` compila só o que `main.ts` alcança, por isso o `ng build` passa. Remover ou corrigir o código do Keycloak destravaria a suíte (decisão do time).
- A cobertura percentual da aplicação inteira é desconhecida: a suíte não roda no comando padrão.
- Os testes não protegem os pontos de maior risco: guards, reautenticação na assinatura e transições de status ([[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]]).

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
