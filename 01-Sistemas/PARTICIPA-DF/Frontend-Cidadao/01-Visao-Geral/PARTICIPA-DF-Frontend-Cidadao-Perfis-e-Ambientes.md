---
type: reference
aliases:
  - "Frontend Cidadão — perfis e ambientes"
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: completa
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
sources:
  - src/environments/environment.ts
  - src/environments/environment.homolog.ts
  - src/environments/environment.prod.ts
  - angular.json
  - web.config
---

# Frontend Cidadão — perfis e ambientes

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]]

## Objetivo
Mapear os perfis de build e as chaves de configuração. **Valores e endereços não são reproduzidos** (`BRAIN-RULES.md`, seção 10).

## Evidências
Arquivos em `sources`, commit `d250804`.

## Informações confirmadas
| Perfil (`--configuration`) | Arquivo de ambiente | Chaves | Observação |
|---|---|---|---|
| (padrão `ng serve`) | `environment.ts` | `applicationName`, `production` (`false`), `apiUrl`, `apiCgdfLocalization` | `apiUrl` aponta para o backend local. |
| `homolog` | `environment.homolog.ts` | `production` (`true`), `apiUrl`, `apiCgdfLocalization` | ✅ `apiUrl` é um caminho relativo (`/api`), resolvido pela regra do `web.config`. |
| `production` | `environment.prod.ts` | `production` (`true`), `apiUrl`, `apiCgdfLocalization` | ✅ `apiUrl` é um endereço absoluto (omitido). |
| `development` | usa `environment.ts` | — | sem `fileReplacements`; `sourceMap` e sem otimização. |

- ✅ `apiCgdfLocalization` é lido somente por `ol-map.component.ts` ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/07-Integracoes/PARTICIPA-DF-Frontend-Cidadao-Integracoes-Externas|Integrações externas]]).
- ✅ `applicationName` existe só em `environment.ts`; os arquivos de homolog e prod não o definem.
- ✅ O identificador do Google Analytics está fixo no código (`app.component.ts` e `index.html`), não em ambiente.

## Inferências e limitações
- ✅ `ng build` sem `--configuration` usa `production` (`defaultConfiguration` do alvo `build`); `ng serve` usa `development`. O build `development` não troca o arquivo de ambiente.
- ❓ Qual ambiente (sandbox, staging, prod) corresponde a cada perfil no deploy: não consta no repositório.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Stack-e-Dependencias|Stack-e-Dependencias]]
- Backend: [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis e ambientes do Backend]]

## Pendências e próximo passo
- Confirmar a correspondência perfis ↔ ambientes ([[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]]).
