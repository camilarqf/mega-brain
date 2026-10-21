---
type: reference
system: Portal-Transparencia
component: Frontend
repository: portal-transparencia-frontend
status: confirmado
coverage: parcial
analyzed_commit: dca3e933ffd7e5bbfd173133e88d14f94304cb52
updated: 2026-10-21
tags:
  - portal-transparencia
  - frontend
  - build
  - ambientes
sources:
  - config.json
  - src/app/config.js
  - gulp/environment.js
  - gulp/conf.js
  - gulpfile.js
  - Dockerfile
  - docker-compose.yml
  - nginx.conf
  - sbin/start.sh
---

# Frontend — build e perfis de ambiente

Voltar: [[01-Sistemas/Portal-Transparencia/Frontend/Portal-Transparencia-Frontend-Index|Índice do Frontend]]

> Por regra do cofre, **valores de URL, hosts e IPs não são reproduzidos**; só nomes de chaves e a forma de composição.

## Objetivo
Explicar como o frontend é construído e como cada ambiente aponta para suas APIs.

## Evidências
Commit `dca3e933`. Arquivos: `config.json`, `src/app/config.js`, `gulp/environment.js`, `gulp/conf.js`, `gulpfile.js`, `Dockerfile`, `docker-compose.yml`, `nginx.conf`, `sbin/start.sh`, `README.md`.

## Informações confirmadas
**Perfis.** `config.json` tem os perfis `local`, `teste` e `homologacao` (e outros além desses não foram lidos; ❓ não confirmado se existe um perfil de produção). A tarefa `environmentSetup` (`gulp-ng-config`) gera o módulo `portal.config` em `src/app/config.js` com o perfil de `--profile <nome>` (padrão `local`).

**Chaves de configuração (constantes AngularJS):**
| Constante | Uso no código |
|---|---|
| `api` | URL-base da API do Backend; usada por todos os serviços e pelo interceptador |
| `apisuperbusca` | URL-base do serviço de busca (`SuperBuscaService`) |
| `apiGerenciador` | URL-base de um "gerenciador" usada em Quadros Temáticos e Setor Desejado |
| `caminhoImagens`, `caminhoArquivos`, `caminhoDadosAbertos` | prefixos de URL de objetos (imagens, arquivos, dados abertos) montados em `ArquivoUrlService` |

No perfil `homologacao` as constantes `api`, `apisuperbusca`, `caminhoImagens` e `caminhoArquivos` são **caminhos relativos** (`/api`, `/api-super-busca`, `/arquivos/portal-imagens/`, `/arquivos/portal-arquivos/`), o que indica um *reverse proxy* na frente da aplicação (🔶, a configuração do proxy não está neste repositório). O perfil `local` usa endereços absolutos.

**Comandos** (`README.md`, `package.json`): `npm install && bower install`; `gulp serve`, `gulp serve:dist`, `gulp test`, `gulp test:auto`, `gulp protractor`; `gulp --profile <perfil>`; `npm run dev` = `gulp --dev --skip-lint`.

**Container.** `Dockerfile` (`node:6.11.3`) instala dependências, copia o código e roda `gulp --profile ${profile} --skip-lint`, gerando `dist/`. `nginx.conf` serve `/usr/share/nginx/html` com *fallback* para `index.html`. `docker-compose.yml` e `sbin/start.sh` são para desenvolvimento (`gulp --dev`).

**Mocks.** `db.json` e `routes.json` (dados de exemplo de `despesa-categoria`, `despesa-credor` …) sugerem uso de `json-server` em desenvolvimento antigo; não há dependência `json-server` no `package.json`.

## Falhas e dependências
- `src/app/config.js` **é versionado** e foi alterado nos commits `cc44e3f1` e `21068a92` (2026-10-20/21, ramo `feature/refatoracao-acesso-minio`). Como contém endereços de infraestrutura, ver [[01-Sistemas/Portal-Transparencia/Frontend/05-Seguranca/Portal-Transparencia-Frontend-Seguranca-e-Privacidade|Segurança e privacidade]].
- Sem pipeline versionado (ver [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Stack-e-Dependencias|Stack]]).

## Inferências e limitações
- 🔶 Qual perfil é usado em produção e como o proxy mapeia `/api`, `/api-super-busca` e `/arquivos/*` não é evidenciável pelo repositório.
- 🔶 `caminhoImagens/Arquivos/DadosAbertos` apontam para *buckets* de armazenamento de objetos (nomes `portal-imagens`, `portal-arquivos`, `portal-dados-abertos` no sufixo); a relação com o MinIO documentado no cofre ([[01-Sistemas/MinIO-CGDF/MinIO-CGDF-Index|MinIO-CGDF]]) não está confirmada.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Frontend/01-Visao-Geral/Portal-Transparencia-Frontend-Arquitetura-AngularJS|Arquitetura]] · [[01-Sistemas/Portal-Transparencia/Frontend/04-API-e-Integracoes/Portal-Transparencia-Frontend-Integracoes-Externas|Integrações externas]]
- Backend: [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Portal-Transparencia/Frontend/99-Controle/Portal-Transparencia-Frontend-Pendencias|Pendências]].
