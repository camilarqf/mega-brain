---
type: flow
system: Portal-Transparencia
component: Backend
repository: portal-transparencia-backend
status: confirmado
coverage: completa
analyzed_commit: 9434e58f35284618d236f25b3ed2f2b307a7e345
updated: 2026-10-19
tags:
  - portal-transparencia
  - backend
  - fluxo
  - rabbitmq
  - cache
sources:
  - src/main/java/br/gov/df/transparencia/servico/mascaramento/MascaramentoAMQService.java
  - src/main/java/br/gov/df/transparencia/servico/comum/CacheControlService.java
  - src/main/java/br/gov/df/transparencia/api/comum/CacheControlController.java
  - src/main/java/br/gov/df/transparencia/servico/mascaramento/MascaramentoService.java
---
# Fluxo: invalidação do cache de valores mascarados

Voltar: [[01-Sistemas/Portal-Transparencia/Backend/Portal-Transparencia-Backend-Index|Índice do Backend]] · Módulo: [[01-Sistemas/Portal-Transparencia/Backend/03-Modulos/Portal-Transparencia-Backend-Cache-e-Mascaramento|Cache-e-Mascaramento]]

## Objetivo
Mostrar como uma alteração na lista de valores protegidos chega às respostas da API sem esperar a expiração do cache.

## Evidências
`MascaramentoAMQService`, `CacheControlService`, `CacheControlController` e `MascaramentoService` (commit `9434e58f`).

## Informações confirmadas
Atores: um **publicador externo** (não identificado), o RabbitMQ, cada instância do backend e quem chame `GET /cache-expire/*`.

1. ✅ Na subida, o backend declara a exchange **fanout** `medida-protetiva-topic` (não durável, sem auto-delete), uma fila **anônima** exclusiva por instância (`AnonymousQueue`) e o binding entre elas.
2. ✅ Um `@RabbitListener` na fila anônima recebe cada mensagem, lê o corpo como JSON (`json-simple`) e procura a chave booleana `expirePortal`.
3. ✅ Se `expirePortal == true`, chama `CacheControlService.expireCacheValoresMascarados()`, que limpa `cacheMascarados` **e** `cacheRemuneracao` e devolve `CacheExpireInfo`.
4. ✅ A próxima chamada a `consultarDadosMascarados()` relê `[Servidor].[TB_MEDIDA_PROTETIVA]` e repovoa o cache; o `@Around` passa a filtrar com os valores novos.
5. ✅ Mensagem nula, sem a chave ou com `false` é ignorada; erros de parse/execução são impressos em `System.err` (sem reentrega).
6. ✅ Alternativa manual: `GET /cache-expire/valores-mascarados` (mesmo efeito, só na instância que recebe a chamada); `/cache-expire/remuneracao` e `/cache-expire/despesa-filtros` limpam os outros dois caches.
7. ✅ Sem mensagem, o cache de mascarados expira sozinho em 3 minutos após a escrita.

## Inferências e limitações
- 🔶 Por ser fila anônima, mensagens publicadas enquanto uma instância está fora do ar se perdem para ela; o limite de 3 minutos do cache de mascarados limita o atraso, mas o `cacheRemuneracao` (1 dia) só é limpo por essa via ou manualmente.
- 🔶 O RabbitMQ aparece nos perfis `dev`, `hom` e `prod`; o `management.health.rabbit` está desligado em `hom` e `prod`.
- ❓ Quem publica `expirePortal` (nome do sistema, evento que dispara) não é identificável aqui.

## Relacionamentos
- [[01-Sistemas/Portal-Transparencia/Backend/07-Integracoes/Portal-Transparencia-Backend-Integracoes-Externas|Integracoes-Externas]] · [[01-Sistemas/Portal-Transparencia/Backend/01-Visao-Geral/Portal-Transparencia-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Pendências e próximo passo
- Identificar o publicador da mensagem (ver Pendências).
