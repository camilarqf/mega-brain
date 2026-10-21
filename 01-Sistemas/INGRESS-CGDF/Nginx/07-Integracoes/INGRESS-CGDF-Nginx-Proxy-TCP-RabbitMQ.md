---
type: integration
system: INGRESS-CGDF
component: Nginx
repository: ingress-controller
status: confirmado
coverage: completa
analyzed_commit: a51459e9e167b5cb4b34910af8ffe26e583d36da
updated: 2026-10-21
consumer: INGRESS-CGDF
provider: RabbitMQ
tags:
  - ingress
  - nginx
  - rabbitmq
  - stream
sources:
  - nginx.conf
  - nginx-nonprod.conf
---
# INGRESS-CGDF — proxy TCP para o RabbitMQ

Voltar: [[01-Sistemas/INGRESS-CGDF/Nginx/INGRESS-CGDF-Nginx-Index|Índice do Nginx]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| clientes AMQP (não identificados) via `INGRESS-CGDF` | `RabbitMQ` (dois nós) | Nginx `stream` (TCP) | porta `5672`, protocolo repassado sem inspeção | entrada → ingress → broker |

## Evidências
- `nginx.conf` e `nginx-nonprod.conf`, bloco `stream`: upstream `rabbitmq_cluster` e `server` com `listen 5672`.

## Informações confirmadas
- ✅ Balanceamento `least_conn` entre dois nós, `max_fails=3 fail_timeout=30s`.
  - Produção: `production-rabbitmq-stack_rabbit-mq-node-1` e `…-node-2`.
  - Nonprod: `sandbox-rabbitmq-stack_rabbit-mq-node-1` e `…-node-2` (os dois ambientes não produtivos, staging e sandbox, usam o broker de sandbox).
- ✅ `proxy_connect_timeout 5s` e `proxy_timeout 1h` (conexões ociosas por mais de 1 hora são encerradas).
- ✅ Não há TLS, autenticação nem log no bloco `stream`; as credenciais AMQP são tratadas pelo broker.

## Falhas e dependências
- 🔶 Os nomes dos nós são literais no `upstream` (sem `resolver` no `stream`); o Nginx os resolve na partida, então a ausência dos serviços RabbitMQ na rede pode impedir o Nginx de iniciar. Não executado.
- Depende dos serviços Swarm do RabbitMQ estarem na mesma rede do ingress.

## Inferências e limitações
- 🔶 O catálogo registra o RabbitMQ como broker dos eventos de denúncia do `PARTICIPA-DF` (e do `SCI` por contraparte), mas o repositório não identifica quem se conecta por este proxy.
- ❓ Se a porta 5672 é publicada fora da rede Swarm (ver [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Build-Deploy-e-Ambientes|Build, deploy e ambientes]]).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/INGRESS-CGDF/Nginx/01-Visao-Geral/INGRESS-CGDF-Nginx-Arquitetura|Arquitetura]]

## Pendências e próximo passo
- Identificar os clientes AMQP; ver [[01-Sistemas/INGRESS-CGDF/Nginx/99-Controle/INGRESS-CGDF-Nginx-Pendencias|Pendências]].
