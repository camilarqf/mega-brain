---
type: reference
aliases:
  - "Build, deploy e ambientes"
system: KEYCLOAK-CGDF
component: Servico-Keycloak
repository: keycloak
status: confirmado
coverage: parcial
analyzed_commit: 1755591a3abfeee96a626cedd800187263967154
updated: 2026-10-18
sources:
  - .docker/Dockerfile
  - .docker/inject-docker-secrets-entrypoint.sh
  - .dockerignore
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/staging.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/prod.env.yml
---
# Build, deploy e ambientes

Voltar: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/KEYCLOAK-CGDF-Servico-Index|Índice]] · Relacionado: [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/01-Visao-Geral/KEYCLOAK-CGDF-Servico-Stack-e-Dependencias|Stack-e-Dependencias]], [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/08-Seguranca/KEYCLOAK-CGDF-Servico-Seguranca-e-Autorizacao|Seguranca-e-Autorizacao]]

## Objetivo
Descrever como a imagem é construída e como cada ambiente é configurado. **Valores de hostnames, clusters, credenciais e conexões foram omitidos**; só nomes de chaves.

## Evidências
- Arquivos em `sources`.

## Informações confirmadas
**Build (`.docker/Dockerfile`, multi-stage):**
1. Estágio `spi-builder`: copia `providers/pom.xml` e `providers/src` e executa `mvn clean package -DskipTests` (os testes **não** rodam no build da imagem).
2. Estágio final (Keycloak): copia o entrypoint `inject-docker-secrets-entrypoint.sh`, o jar `ibs-keycloak-extension-1.0.0.jar` para `/opt/keycloak/providers/` e o driver `mssql-jdbc` (download do Maven Central); define `KC_HEALTH_ENABLED=true`; roda `kc.sh build --db=mssql`.
3. Comando: `ENTRYPOINT` = script de secrets; `CMD` = `kc.sh start --optimized --http-enabled=true`.

**Entrypoint (`inject-docker-secrets-entrypoint.sh`):** para cada arquivo em `/run/secrets/`, remove quebras de linha do conteúdo e exporta uma variável de ambiente com o nome do arquivo; imprime apenas o **nome** de cada secret; depois executa `exec "$@"`.

**Pipeline (`deployment.params.yml`):** serviço `Keycloak`, branch `master`, imagem `keycloak-img`, health check `healthcheck`. Três regiões:

| Região | Réplicas | Memória | Porta interna | Arquivo de variáveis |
|---|---|---|---|---|
| Staging | 1 | 1G | 8080 | `staging.env.yml` |
| Sandbox | 1 | 1G | 8080 | `sandbox.env.yml` |
| Producao | 2 | 1G | 8080 | `prod.env.yml` |

Staging e Sandbox rodam no cluster não produtivo; Produção em cluster próprio. Cada região injeta três secrets Swarm nos alvos `KC_DB_URL`, `KEYCLOAK_ADMIN` e `KEYCLOAK_ADMIN_PASSWORD` (nomes das fontes omitidos).

**Variáveis de ambiente por ambiente (só chaves):**

| Variável | Staging | Sandbox | Produção |
|---|---|---|---|
| `KC_HOSTNAME` | sim | sim | não definida |
| `KC_CACHE` (= `local`) | sim | sim | sim |
| `KC_DB` (= `mssql`) | sim | sim | sim |
| `KC_HOSTNAME_STRICT` (= `false`) | não | não | sim |
| `KC_PROXY_HEADERS` (= `xforwarded`) | não | não | sim |
| `KC_HTTP_ENABLED` (= `true`) | não | não | sim |
| `KC_HTTP_RELATIVE_PATH` (= `/keycloak`) | não | não | sim |

## Inferências e limitações
- 🔶 Com 2 réplicas em produção e `KC_CACHE=local`, o cache de sessões não é distribuído entre as réplicas; consequência não verificada (depende do balanceamento).
- ❓ O `Dockerfile` usa `COPY ../providers/...` e `COPY .docker/...`; o contexto de build usado pelo Jenkins não está no repositório.
- ❓ O `Dockerfile` **não** copia `integra-login/`; não há evidência de como o tema chega ao Keycloak (ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/03-Modulos/KEYCLOAK-CGDF-Servico-Tema-Integra-Login|Tema-Integra-Login]]).
- ❓ `health_check_endpoint: healthcheck` não corresponde a um caminho padrão conhecido do Keycloak; não verificado.
- O `Jenkinsfile`/biblioteca de pipeline que consome esses arquivos não está no repositório.

## Relacionamentos
- [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/09-Qualidade/KEYCLOAK-CGDF-Servico-Debitos-Tecnicos|Debitos-Tecnicos]]

## Pendências e próximo passo
- Ver [[01-Sistemas/KEYCLOAK-CGDF/Servico-Keycloak/99-Controle/KEYCLOAK-CGDF-Servico-Pendencias|Pendências]].
