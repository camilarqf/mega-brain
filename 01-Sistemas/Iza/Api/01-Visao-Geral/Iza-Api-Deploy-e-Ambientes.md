---
type: reference
system: Iza
component: Api
repository: cgdf-iza
status: confirmado
coverage: parcial
analyzed_commit: 988360c5302bb0785f21c4c1bb9f04da02816b7c
updated: 2026-10-22
tags:
  - iza
  - deploy
  - ambientes
  - jenkins
sources:
  - Dockerfile
  - .dockerignore
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/homolog.env.yml
  - .jenkins-pipelines/prod.env.yml
  - deploy/Jenkinsfile
  - deploy/Jenkinsfile.hom
---
# Iza Api — deploy e ambientes

Voltar: [[01-Sistemas/Iza/Api/Iza-Api-Index|Índice da Api]]

## Objetivo
Descrever imagem, parâmetros de implantação e diferenças entre ambientes, sem endereços, credenciais nem segredos (BRAIN-RULES, seção 10).

## Evidências
- `Dockerfile`, `.jenkins-pipelines/*.yml`, `deploy/Jenkinsfile`, `deploy/Jenkinsfile.hom`.

## Informações confirmadas
**Imagem (`Dockerfile`)**
- ✅ `python:3.12`; instala `requirements.txt`; copia só `src/`; `PYTHONPATH=/`; `ENV models_path=/mnt/iza-modelos`; `EXPOSE 8000`.
- ✅ Entrada: `gunicorn src.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind` na porta 8000 em todas as interfaces.
- ✅ `HEALTHCHECK` a cada 30 s com `curl -f http://localhost:8000/health-check` (início após 30 s, 3 tentativas).
- ✅ Os modelos **não** entram na imagem: devem existir no volume `/mnt/iza-modelos` do host.

**Parâmetros do pipeline Swarm (`deployment.params.yml`)**
| Item | Valor |
|---|---|
| Aplicação / imagem / contêiner | `Iza Api` / `iza-api-img` / `iza-api` |
| Ramo principal | `main` |
| Porta interna / externa | 8000 / 8002 |
| Réplicas · memória | 2 · 4G |
| Volume | `/mnt/iza-modelos` |
| Restrições | papel `worker`, rótulo `service==iza` |
| Health check | `health-check` |
| Logs | 5 arquivos de até 5m |
| Regiões | `Homolog` (cluster `homolog-cluster`) e `Producao` (cluster `prod-cluster`), cada uma com credencial e arquivo de ambiente próprios (identificadores omitidos) |

- ✅ `homolog.env.yml` e `prod.env.yml` definem somente `NEW_RELIC_APP_NAME` (valores distintos por ambiente).

**Jenkinsfiles legados (`deploy/`)**
- ✅ Constroem a imagem, enviam a um registry interno (HTTP), removem o contêiner antigo e sobem outro por SSH com `docker run -d --restart unless-stopped`, montando `/mnt/iza-modelos`.
- ✅ Produção (`Jenkinsfile`): 2 servidores ("zona1" e "zona2"), contêiner `cgdf-iza`, porta `8000:8000`. Homologação (`Jenkinsfile.hom`): 1 servidor, contêiner `cgdf-iza-hom`, porta `8002:8000`, `--memory=4g`.
- ✅ Após o build, o `Jenkinsfile` de produção notifica um canal do Discord; no `.hom` a notificação está comentada. Ver [[01-Sistemas/Iza/Api/06-Seguranca/Iza-Api-Seguranca|Segurança]].

## Inferências e limitações
- 🔶 O ingress da CGDF roteia o serviço `cgdf-iza` para `iza-api:8000`, o que coincide com o nome de contêiner e a porta interna do pipeline Swarm; ver [[01-Sistemas/INGRESS-CGDF/Nginx/05-API/INGRESS-CGDF-Nginx-Catalogo-de-Rotas|Catálogo de rotas do ingress]].
- 🔶 Não se sabe qual dos dois mecanismos (Swarm por `deployment.params.yml` ou Jenkinsfile legado) está ativo; o histórico de ramos (`feat/novo-cluster-swarm-*`) sugere migração para o Swarm.
- ✅ Defeito no `Jenkinsfile.hom`: no ramo "sem volume" o comando tem `--memory=4g--restart` (faltou espaço). O ramo não é usado enquanto `volume` estiver definido.
- ❓ URLs, domínios, quem popula `/mnt/iza-modelos` e como os modelos são atualizados/versionados não constam no repositório.

## Relacionamentos
- [[01-Sistemas/Iza/Api/01-Visao-Geral/Iza-Api-Observabilidade-e-Logs|Observabilidade e logs]] · [[01-Sistemas/Iza/Api/02-Dominio/Iza-Api-Modelos-e-Artefatos|Modelos e artefatos]] · [[01-Sistemas/Iza/Api/08-Qualidade/Iza-Api-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Confirmar o mecanismo de deploy ativo e o processo de publicação dos modelos; ver [[01-Sistemas/Iza/Api/99-Controle/Iza-Api-Pendencias|Pendências]].
