---
type: flow
aliases:
  - "Fluxo de expirar o cache de medida protetiva"
system: Gerenciador-Portal
component: Backend
repository: gerenciador-portal-backend
status: confirmado
coverage: parcial
analyzed_commit: 14b185feeac4f5889a0ce8041a3b5baaead0334b
created: 2026-10-27
updated: 2026-10-27
tags:
  - mensageria
sources:
  - src/main/java/br/gov/df/cgdf/gerenciador/services/ServidorMedidaProtetivaService.java
  - src/main/java/br/gov/df/cgdf/gerenciador/util/HttpClientImpl.java
---
# Fluxo de expirar o cache de medida protetiva

Voltar: [[01-Sistemas/Gerenciador-Portal/Backend/Gerenciador-Portal-Backend-Index|Índice do Backend]]

## Objetivo
Explicar como uma alteração na lista de medida protetiva é comunicada aos sistemas que guardam cache.

## Evidências
`ServidorMedidaProtetivaService.expirarCache` e `HttpClientImpl` (`put`/`post`); lado consumidor documentado em [[01-Sistemas/Portal-Transparencia/Backend/05-Fluxos/Portal-Transparencia-Backend-Fluxo-Invalidacao-de-Cache-de-Mascarados|Fluxo de invalidação do Portal]].

## Informações confirmadas
1. ✅ O operador cadastra ou exclui uma pessoa (`POST`/`DELETE /servidores-medida-protetiva/...`): grava na tabela e no log. **Não há chamada automática ao cache.**
2. ✅ `GET /servidores-medida-protetiva/expirar-cache` monta o cabeçalho `Authorization: Basic …` a partir de `medidaprotetiva.expirecache.credentials` (`usuario:senha`, valor não registrado).
3. ✅ `PUT <medidaprotetiva.expirecache.url>` declara a exchange com `{"type":"fanout","auto_delete":false,"durable":false}`.
4. ✅ `POST <medidaprotetiva.expirecache.url>/publish` publica na API HTTP de gestão do RabbitMQ: `routing_key` vazia, `payload_encoding=string`, `payload` = `{"expirePortal":true,"expireSuperbusca":true}`.
5. ✅ A resposta do endpoint é sempre `200`: `ok` ou `failed [<mensagem>]` (exceção capturada com `Throwable`, `printStackTrace`).

A URL tem a forma `http://<host>/api-mensageria/exchanges/<vhost>/medida-protetiva-topic` (nome da exchange confirmado; host omitido).

## Falhas e dependências
- ✅ Depende de `HttpClientImpl` (Apache HttpClient 4.3.6): qualquer status fora de 2xx vira `HttpRequestException`.
- ✅ A guarda de URL vazia está incorreta (`&&` em vez de `||`); sem URL configurada a chamada lança `NullPointerException` e o `expirar-cache` falha com `500` (a exceção ocorre antes do `try`).
- ✅ A exchange é criada como **não durável** (`durable=false`) e sem confirmação; se o broker reiniciar, a exchange e as filas ligadas se perdem.
- ✅ Credenciais do broker estão versionadas nos `application-*.properties` (valores não registrados).

## Inferências e limitações
- 🔶 `expirePortal` é consumido pelo backend do Portal-Transparencia (exchange e campo coincidem) e `expireSuperbusca` por um serviço de busca; este último não foi identificado.
- ❓ Se o cliente web dispara `expirar-cache` após cada alteração.

## Relacionamentos
- [[01-Sistemas/Gerenciador-Portal/Backend/07-Integracoes/Gerenciador-Portal-Backend-Integracao-RabbitMQ-Expirar-Cache|Integração com o RabbitMQ]] · [[01-Sistemas/Gerenciador-Portal/Backend/03-Modulos/Gerenciador-Portal-Backend-Modulo-Medida-Protetiva|Módulo de medida protetiva]]

## Pendências e próximo passo
- Confirmar o consumidor `expireSuperbusca` e o gatilho no cliente.
