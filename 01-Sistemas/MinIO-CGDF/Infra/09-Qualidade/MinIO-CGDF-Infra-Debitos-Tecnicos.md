---
type: technical-debt
aliases:
  - "MinIO CGDF — débitos técnicos"
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
  - README.md
  - .docker/Dockerfile
  - config/production/stack.yml
  - config/staging/stack.yml
  - config/sandbox/stack.yml
---
# MinIO CGDF — débitos técnicos

Voltar: [[01-Sistemas/MinIO-CGDF/Infra/MinIO-CGDF-Infra-Index|Índice da Infra]]

## Objetivo
Registrar riscos e melhorias, separados dos fatos.

## Evidências
- Arquivos listados em `sources`, no commit `f36efc5`.

## Informações confirmadas
Fatos verificados no código:
| # | Fato | Arquivo |
|---|---|---|
| D1 | O README manda montar o volume em `/data`, mas o `CMD` da imagem serve `/mnt/minio-files/data`; o volume do exemplo não recebe os dados. | `README.md`, `.docker/Dockerfile` |
| D2 | O README manda rodar `docker build -t api-minio .` na raiz, mas o Dockerfile está em `.docker/` (sem `-f`, o build não o encontra). | `README.md` |
| D3 | O README descreve só o uso local; não cita os stacks nem os ambientes. | `README.md` |
| D4 | Staging não tem healthcheck e publica só o console. | `config/staging/stack.yml` |
| D5 | O usuário raiz é o literal `admin` nos três ambientes; só a senha é segredo. | `config/*/stack.yml` |
| D6 | O comando do servidor está duplicado entre `CMD` e `command` do stack. | `.docker/Dockerfile`, `config/*/stack.yml` |
| D7 | Uma réplica e um só caminho de dados, sem redundância. | `config/*/stack.yml` |

## Inferências e limitações
Recomendações (🔶, não são fatos):
- Corrigir o README (D1 a D3) e documentar os ambientes.
- Alinhar o healthcheck de staging aos demais ambientes (D4), depois de confirmar que a imagem tem `curl`.
- Avaliar guardar o usuário raiz também como segredo (D5) e fixar o comando em um só lugar (D6).
- Avaliar backup do volume e a necessidade de alta disponibilidade (D7).

## Relacionamentos
- [[01-Sistemas/MinIO-CGDF/Infra/01-Visao-Geral/MinIO-CGDF-Infra-Deploy-e-Ambientes|Deploy e ambientes]]

## Pendências e próximo passo
- Ver [[01-Sistemas/MinIO-CGDF/Infra/99-Controle/MinIO-CGDF-Infra-Pendencias|Pendências]].
