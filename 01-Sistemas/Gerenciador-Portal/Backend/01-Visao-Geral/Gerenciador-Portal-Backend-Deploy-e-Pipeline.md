---
type: reference
aliases:
  - "Deploy e pipeline"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - .docker/Dockerfile
  - .docker/inject-docker-secrets-entrypoint.sh
  - inject-docker-secrets-entrypoint.sh
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/prod.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/staging.env.yml
---
# Deploy e pipeline

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Descrever como o backend é empacotado e implantado (Docker Swarm via Jenkins).

## Evidências
`.docker/Dockerfile`, `.docker/inject-docker-secrets-entrypoint.sh` (a cópia da raiz difere só pela quebra de linha final), `.jenkins-pipelines/*.yml`.

## Informações confirmadas
- ✅ **Imagem em dois estágios**: build `maven:3.5.2-jdk-8-alpine` (`mvn -Dmaven.test.skip=true -P $SPRING_PROFILES_ACTIVE package`) e runtime `eclipse-temurin:8-jre-alpine`; timezone `America/Sao_Paulo`; `curl` para o `HEALTHCHECK` (`GET http://localhost:8080/healthcheck`, 30s/10s/3 tentativas).
- ✅ **Entrypoint** `inject-docker-secrets-entrypoint.sh`: lê cada arquivo de `/run/secrets/*`, exporta como variável de ambiente (nome do arquivo = nome da variável), imprime apenas o **nome** de cada secret no log e executa `java -jar /novoGerenciador.jar`.
- ✅ **Jenkins** (`deployment.params.yml`): app "Gerenciador do Portal da Transparência", branch principal `master`, imagem `gerenciador-portal-transparencia-backend-img`, health check `healthcheck`, rede `nginx-ingress-network`, porta interna 8080, volume `/mnt/gerenciador_share`.

| Região | Contêiner | Memória | Réplicas | Secrets (destino) |
|---|---|---|---|---|
| Staging | `gerenciador-portal-transparencia-backend-staging` | 1G | 1 | `SSO_CLIENT_SECRET` |
| Sandbox | `gerenciador-portal-transparencia-backend-sandbox` | 1G | 1 | `SSO_CLIENT_SECRET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` |
| Produção | `gerenciador-portal-transparencia-backend` | 2G | 2 | `SSO_CLIENT_SECRET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` |

## Falhas e dependências
- ✅ Os testes são **ignorados** no build da imagem (`-Dmaven.test.skip=true`).
- ✅ O `Dockerfile` usa `COPY ../pom.xml` e `COPY ../src` (caminhos fora do contexto padrão) e define `ENV SPRING_PROFILES_ACTIVE=SPRING_PROFILES_ACTIVE`; o `-P` do Maven recebe esse valor. ❓ Não está claro como o Jenkins fornece o contexto e o perfil Maven reais (o perfil Maven e o perfil Spring têm nomes diferentes: `producao` × `prod`).
- ✅ O agente New Relic (`newrelic.jar`) está nos recursos, mas o comando de inicialização **não** usa `-javaagent`.
- ✅ O volume `/mnt/gerenciador_share` é montado, mas `ArquivoService`/`ImagemService` enviam ao MinIO; o diretório só é usado por `CommonService.deletarArquivo` ([[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Arquivos-e-Relatorios|Módulo de arquivos]]).

## Inferências e limitações
- 🔶 Staging sem `STORAGE_*` ([[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Perfis-e-Ambientes|Perfis e ambientes]]).
- 🔶 O catálogo de rotas do [[01-Sistemas/INGRESS-CGDF/INGRESS-CGDF-Index|INGRESS-CGDF]] tem a rota `gerenciador-portal-transparencia` → `gerenciador-portal-transparencia-backend:8080`, cujo nome coincide com o contêiner de produção deste pipeline (correspondência por nome, não confirmada). Ver [[Mapa-de-Integracoes|Mapa de integrações]].
- ❓ O Jenkins em si não foi analisado.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Perfis-e-Ambientes|Perfis e ambientes]]
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|Integração com MinIO/S3]]

## Pendências e próximo passo
- Confirmar o contexto de build do Jenkins e o perfil Maven efetivamente usado em produção.
