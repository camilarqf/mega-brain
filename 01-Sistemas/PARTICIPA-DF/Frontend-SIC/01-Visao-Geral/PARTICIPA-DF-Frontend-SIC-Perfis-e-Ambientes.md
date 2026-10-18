---
type: reference
system: PARTICIPA-DF
repository: participa-df-sic-frontend
status: confirmado
coverage: parcial
analyzed_commit: 5518a8141d83784eab17ebe61d84331d842add2c
updated: 2026-10-18
tags:
  - participa-df
  - frontend-sic
  - ambientes
  - build
  - deploy
sources:
  - api.config.json
  - app/api.config.js
  - app/api-dist.config.js
  - gulpfile.js
  - Dockerfile
  - nginx.conf
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/staging.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/prod.env.yml
---

# Frontend SIC — perfis, ambientes e build

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/PARTICIPA-DF-Frontend-SIC-Index|Índice do Frontend SIC]] · Stack: [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Stack-e-Dependencias|Stack-e-Dependencias]]

## Objetivo
Registrar como a aplicação é configurada, compilada e publicada. **Endereços e valores de variáveis foram omitidos**; só nomes de chaves.

## Evidências
Arquivos em `sources`, commit `5518a81`. Os valores dos `*.env.yml` não foram lidos nem reproduzidos.

## Informações confirmadas

### Configuração por ambiente (`api.config.json`)
| Perfil | Chave | Observação |
|---|---|---|
| `local` | `configService.urlApi` | endereço absoluto (omitido), HTTP |
| `homologacao` | `configService.urlApi` | relativo: `api/` |
| `producao` | `configService.urlApi` | relativo: `api/` |

- ✅ Em `homologacao` e `producao` a API é chamada por caminho relativo (`api/`), resolvido pelo `nginx` do contêiner, que repassa ao backend (`BACKEND_TARGET`). Em `local` o navegador fala direto com o backend.
- ✅ `app/api.config.js` (gerado com `local` por `gulp dev`) e `app/api-dist.config.js` (gerado por `gulp homolog`/`gulp prod`) **estão versionados** — ambos definem a constante `configService`. O arquivo `api-dist.config.js` versionado contém um endereço absoluto (omitido).

### Build (Gulp 3)
- ✅ `gulp dev`: gera `app/api.config.js`, concatena libs/scripts/CSS em `public/build` e abre `browser-sync`.
- ✅ `gulp homolog` e `gulp prod` (mesma sequência; muda o perfil do `ng-config` e o arquivo de configuração copiado): `viewsCacheSetup` (templates → `views-dist.js`), configuração de ambiente, limpeza, `libs-dist`/`scripts-dist`/`sheets-dist` (concatena, minifica e `gulp-rev`), fontes, imagens, `favicon.ico`, `Web.config`, `index.html` com nomes versionados e `auth.html`. A saída fica em `public/dist`.
- ❓ `gulpfile.js` copia `Web.config`, `Web.Producao.config` e `auth.html`, que **não existem** no repositório (herança do front de Ouvidoria/IIS). 🔶 Com o Gulp 3 a ausência de arquivos literais não costuma gerar erro (não executado).
- ✅ O `Dockerfile` executa `gulp ${profile}` com `profile=prod` por padrão e copia `public/dist` para o `nginx`.

### Execução (nginx)
- ✅ `nginx.conf` é *template*: variáveis `BASE_HREF` e `BACKEND_TARGET`; `proxy_pass` de `${BASE_HREF}api/*` para o backend; `try_files ... /index.html` (fallback de SPA); `client_max_body_size 25M`; reescrita de `src`/`href`/`url()` iniciados por `/assets/`, `/webfonts/` e `/images/` para o `BASE_HREF` (`sub_filter`).
- ✅ Há regras fixas para o prefixo `/participa-df-sic-test/` (base e `api/`), além do `BASE_HREF`.
- ✅ `app/auth/auth-ctrl.js` (commit `5bf484a`, 2026-10-14) redireciona após o login para `window.location.pathname`, preservando o subcaminho em ambientes servidos sob `BASE_HREF`.

### Pipeline (Jenkins/contêiner) — `.jenkins-pipelines`
| Região | Contêiner | Memória | Réplicas | Cluster |
|---|---|---|---|---|
| Staging | `participa-df-sic-frontend-staging` | 256M | 1 | `nonprod-cluster-1` |
| Sandbox | `participa-df-sic-frontend-sandbox` | 256M | 1 | `nonprod-cluster-1` |
| Producao | `participa-df-sic-frontend` | 1G | 2 | `prod-cluster` |

- ✅ Cada `*.env.yml` define as variáveis `ENVIRONMENT`, `BASE_HREF` e `BACKEND_TARGET` (valores omitidos). Porta interna 80; *health check* em `/`; rede `nginx-ingress-network`.
- ✅ Nome do aplicativo no pipeline: `Participa DF Sic Frontend`; imagem `participa-df-sic-frontend-img`; ramo principal `master`.

## Inferências e limitações
- 🔶 `ENVIRONMENT` não é lida pelo `Dockerfile` nem pelo `nginx.conf`; o perfil do build vem do argumento `profile` (padrão `prod`). Se o pipeline não passar `--build-arg profile`, **todas as regiões recebem o build `prod`**; como `homologacao` e `producao` usam o mesmo `urlApi` relativo, a diferença é irrelevante hoje.
- ❓ Se `ENVIRONMENT` é usada pelo pipeline Jenkins (fora do repositório).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/01-Visao-Geral/PARTICIPA-DF-Frontend-SIC-Arquitetura|Arquitetura]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/06-Qualidade/PARTICIPA-DF-Frontend-SIC-Debitos-Tecnicos|Debitos-Tecnicos]] · [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/04-API-e-Integracoes/PARTICIPA-DF-Frontend-SIC-Integracoes-Externas|Integracoes-Externas]]

## Pendências e próximo passo
- Confirmar com o time o uso de `ENVIRONMENT`, a existência de `Web.config`/`auth.html` e o objetivo do prefixo `/participa-df-sic-test/`. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-SIC/99-Controle/PARTICIPA-DF-Frontend-SIC-Pendencias|Pendências]].
