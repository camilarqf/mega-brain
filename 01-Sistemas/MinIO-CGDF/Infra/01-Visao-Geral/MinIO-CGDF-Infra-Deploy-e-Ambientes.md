---
type: reference
system: MinIO-CGDF
component: Infra
repository: minio-infra
status: confirmado
coverage: completa
analyzed_commit: f36efc5fa586f71a2f964f0f3a51a8b9383d84d2
updated: 2026-10-21
tags:
  - minio
  - deploy
  - ambientes
sources:
  - config/production/stack.yml
  - config/staging/stack.yml
  - config/sandbox/stack.yml
---
# MinIO CGDF — deploy e ambientes

Voltar: [[01-Sistemas/MinIO-CGDF/Infra/MinIO-CGDF-Infra-Index|Índice da Infra]]

## Objetivo
Comparar os três ambientes. Endereços de armazenamento e valores de segredos não são reproduzidos.

## Evidências
- Os três `config/<ambiente>/stack.yml`.

## Informações confirmadas
| Aspecto | Produção | Staging | Sandbox |
|---|---|---|---|
| `x-platform-info.stack_name_prefix` | `production-minio-stack` | `staging-minio-stack` | `sandbox-minio-stack` |
| `image_name` | `minio-production-img` | `minio-staging-img` | `minio-sandbox-img` |
| `hostname` | `minio-production` | `minio-staging` | `minio-sandbox` |
| Restrição de placement | `node.role == worker` | `node.hostname == nonprod-staging` | `node.hostname == nonprod-sandbox` |
| Secret da senha raiz (nome) | `minio-root-pwd-v1` | `stg-minio-root-pwd-v1` | `sbx-minio-root-pwd-v1` |
| Portas publicadas (host:contêiner) | `9002:9000`, `9001:9001` | `9003:9001` (somente console) | `9000:9000`, `9001:9001` |
| Healthcheck (`/minio/health/live`, 30s) | sim | **não** | sim |
| Volume `minio-data` | driver `local` com opções NFS | volume local padrão | volume local padrão |
| Réplicas | 1 | 1 | 1 |

- ✅ Todos usam `docker_file: .docker/Dockerfile` e `image: ${IMAGE_NAME}`.
- ✅ Healthcheck: `curl -f http://localhost:9000/minio/health/live`, intervalo 30s, timeout 10s, 3 tentativas, `start_period` 30s.

## Inferências e limitações
- 🔶 Em staging a API (9000) não é publicada no host; o acesso a ela só seria possível pela rede interna.
- ❓ URLs expostas por ambiente, o NFS (endereço e volume omitidos) e o pipeline não estão no repositório.

## Relacionamentos
- [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Arquitetura|Arquitetura]] · [[01-Sistemas/MinIO-CGDF/Infra/09-Qualidade/MinIO-CGDF-Infra-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Registrar URLs por ambiente se o usuário informar. Ver [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Pendencias|Pendências]].
