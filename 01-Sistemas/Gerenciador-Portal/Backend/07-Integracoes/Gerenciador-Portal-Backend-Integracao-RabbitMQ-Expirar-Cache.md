---
type: integration
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
consumer: Gerenciador-Portal
provider: RabbitMQ
tags:
  - gerenciador-portal
  - integracao
  - rabbitmq
  - cache
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/services/ServidorMedidaProtetivaService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/util/HttpClientImpl.java
  - src/main/resources/application-dev.properties
  - src/main/resources/application-homolog.properties
  - src/main/resources/application-prod.properties
---
# Integração Gerenciador-Portal → RabbitMQ (expirar cache)

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracoes-Externas|Integrações externas do Gerenciador-Portal Backend]] · [[Mapa-de-Integracoes|Mapa de integrações]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `Gerenciador-Portal` (`gerenciador-portal-backend`) | `RabbitMQ` (API HTTP de gestão, via proxy `api-mensageria`) | `PUT` e `POST` JSON, autenticação Basic (Apache HttpClient) | declarar a exchange `medida-protetiva-topic` (fanout) e publicar `{"expirePortal":true,"expireSuperbusca":true}` | saída (publicação) |

## Evidências
`ServidorMedidaProtetivaService.expirarCache`, `HttpClientImpl.put`/`post`, chaves `medidaprotetiva.expirecache.url` e `medidaprotetiva.expirecache.credentials`.

## Informações confirmadas
- ✅ Não usa AMQP: chama a **API HTTP de gestão** (`.../exchanges/<vhost>/medida-protetiva-topic` e `/publish`), com vhost por ambiente (`homolog`; o de produção está em `application-prod.properties`).
- ✅ Corpo da publicação: `routing_key=""`, `payload_encoding=string`, `payload` = JSON `{expirePortal, expireSuperbusca}`, `properties` vazias. Exchange declarada com `type=fanout`, `durable=false`, `auto_delete=false`.
- ✅ Credenciais Basic (usuário:senha) estão em texto nos `application-*.properties` (valores **não** registrados) — com usuários diferentes em `dev` e `homolog` (o de `prod` está em `application-prod.properties`, não comparado).
- ✅ Gatilho: `GET /servidores-medida-protetiva/expirar-cache` ([[01-Sistemas/Gerenciador-Portal/Backend/04-Fluxos/Gerenciador-Portal-Backend-Fluxo-Expirar-Cache-Medida-Protetiva|Fluxo]]).

## Falhas e dependências
- ✅ Resposta do gerenciador sempre `200` (inclusive em falha); `Throwable` é engolido. Status não 2xx do RabbitMQ vira `HttpRequestException`.
- ✅ Sem *timeout*, *retry* nem confirmação de entrega; o cliente HTTP é um singleton com `HttpClients.createDefault()`.
- ✅ A URL usa `http`.

## Inferências e limitações
- 🔶 O consumidor de `expirePortal` é o backend do Portal-Transparencia (mesma exchange e campo; ver [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integrações do Portal]] e a linha de RabbitMQ no [[Mapa-de-Integracoes|mapa]]). Não se sabe se o broker é o mesmo do PARTICIPA-DF/SCI.
- ❓ Quem consome `expireSuperbusca` (serviço de busca do Portal, `apisuperbusca`?).
- ❓ Dono do broker e política de usuários.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Módulo de medida protetiva]] · [[01-Sistemas/Portal-Transparencia/Backend/04-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo de invalidação no Portal]]

## Pendências e próximo passo
- Confirmar o broker de destino e o consumidor `expireSuperbusca`.
