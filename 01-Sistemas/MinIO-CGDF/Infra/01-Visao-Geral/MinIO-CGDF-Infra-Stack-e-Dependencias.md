---
type: reference
aliases:
  - "MinIO CGDF — stack e dependências"
system: MinIO-CGDF
component: Infra
repository: minio-infra
status: confirmado
coverage: completa
analyzed_commit: f36efc5fa586f71a2f964f0f3a51a8b9383d84d2
updated: 2026-10-21
tags:
  - armazenamento-objetos
sources:
  - .docker/Dockerfile
  - config/production/stack.yml
  - config/staging/stack.yml
  - config/sandbox/stack.yml
---
# MinIO CGDF — stack e dependências

Voltar: [[01-Sistemas/MinIO-CGDF/Infra/MinIO-CGDF-Infra-Index|Índice da Infra]]

## Objetivo
Listar as tecnologias e dependências externas da implantação.

## Evidências
- `.docker/Dockerfile`; `config/*/stack.yml`.

## Informações confirmadas
| Item | Valor | Origem |
|---|---|---|
| Imagem base | `minio/minio:RELEASE.2025-09-07T16-13-09Z` | `.docker/Dockerfile` |
| Portas expostas pela imagem | 9000 (API) e 9001 (console) | `EXPOSE` |
| Orquestração | formato de stack (`deploy`, `secrets` externos, `placement`) compatível com Docker Swarm | `config/*/stack.yml` |
| Rede | `nginx-ingress-network`, externa | `networks` |
| Segredo | senha do usuário raiz, via Docker Secret externo, lida de arquivo (`MINIO_ROOT_PASSWORD_FILE`) | `secrets` |
| Armazenamento | volume nomeado `minio-data` em `/mnt/minio-files/data`; em produção, driver `local` com opções NFS (endereço e caminho omitidos) | `volumes` |
| Variável do pipeline | `IMAGE_NAME` (substituída na implantação) | `image: ${IMAGE_NAME}` |

## Inferências e limitações
- 🔶 O healthcheck usa `curl`; não foi verificado se a imagem o inclui.
- ❓ O pipeline de build/deploy que consome `x-platform-info` não está no repositório.

## Relacionamentos
- [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Arquitetura|Arquitetura]] · [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Deploy-e-Ambientes|Deploy e ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Pendencias|Pendências]].
