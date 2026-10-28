---
type: index
aliases:
  - "Integrações externas do Gerenciador-Portal Backend"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
sources:
  - pom.xml
  - src/main/resources/application.properties
---
# Integrações externas do Gerenciador-Portal Backend

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Objetivo
Índice das integrações do backend; cada uma tem uma nota canônica (seção 7 do `BRAIN-RULES.md`).

## Evidências
Clientes e configurações no repositório (`S3Config`, `SsoAuthClient`, `HttpClientImpl`, `MongoConfiguration`, `spring.datasource.*`).

## Informações confirmadas
| Integração | Direção | Tecnologia | Nota |
|---|---|---|---|
| Gerenciador → `MinIO-CGDF` 🔶 | saída | S3 (AWS SDK v2) | [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MinIO-S3|MinIO/S3]] |
| Gerenciador → `Keycloak` 🔶 | saída | OIDC (password) | [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SSO-Keycloak|SSO]] |
| Gerenciador → `RabbitMQ` | saída | API HTTP de gestão | [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-RabbitMQ-Expirar-Cache|RabbitMQ]] |
| Gerenciador → `MongoDB-Portal` | saída | Spring Data MongoDB | [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-MongoDB|MongoDB]] |
| Gerenciador → `SQL-Server-Portal` | saída | JDBC/JPA | [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-SQL-Server|SQL Server]] |

- ✅ O backend **não expõe** integrações a outros sistemas além da API usada pelo cliente web; `/healthcheck` e `/prometheus` são consumidos pela plataforma (Docker/Prometheus, 🔶).
- ✅ Não há cliente HTTP para o Portal-Transparencia, para o PARTICIPA-DF, SCI ou qualquer outro sistema do cofre.

## Inferências e limitações
- 🔶 **Relação com o Portal-Transparencia** (informada pelo usuário, sem chamada direta no código): compartilham o banco `DB_PRT_TRANSPARENCIA`, os buckets `portal-arquivos`/`portal-imagens` e a exchange `medida-protetiva-topic` (o Portal consome `expirePortal`). Registrada como hipótese no [[Mapa-de-Integracoes|mapa]].
- ❓ Se o Gerenciador chama `/storage/health` ou `/storage/url` do Portal (pendência 18 do Portal): **não há essa chamada neste repositório**; outro componente (cliente web) poderia fazê-lo.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Pendências e próximo passo
- Ver [[01-Sistemas/Gerenciador-Portal/Backend/99-Controle/Gerenciador-Portal-Backend-Pendencias|Pendências]].
