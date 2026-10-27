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
  - stack
sources:
  - Dockerfile
  - nginx.conf
  - .gitignore
---
# INGRESS-CGDF — stack e dependências

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Objetivo
Registrar tecnologias e dependências de execução.

## Evidências
- `Dockerfile` (`FROM nginx:alpine`), `nginx.conf` (diretiva `resolver`), `.gitignore` (`.idea/`, `*.iml`).

## Informações confirmadas
| Item | Valor | Evidência |
|---|---|---|
| Imagem base | `nginx:alpine` (tag flutuante, sem versão fixa) | `Dockerfile` |
| Módulos usados | `http` (proxy reverso, `rewrite`, `map`) e `stream` (TCP) | `nginx.conf` |
| Orquestração | Docker Swarm (DNS interno do Docker; rede `nginx-ingress-network`) | `nginx.conf`, `.jenkins-pipelines/deployment.params.yml` |
| CI/CD | Jenkins, parâmetros em `.jenkins-pipelines/` | ver [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Build-Deploy-e-Ambientes|Build, deploy e ambientes]] |
| Código de aplicação, gerenciador de dependências, testes | não há | árvore versionada |

- ✅ Dependências de execução: os serviços upstream (resolvidos por nome na rede Swarm) e os dois nós RabbitMQ do proxy TCP. Lista em [[01-Sistemas/INGRESS-CGDF/Nginx/06-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas]].

## Inferências e limitações
- ❓ Versão do Nginx efetivamente em uso (depende do momento do build, por causa da tag flutuante).

## Relacionamentos
- [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
