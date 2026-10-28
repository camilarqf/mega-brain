---
type: reference
aliases:
  - "Build e perfis de ambiente — Gerenciador-Portal Frontend"
system: Gerenciador-Portal
component: Frontend
repository: gerenciador-portal-frontend
status: confirmado
coverage: parcial
analyzed_commit: d6a737a3a0e5cf1b245aa35c81321638dd0cbecc
created: 2026-10-27
updated: 2026-10-27
sources:
  - config.json
  - gulpfile.js
  - gulp/conf.js
  - gulp/environment.js
  - gulp/build.js
  - Dockerfile
  - src/app/config.js
  - src/index.html
---
# Build e perfis de ambiente — Gerenciador-Portal Frontend

Voltar: [[01-Sistemas/Gerenciador-Portal/Frontend/Gerenciador-Portal-Frontend-Index|Índice do Frontend]]

## Objetivo
Explicar como o frontend é construído e como as URLs de cada ambiente entram no código. **Endereços e IPs foram omitidos de propósito** (seção 10 do `BRAIN-RULES.md`); só constam nomes de chaves.

## Evidências
`config.json`, `gulp/environment.js`, `gulp/conf.js`, `gulp/build.js`, `Dockerfile`, `src/app/config.js`, `src/index.html`.

## Informações confirmadas
### Fluxo de build
- ✅ Tarefa `build` = `environmentSetup`, `html`, `scripts`, `styles`, `assets`; a tarefa padrão limpa `dist/` e roda `build` (ou `serve:dev` com `--dev`; `npm run dev` usa `--dev --skip-lint`).
- ✅ `environmentSetup` lê `config.json` e gera `src/app/config.js`, módulo `gerenciadorPortal.config`, com **as constantes do perfil** escolhido por `--profile` (padrão `local`).
- ✅ Os templates HTML viram `views.js` (`$templateCache`, raiz `app`); a página `src/index.html` carrega `scripts/vendor.min.js`, `scripts/app.min.js` e `views.js`.
- ✅ `Dockerfile`: `node:6.11.3`; `npm install`, `bower install`, copia o código e roda o gulp com `--profile ${profile}` (argumento de build `profile`) e `--skip-lint`. **Não há** servidor web, `CMD` nem `ENTRYPOINT` no `Dockerfile`: como os arquivos de `dist/` são servidos não está no repositório (❓).

### Perfis (`config.json`)
| Perfil | Constantes definidas | Observação |
|---|---|---|
| `local` | `api`, `apiPortal`, `apiSuperbusca`, `route`, `caminhoArquivos`, `caminhoImagens` | URLs absolutas; `api` aponta para a porta 8080 local |
| `teste` | `api` | valor de exemplo; os demais não existem |
| `homologacao` | as seis | `api` = `/api` (relativo); `caminhoArquivos` e `caminhoImagens` relativos (`/arquivos/...`); `apiPortal` e `apiSuperbusca` absolutos (sandbox) |
| `producao` | as seis | `api` = `/api` e `caminho*` relativos; `apiPortal` e `apiSuperbusca` no domínio público do Portal |

- ✅ Nos perfis `homologacao` e `producao`, `api` e os `caminho*` são **relativos**: o navegador chama o mesmo host de onde a SPA foi servida. 🔶 Portanto existe um proxy reverso na frente (por exemplo o `INGRESS-CGDF`) que encaminha `/api` ao backend e `/arquivos/<bucket>` ao MinIO; não confirmado no repositório.
- ✅ `route.uri` é vazio em todos os perfis; o `navbar` o usa como prefixo dos links `#!/…` (comentários no HTML falam em adicionar `/gerenciador/` na produção).
- ✅ `src/app/config.js` **está versionado**, apesar de gerado, e está desatualizado em relação ao perfil `local` atual do `config.json` (o `caminhoArquivos` e o `caminhoImagens` apontam para outro host/porta). O próximo `gulp` o sobrescreve.

## Falhas e dependências
- O perfil `teste` não tem `apiPortal` etc.; construir com ele deixa as constantes injetadas em `exclusoesAPI` indefinidas (o AngularJS falha na injeção).
- ❓ Como o pipeline escolhe `--profile` e onde a SPA é publicada (não há pipeline neste repositório).

## Inferências e limitações
Leitura estática; o build não foi executado.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Frontend/01-Visao-Geral/Gerenciador-Portal-Frontend-Stack-e-Dependencias|Stack]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Perfis-e-Ambientes|Perfis do Backend]] · [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Deploy-e-Pipeline|Deploy do Backend]]

## Pendências e próximo passo
- Confirmar com o time o proxy reverso e o pipeline de publicação (pendência 3 do [[01-Sistemas/Gerenciador-Portal/Frontend/99-Controle/Gerenciador-Portal-Frontend-Pendencias|controle]]).
