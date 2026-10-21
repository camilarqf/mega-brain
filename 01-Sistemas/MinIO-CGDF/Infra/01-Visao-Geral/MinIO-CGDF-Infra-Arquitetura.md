---
type: architecture
system: MinIO-CGDF
component: Infra
repository: minio-infra
status: confirmado
coverage: completa
analyzed_commit: f36efc5fa586f71a2f964f0f3a51a8b9383d84d2
updated: 2026-10-21
tags:
  - minio
  - arquitetura
sources:
  - .docker/Dockerfile
  - config/production/stack.yml
  - config/staging/stack.yml
  - config/sandbox/stack.yml
---
# MinIO CGDF — arquitetura

Voltar: [[01-Sistemas/MinIO-CGDF/Infra/MinIO-CGDF-Infra-Index|Índice da Infra]]

## Objetivo
Descrever a estrutura da implantação do MinIO.

## Evidências
- `config/*/stack.yml` (serviço `minio`) e `.docker/Dockerfile`.

## Informações confirmadas
- ✅ Um único serviço, `minio`, com `replicas: 1`, em cada ambiente.
- ✅ O comando do stack é `server /mnt/minio-files/data --address ":9000" --console-address ":9001"`, igual ao `CMD` do Dockerfile (a definição está duplicada).
- ✅ O usuário raiz é o literal `admin` (`MINIO_ROOT_USER`); a senha vem de um Docker Secret montado em `/run/secrets/minio_root_password`.
- ✅ Os dados ficam em um volume nomeado montado em `/mnt/minio-files/data`.
- ✅ O serviço entra na rede externa `nginx-ingress-network` com `hostname` por ambiente (`minio-production`, `minio-staging`, `minio-sandbox`).
- ✅ A API (9000) e o console (9001) são publicados em portas do host que variam por ambiente. Ver [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Deploy-e-Ambientes|Deploy e ambientes]].

## Inferências e limitações
- 🔶 Um só caminho de dados e uma só réplica indicam o modo de servidor único (não distribuído); não há redundância de nós.
- 🔶 A rede `nginx-ingress-network` sugere acesso por proxy reverso; a configuração do proxy não está no repositório.

## Relacionamentos
- [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Stack-e-Dependencias|Stack e dependências]] · [[01-Sistemas/MinIO-CGDF/Infra/08-Qualidade/MinIO-CGDF-Infra-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Ver [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Pendencias|Pendências]].
