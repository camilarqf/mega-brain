---
type: reference
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
tags:
  - ingress
  - nginx
  - deploy
  - ambientes
sources:
  - Dockerfile
  - .jenkins-pipelines/deployment.params.yml
  - ".jenkins-pipelines/deployment.params copy.yml"
  - .jenkins-pipelines/homolog.env.yml
  - .jenkins-pipelines/nonprod.env.yml
  - .jenkins-pipelines/prod.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/staging.env.yml
---
# INGRESS-CGDF — build, deploy e ambientes

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Mostrar como a imagem é construída, qual `ENVIRONMENT` cada ambiente recebe e como o contêiner é implantado.

## Evidências
- `.jenkins-pipelines/*.yml`. Os arquivos só têm parâmetros; o pipeline Jenkins em si não está no repositório. Identificadores de credencial e endereços não são reproduzidos aqui.

## Informações confirmadas
**Build**: `docker build` do `Dockerfile` da raiz; imagem `nginx-ingress-controller-img` (`image_definition`). Branch principal `master`. Health check de integração: `healthcheck`.

**Valores de `ENVIRONMENT` e configuração escolhida** (`Dockerfile`):

| Valor | Configuração |
|---|---|
| `production`, `prod` | `nginx.conf` (rotas de `locations/prod`) |
| `nonprod`, `nonproduction`, `staging`, `sandbox`, `homolog`, `homologacao` | `nginx-nonprod.conf` (rotas de `locations/nonprod`, com `/staging/` e `/sandbox/`) |

**Arquivos de ambiente do pipeline**:

| Arquivo | `ENVIRONMENT` | Usado por |
|---|---|---|
| `nonprod.env.yml` | `nonprod` | Staging e Sandbox em `deployment.params.yml` |
| `prod.env.yml` | `production` | Produção (os dois arquivos de parâmetros) |
| `homolog.env.yml` | `sandbox` | só `deployment.params copy.yml` (Homolog) |
| `sandbox.env.yml`, `staging.env.yml` | `nonproduction`, `staging` | ✅ nenhum arquivo de parâmetros os referencia |

**Implantação** (`deployment.params.yml`): todos com 2G de memória, 1 réplica, logs rotativos (5 arquivos de 5 MB) e rede `nginx-ingress-network`.

| Região | Cluster | Restrição | Nome do contêiner | Porta interna → externa |
|---|---|---|---|---|
| Staging | `nonprod-cluster-1` | label `env==staging` | `nginx-ingress-controller-nonprod-2` | 80 → 8080 |
| Sandbox | `nonprod-cluster-1` | label `env==sandbox` | `nginx-ingress-controller-nonprod-2` | 80 → 8080 |
| Produção | `prod-cluster` | `role: worker` | `nginx-ingress-controller-2` | 8080 → 8080 |

- ✅ `deployment.params copy.yml` é uma versão anterior (contêiner `nginx-ingress-controller`, 3 réplicas, porta interna 80, regiões Homolog e Produção). Está versionada.
- ✅ A porta `5672` do proxy TCP não aparece nos parâmetros de portas.

## Inferências e limitações
- 🔶 Staging e Sandbox têm o mesmo nome de contêiner e se distinguem pelo label do nó, provavelmente sendo instâncias separadas por nó/serviço. Não confirmado.
- 🔶 A porta 5672 deve ser alcançada pela rede `nginx-ingress-network`, não por porta publicada. Não confirmado.
- ❓ Pipeline Jenkins, domínios por ambiente e o repositório da biblioteca de pipeline não estão no repositório.

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Arquitetura|Arquitetura]] · [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Deploy-e-Ambientes|Deploy do MinIO-CGDF]] (também usa a rede `nginx-ingress-network`)

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
