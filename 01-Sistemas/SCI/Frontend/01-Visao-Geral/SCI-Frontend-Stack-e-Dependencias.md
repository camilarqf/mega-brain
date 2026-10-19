---
type: reference
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
  - stack
sources:
  - package.json
  - angular.json
  - Dockerfile
  - tsconfig.json
---
# SCI Frontend — stack e dependências

Voltar: [[01-Sistemas/SCI/Frontend/SCI-Frontend-Index|Índice do Frontend]]

## Objetivo
Registrar linguagem, framework, bibliotecas e empacotamento do `sci-frontend`.

## Evidências
- `package.json` (nome do pacote `sci-novo`), `angular.json` (projeto `cgdf-web`, saída `dist/novo-sci`), `Dockerfile`, `.jenkins-pipelines/`.

## Informações confirmadas
| Item | Valor |
|---|---|
| Framework | ✅ Angular 18.2 (NgModules; componentes lidos com `standalone: false`), TypeScript ~5.5, RxJS ~7.8, zone.js |
| Estado | ✅ NgRx 18 (`store`, `effects`, `store-devtools`) |
| UI | ✅ Angular Material 18 e CDK, PrimeNG 17 (`primeicons`), Bootstrap 5.3 (ícones `bi`), `ng-select`, `ngx-pagination`, `ngx-spinner`, `ngx-mask` |
| Editores e documentos | ✅ CKEditor 5 (build classic), Quill 2 (componente `text-editor`), `ng2-pdf-viewer` |
| Sessão | ✅ `ngx-cookie-service`; `jwt-decode` declarado |
| Utilitários | ✅ `uuid` |
| Testes | ✅ Karma + Jasmine configurados; **nenhum** `*.spec.ts` (ver [[01-Sistemas/SCI/Frontend/06-Qualidade/SCI-Frontend-Testes-e-Cobertura|Testes]]) |
| Configurações de build | ✅ `development` (padrão), `homolog` e `production`, cada uma trocando `environment.ts` por `environment.dev/hom/prod.ts`; `production` com orçamento inicial de 2 MB (aviso) e 6 MB (erro) |
| Empacotamento | ✅ `Dockerfile` em duas etapas (Node 22 Alpine, `npm install --force`, `ng build --configuration=<profile>`); pipelines Jenkins `development`, `homolog` e `prod` copiam o resultado para servidores de destino (endereços omitidos) |

## Inferências e limitações
- 🔶 `sci-novo` aparece também como dependência `"file:"` do próprio pacote (provável artefato de instalação; uso não verificado).
- ❓ O uso de `jwt-decode` não foi procurado nos arquivos.
- Versões resolvidas ficam em `package-lock.json` (não lido). `ng build` e `ng test` não foram executados.

## Relacionamentos
- [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Arquitetura|Arquitetura]] · [[01-Sistemas/SCI/Frontend/01-Visao-Geral/SCI-Frontend-Perfis-e-Ambientes|Perfis e ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SCI/Frontend/99-Controle/SCI-Frontend-Pendencias|Pendências]].
