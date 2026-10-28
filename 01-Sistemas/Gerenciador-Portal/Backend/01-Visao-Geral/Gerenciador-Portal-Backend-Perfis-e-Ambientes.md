---
type: reference
aliases:
  - "Perfis e ambientes"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - src/main/resources/application.properties
  - src/main/resources/application-dev.properties
  - src/main/resources/application-homolog.properties
  - src/main/resources/application-local.properties
  - src/main/resources/application-prod.properties
  - .jenkins-pipelines/staging.env.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/prod.env.yml
---
# Perfis e ambientes

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

> Somente **nomes de chaves** e valores não sensíveis. Valores de usuário, senha, token e hosts não são registrados (`BRAIN-RULES.md`, seção 10).

## Objetivo
Mapear perfis Spring, ambientes de deploy e as chaves de configuração que o código lê.

## Evidências
- `application.properties` (comum): `spring.profiles.active=@activatedProperties@`, `server.port=8080`, `server.tomcat.max-threads=100`, Hikari (`maximum-pool-size=4`, `connection-timeout=60000`, `max-lifetime=300000`), `spring.http.multipart.max-file-size`/`max-request-size` = 900MB, `spring.jpa.show-sql=true`, buckets `storage.bucket.arquivos`/`storage.bucket.imagens`, `endpoints.health.id=healthcheck`, `so.auth.client-secret` vindo de `${SSO_CLIENT_SECRET}`.
- Pipelines: `staging.env.yml` e `sandbox.env.yml` definem `SPRING_PROFILES_ACTIVE=homolog`; `prod.env.yml` define `prod`.

## Informações confirmadas
| Perfil | Quando | Diferenças relevantes (✅) |
|---|---|---|
| `dev` | Maven `desenvolvimento` | banco de desenvolvimento; pastas locais Windows para arquivos/imagens; MinIO por endpoint fixo; **sem** chaves `so.auth.*`/`autorizacao.*` neste arquivo |
| `homolog` | Staging e Sandbox | banco de homologação; `logging.file=gerenciador.log`; pasta `/mnt/gerenciador_share/...`; MinIO `minio-sandbox`; `storage.access-key`/`secret-key` de `${STORAGE_ACCESS_KEY}`/`${STORAGE_SECRET_KEY}`; SSO e autorização (`autorizacao.id-orgao`, `autorizacao.id-unidades`); log DEBUG do AWS SDK e do Apache HTTP |
| `prod` | Produção | MinIO `minio-production`; mesmos chaves de storage, SSO e autorização; realm de produção |
| `local` | Maven `local` | `application-local.properties` está no `.gitignore` e **não é versionado** (existe só na máquina de trabalho); não faz parte do commit analisado e não foi documentado |

Chaves lidas pelo código (todas confirmadas por `@Value`): `default.diretorio`, `default.imagem.diretorio`, `storage.endpoint`, `storage.access-key`, `storage.secret-key`, `storage.bucket.arquivos`, `storage.bucket.imagens`, `so.auth.url`, `so.auth.client-id`, `so.auth.client-secret`, `so.auth.id-orgao`, `autorizacao.id-orgao`, `autorizacao.id-unidades`, `dev.usuario.cpf`, `dev.usuario.senha`, `medidaprotetiva.expirecache.url`, `medidaprotetiva.expirecache.credentials`, `spring.data.mongodb.{host,port,user,pass,database}`, `spring.datasource.{url,username,password}`.

Variáveis de ambiente/secrets: `SSO_CLIENT_SECRET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` (também lidas por `S3Config` via `System.getenv`).

## Inferências e limitações
- ✅ A chave `access.token` existe nos perfis `dev`, `homolog` e `prod` (e no `local`, não versionado), mas **nenhuma classe a lê** (busca em `src/main/java`): configuração morta.
- ✅ `url.servidor.api.sigrh` e `url.portal.verificar.sutcs` existem em `prod` (e no `local`), mas **nenhuma classe as lê**: resquício de uma autenticação anterior (🔶 SIGRH/SUTCS), sem uso no commit.
- ✅ O perfil `prod` usa o banco Mongo `superbuscaportal`; `dev`/`homolog` usam `superbuscaportal_hom`. A exchange do RabbitMQ usa o vhost `homolog` em `dev`/`homolog` e `prod` em produção.
- ✅ `dev.usuario.cpf`/`dev.usuario.senha` existem em todos os perfis versionados, inclusive `prod` ([[01-Sistemas/Gerenciador-Portal/Backend/08-Seguranca/Gerenciador-Portal-Backend-Seguranca-e-Autorizacao|Segurança]]).
- 🔶 Os perfis `dev`, `homolog` e `local` apontam para o mesmo conjunto de bancos e brokers com credenciais próprias versionadas; `prod` também (valores não registrados).
- ❓ Staging não monta os secrets `STORAGE_*` no pipeline (só o do SSO): sem eles `S3Config` lança `IllegalStateException` na inicialização. Se Staging funciona, a origem das credenciais não está no repositório.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Deploy-e-Pipeline|Deploy e pipeline]]
- [[01-Sistemas/Gerenciador-Portal/Backend/01-Visao-Geral/Gerenciador-Portal-Backend-Stack-e-Dependencias|Stack]]

## Pendências e próximo passo
- Confirmar quais secrets existem em Staging e quem consome `access.token`.
