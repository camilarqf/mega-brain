---
type: reference
system: PARTICIPA-DF
repository: participa-df-frontend
status: confirmado
coverage: completa
analyzed_commit: d250804ce5208995296da23ccfb2c444f91da8cc
updated: 2026-10-18
tags:
  - participa-df
  - frontend-cidadao
  - stack
sources:
  - package.json
  - angular.json
  - tsconfig.json
  - Dockerfile
  - web.config
  - src/index.html
---

# Frontend Cidadão — stack e dependências

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/PARTICIPA-DF-Frontend-Cidadao-Index|Índice do Frontend Cidadão]]

## Objetivo
Registrar a tecnologia, as bibliotecas e o empacotamento do repositório `participa-df-frontend`.

## Evidências
Arquivos em `sources`, commit `d250804`. O `package.json` declara o nome `eou-df`, versão `0.0.0`; o README é o modelo padrão do Angular CLI ("EouDf").

## Informações confirmadas
| Item | Valor | Evidência |
|---|---|---|
| ✅ Framework | Angular `~13.0` (CLI `^13.2.6`), TypeScript `~4.4`, RxJS `~7.4`, zone.js | `package.json` |
| ✅ UI | Bootstrap `^5.1`, `@ng-bootstrap/ng-bootstrap` 12 (beta), `@ng-select/ng-select` 8, `bootstrap-icons`, fonte de ícones local (`icofont`) | `package.json`, `angular.json` (`styles`) |
| ✅ Formulários | Angular Forms (reativos e template), `ngx-mask` 13, `ng-otp-input` | `package.json` |
| ✅ Mapa | OpenLayers `ol` 6.12, camada base OSM | `package.json`, `ol-map.component.ts` |
| ✅ Hash | `ts-md5` (usado para o `sessionId` e para o hash do rascunho) | `app.component.ts`, `manifestacao-state-manager.service.ts` |
| ✅ Paginação | `ngx-pagination` e `angular-paginator` | `package.json` |
| ✅ Testes | Karma + Jasmine (`ng test`); ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Testes-e-Cobertura\|Testes-e-Cobertura]] | `karma.conf.js`, `package.json` |
| ✅ Build | `ng build --configuration=<profile>`; perfis `production`, `homolog` e `development`; `fileReplacements` troca `environment.ts` pelo do perfil; orçamento inicial: aviso 1,5 MB, erro 6 MB | `angular.json` |
| ✅ Imagem de build | `node:16.13.0`, `npm install --force`, `ng build` com `ARG profile`, sem `--source-map` | `Dockerfile` |
| ✅ Hospedagem | `web.config` do IIS: reescreve `api/*` para um backend (endereço omitido) e faz fallback da SPA para `/` | `web.config` |
| ✅ TypeScript | `strict: true`; `strictTemplates: false` | `tsconfig.json` |
| ✅ Recursos de terceiros no `index.html` | tag do Google Analytics (`gtag.js`); plugin de acessibilidade "Perto Digital" (o bloco aparece duas vezes no arquivo, ambos com o mesmo carregador); CSS do Bootstrap 5.0.2 via CDN (jsDelivr), além do Bootstrap local; Google Fonts (Roboto, Montserrat, Material Icons) | `src/index.html` |

## Inferências e limitações
- 🔶 O `Dockerfile` copia só `package.json` antes do `npm install`, então o `package-lock.json` (presente no repositório) não é usado na imagem.
- ❓ Quem entrega o resultado do build (pipeline, servidor) não consta no repositório.
- Os endereços dos scripts de acessibilidade e do backend não são reproduzidos aqui.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Perfis-e-Ambientes|Perfis-e-Ambientes]]
- Backend: [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Stack-e-Dependencias|Stack do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/99-Controle/PARTICIPA-DF-Frontend-Cidadao-Pendencias|Pendências]] e o débito sobre Angular 13 em [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/05-Qualidade/PARTICIPA-DF-Frontend-Cidadao-Debitos-Tecnicos|Débitos técnicos]].
