---
type: reference
system: SICI
repository: sici-frontend
status: confirmado
coverage: parcial
analyzed_commit: 418642ffc9bc8481878633a73aff6fe60b41140a
updated: 2026-10-18
tags:
  - sici
  - frontend
  - ambientes
  - build
  - deploy
sources:
  - angular.json
  - src/environments/environment.ts
  - src/environments/environment.development.ts
  - src/environments/environment.homolog.ts
  - src/environments/environment.prod.ts
  - .docker/Dockerfile
  - nginx.conf
  - .jenkins-pipelines/Jenkinsfile.development
  - .jenkins-pipelines/Jenkinsfile.homolog
  - .jenkins-pipelines/Jenkinsfile.prod
  - .jenkins-pipelines/deployment.params.yml
---

# Perfis de build e ambientes — SICI Frontend

Voltar: [[01-Sistemas/SICI/Frontend/SICI-Frontend-Index|Índice do Frontend]] · Relacionado: [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Stack-e-Dependencias|Stack-e-Dependencias]], [[01-Sistemas/SICI/Frontend/07-Integracoes/SICI-Frontend-Integracoes|Integracoes]] · Backend: [[01-Sistemas/SICI/Backend/01-Visao-Geral/SICI-Backend-Perfis-e-Ambientes|Perfis do Backend]]

> Não são reproduzidos endereços, IPs de servidores de deploy, nomes de credenciais nem valores de variáveis. Só nomes de chaves.

## Objetivo
Registrar como o frontend é configurado, empacotado e implantado em cada ambiente.

## Evidências
Arquivos em `sources`. Pipelines e Docker lidos, não executados.

## Informações confirmadas ✅
### Configurações de build (`angular.json`)
| Configuração | Substituição de ambiente | Observação |
|---|---|---|
| `production` (padrão do `build`) | `environment.prod.ts` | `outputHashing: all`; orçamentos: inicial 3 MB aviso / 6 MB erro; estilo por componente 300 kB / 500 kB |
| `homolog` | `environment.homolog.ts` | mesmos orçamentos de `production` |
| `development` | `environment.development.ts` | sem otimização, com *source map* |
| `local` (padrão do `serve`) | nenhuma: usa `environment.ts` | sem otimização; `urlApi` absoluto (endereço omitido), `production: false` |

### Chaves de `environment`
`production`, `urlApi` e, nas configurações empacotadas, `name`. Nos perfis `development`, `homolog` e `prod`, `urlApi` é `/api` (caminho relativo, resolvido pelo proxy do nginx) e `name` vale `staging`, `sandbox` e `prod`, respectivamente. Não há chave de Keycloak nos arquivos de ambiente (relevante para [[01-Sistemas/SICI/Frontend/08-Seguranca/SICI-Frontend-Seguranca-e-Sessao|Seguranca-e-Sessao]]).

### Imagem e servidor web
- `Dockerfile` em dois estágios: build com `node:20.19.2` (`npm ci --legacy-peer-deps`, `ng build --configuration=${profile} --base-href=${base_href}`, `--source-map=false`, `--stats-json`) e execução com `nginx:alpine`. Argumentos: `profile` (padrão `production`) e `base_href` (padrão `/`).
- `nginx.conf` é *template* com as variáveis `BASE_HREF` e `BACKEND_TARGET`: serve a SPA com *fallback* para `index.html`, repassa `${BASE_HREF}api/` para `BACKEND_TARGET`, reescreve `<base href>` e prefixos `/assets` e `/api` conforme o *base href* ativo (inclui tratamento do prefixo `/integra`) e desativa cache de `index.html`. Limite de corpo `10m`.

### Pipelines (`.jenkins-pipelines`)
| Pipeline | `profile` | `baseHref` | Mecanismo |
|---|---|---|---|
| `Jenkinsfile.development` | `development` | `/integra-dev/` | constrói a imagem, cria um contêiner temporário, copia os estáticos para compartilhamentos remotos (montagem CIFS com credencial do Jenkins) e remove o contêiner |
| `Jenkinsfile.homolog` | `homolog` | `/integra/` | idem |
| `Jenkinsfile.prod` | `production` | `/` | idem, com dois destinos remotos |

`deployment.params.yml`: aplicação `Integra Frontend`, imagem `integra-frontend-img`, `Dockerfile` em `.docker/`, *health check* em `/`, e três regiões (`Staging` e `Sandbox` com 1 réplica e 128 MB; `Producao` com 2 réplicas e 512 MB). Cada região lê um arquivo `*.env.yml` (`staging`, `sandbox`, `prod`) com as variáveis `BACKEND_TARGET`, `BASE_HREF` e `ENVIRONMENT`.

## Inferências e limitações
- 🔶 O nome "Integra" (aplicação no pipeline, prefixo `/integra`, imagem do logotipo) sugere que o SICI é publicado como "Integra"; o backend também usa a chave `integra.verify.secret`. Não confirmado. Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
- 🔶 Existem dois mecanismos de entrega (cópia de estáticos por Jenkinsfile para servidores e implantação de contêiner por `deployment.params.yml`); qual está ativo por ambiente não foi identificado.
- 🔶 O mapeamento do nginx para o *base href* só cita `/integra`; o pipeline de desenvolvimento usa `/integra-dev/`. O efeito não foi verificado.
- Não foram verificados os valores das variáveis nem os endereços reais.

## Relacionamentos
- [[01-Sistemas/SICI/Frontend/01-Visao-Geral/SICI-Frontend-Arquitetura|Arquitetura]] · [[01-Sistemas/SICI/Frontend/09-Qualidade/SICI-Frontend-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Ver [[01-Sistemas/SICI/Frontend/99-Controle/SICI-Frontend-Pendencias|Pendências]].
