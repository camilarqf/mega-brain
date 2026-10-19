---
type: integration
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
consumer: SCI
provider: RabbitMQ
tags:
  - sci
  - integracao
  - rabbitmq
  - participa-df
  - denuncia
sources:
  - src/SCI.Api/Program.cs
  - src/SCI.IntegrationServices/EventConsumers/DenunciaRegistradaConsumer.cs
  - src/SCI.Application/IntegrationEvents
  - src/SCI.Application/EventHandlers/DenunciaAceitaEventHandler.cs
  - src/SCI.Application/EventHandlers/DenunciaRecusadaEventHandler.cs
  - src/SCI.Api/HealthChecks/RabbitMqHealthCheck.cs
---
# Integração SCI ⇄ PARTICIPA-DF por eventos (RabbitMQ)

Voltar: [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas do SCI Backend]]

## Visão geral
| Consumidor | Provedor | Tecnologia | Contrato | Direção |
|---|---|---|---|---|
| `SCI` | `RabbitMQ` (broker) | `CGDF.DotNet.SDK.PubSub` | canal `denuncia-registrada` → `DenunciaRegistrada` | entrada (consome) |
| `SCI` | `RabbitMQ` (broker) | idem | canais `denuncia-aceita` → `DenunciaAceita` e `denuncia-recusada` → `DenunciaRecusada` | saída (publica) |

Contraparte 🔶: `PARTICIPA-DF` (publica `denuncia-registrada`; consome `denuncia-aceita` e `denuncia-recusada`).

## Evidências
- `Program.cs`: `ConfigurePubSub(...).AddConsumer<DenunciaRegistradaConsumer, DenunciaRegistrada>("denuncia-registrada")`.
- `IntegrationEvents/{DenunciaRegistrada,DenunciaAceita,DenunciaRecusada}.cs`: `Producer = "sci"`, `EventVersion = 1`, `ChannelName` do canal; `CorrelationId` e `EventId` novos por publicação.
- Configuração `RabbitMqPubSubSettings`: `ConnectionStringName`, `ClientProvidedName`, `ExchangeName`, `ConsumerSettings` (valores não lidos).

## Informações confirmadas
- ✅ **Payloads**: `DenunciaRegistrada` {`DenunciaId` (long), `UnidadeOrigemId`, `UnidadeDestinoId`, `ProtocoloRelacionado?`, `Identificada`}; `DenunciaAceita` {`DenunciaId`, `Usuario`, `IdentificadorProcessual`}; `DenunciaRecusada` {`DenunciaId`, `Usuario?`, `IdentificadorProcessual?`, `MotivoRecusa`}.
- ✅ **Consumo** (`DenunciaRegistradaConsumer`): idempotência por `DenunciaId` (ignora duplicata); resolve a unidade pelo vínculo `PARTICIPA_DF`; sem vínculo → publica `denuncia-recusada` com motivo fixo; com vínculo → `CriarDenunciaCommand`.
- ✅ **Publicação**: ao aceitar/recusar a denúncia, os `EventHandlers` publicam o evento com o `IntegrationEventPublisher`/`INotificationPublisher`.
- ✅ **Correspondência com o outro lado**: o [[01-Sistemas/PARTICIPA-DF/Backend/07-Integracoes/PARTICIPA-DF-Backend-Integracoes-Externas|backend do PARTICIPA-DF]] documenta (commit `4901ad5`) os mesmos três canais com os papéis inversos. O SCI é, portanto, a contraparte antes não identificada ("COACI/sistema correcional").
- ✅ **Health check**: `RabbitMqHealthCheck` verifica a conexão/canal no `/health`.

## Falhas e dependências
- 🔶 Se `CriarDenunciaCommand` lançar exceção no consumidor, o comportamento de reentrega depende do SDK (`ConsumerSettings` não lidos).
- ✅ Recusa por ausência de vínculo é a única falha de negócio tratada explicitamente.
- Dependência: broker RabbitMQ acessível; unidade com vínculo `PARTICIPA_DF` cadastrado.

## Inferências e limitações
- 🔶 A correspondência foi confirmada por nomes de canal e payload nos dois repositórios; o código do `PARTICIPA-DF` não foi relido nesta análise (apenas a documentação do cofre).
- ❓ Nome do exchange e da fila (valores de configuração).

## Relacionamentos
- [[Mapa-de-Integracoes|Mapa de integrações]] · [[01-Sistemas/SCI/Backend/03-Modulos/SCI-Backend-Modulo-Denuncia-e-Demanda|Denúncia e Demanda]] · [[01-Sistemas/SCI/Backend/04-Fluxos/SCI-Backend-Fluxo-Denuncia-ate-Admissibilidade|Fluxo]]

## Pendências e próximo passo
- Confirmar com o time o comportamento de reentrega/DLQ.
