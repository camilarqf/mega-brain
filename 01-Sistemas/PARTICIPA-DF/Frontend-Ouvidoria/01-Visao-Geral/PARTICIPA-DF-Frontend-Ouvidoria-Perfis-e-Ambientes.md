---
type: reference
system: PARTICIPA-DF
repository: participa-df-ouv-frontend
status: confirmado
coverage: parcial
analyzed_commit: 9d8ecdb6b027b5283d71cee49bc40aa452be6afe
updated: 2026-10-18
tags:
  - participa-df
  - frontend-ouvidoria
  - ambientes
  - build
  - deploy
sources:
  - api.config.json
  - gulpfile.js
  - Dockerfile
  - Dockerfile.dev
  - docker-compose.yml
  - .jenkins-pipelines/Jenkinsfile.homolog
  - .jenkins-pipelines/Jenkinsfile.prod
  - Properties/PublishProfiles
  - .gitignore
---

# Frontend Ouvidoria — perfis e ambientes

Voltar: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/PARTICIPA-DF-Frontend-Ouvidoria-Index|Índice do Frontend Ouvidoria]] · Stack: [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/01-Visao-Geral/PARTICIPA-DF-Frontend-Ouvidoria-Stack-e-Dependencias|Stack-e-Dependencias]]

## Objetivo
Registrar perfis de build, configuração por ambiente e o caminho de implantação, sem reproduzir endereços.

## Evidências
Arquivos em `sources`, commit `9d8ecdb`. Endereços de API, serviços e servidores de deploy foram omitidos (infraestrutura interna).

## Informações confirmadas

### Configuração por ambiente
`api.config.json` define três perfis, com as mesmas duas chaves:

| Perfil | Chaves | Observação |
|---|---|---|
| `local` | `urlApi`, `urlApiCgdfLocalization` | API em `localhost`; serviço de localização em endereço IP interno, sem HTTPS |
| `homologacao` | idem | API e serviço de localização por HTTP |
| `producao` | idem | API e serviço de localização por HTTPS |

O Gulp (`gulp-ng-config`) transforma o perfil escolhido na constante `configService` em `app/api.config.js`. ⚠️ O arquivo gerado `app/api.config.js` está **versionado** com o perfil `local` (e `app/views-dist.js`, de ~427 KB, também).

### Perfis de build
| Comando | Tarefa Gulp | Saída | Observação |
|---|---|---|---|
| `npm run dev` | `dev` | `public/build` + BrowserSync | perfil `local`; `Dockerfile.dev`/`docker-compose` sobem o mesmo comando |
| `npm run homolog` | `homolog` | `public/dist` | copia `Web.config`, `auth.html`, favicon |
| `npm run prod` | `prod` | `public/dist` | copia `Web.Producao.config` como `Web.config` |

⚠️ `Web.config`, `Web.Producao.config` e `auth.html` são exigidos pelas tarefas `copy-web-config*` e `copy-auth`, mas **não existem** no repositório (não versionados ou ausentes). `viewsCacheSetup` também troca `/assets/img/` por `/images/` nos templates.

### Pipeline de implantação (Jenkins)
- ✅ `.jenkins-pipelines/Jenkinsfile.homolog` e `Jenkinsfile.prod`: constroem a imagem Docker (`Dockerfile`, `--build-arg profile=<prod|homolog>`), extraem `public/dist` do contêiner e copiam o resultado para **dois** destinos de compartilhamento de rede Windows por ambiente (`.../ouv-participa-df`), com credencial do Jenkins.
- ✅ O `Dockerfile` roda `gulp ${profile}`; o contêiner não serve a aplicação — só gera os arquivos estáticos.
- 🔶 O `Web.config` copiado indica hospedagem em IIS; não confirmado (arquivo ausente).
- ✅ `Properties/PublishProfiles/{Homologacao,Producao,Treinamento}.pubxml` são perfis de publicação por sistema de arquivos do Visual Studio (legado); há um ambiente `Treinamento` sem equivalente em `api.config.json` nem em Jenkinsfile.

## Inferências e limitações
- ❓ Qual perfil/ambiente corresponde ao `Treinamento` e se ainda é usado.
- Cobertura `parcial`: o conteúdo dos `.pubxml` e a sequência completa dos estágios Jenkins não foram lidos linha a linha.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/07-Integracoes/PARTICIPA-DF-Frontend-Ouvidoria-Integracoes-Externas|Integracoes-Externas]] · [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/09-Qualidade/PARTICIPA-DF-Frontend-Ouvidoria-Debitos-Tecnicos|Debitos-Tecnicos]] · Comparação: [[01-Sistemas/PARTICIPA-DF/Frontend-Cidadao/01-Visao-Geral/PARTICIPA-DF-Frontend-Cidadao-Perfis-e-Ambientes|Perfis do Frontend Cidadão]]

## Pendências e próximo passo
- Confirmar onde ficam `Web.config` e `auth.html` e se o destino é IIS. Ver [[01-Sistemas/PARTICIPA-DF/Frontend-Ouvidoria/99-Controle/PARTICIPA-DF-Frontend-Ouvidoria-Pendencias|Pendências]].
