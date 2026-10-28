---
type: architecture
aliases:
  - "SCI Backend — arquitetura (CQRS e eventos de domínio)"
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 299891144fc8c08a314738782442772a8a98b913
updated: 2026-10-23
tags:
  - mensageria
sources:
  - src/SCI.Api/Program.cs
  - src/SCI.Infrastructure.Data/UnitOfWork.cs
  - src/SCI.Application/EventHandlers/PublishDomainEventHandler.cs
  - src/SCI.Application/EventHandlers/StoreEventHandler.cs
  - src/SCI.Domain/_SharedKernel/Abstractions/AggregateEventManager.cs
  - src/SCI.Domain/_SharedKernel/AggregateTypesCatalog.cs
  - src/SCI.Infrastructure.CQRS
  - src/SCI.Infrastructure.Projections
---
# SCI Backend — arquitetura (CQRS e eventos de domínio)

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Descrever camadas, o caminho de comandos e consultas e o ciclo de eventos de domínio.

## Evidências
- `src/SCI.Api/Program.cs` (composição: `ConfigureCQRS`, `RegisterCommandHandlers`, `RegisterQueryHandlers`, `RegisterEventHandlers`, `ConfigureProjectionBuilder`).
- `src/SCI.Infrastructure.Data/UnitOfWork.cs`, `src/SCI.Application/EventHandlers/{PublishDomainEventHandler,StoreEventHandler}.cs`.

## Informações confirmadas
### Camadas (projetos)
| Camada | Projeto | Papel |
|---|---|---|
| Apresentação | `SCI.Api` | controllers, requests/responses, filtros de exceção, políticas de autorização, health checks |
| Aplicação | `SCI.Application` | casos de uso (`UseCases/*`: command + handler MediatR), `EventHandlers`, `Builders`, `IntegrationEvents` |
| Domínio | `SCI.Domain` | agregados, regras (`Rules/*` como `ISpecification`), eventos, repositórios (interfaces), `_SharedKernel` |
| Escrita | `SCI.Infrastructure.Data` | EF Core (`DefaultDbContext`, `EventStoreDbContext`), repositórios, `UnitOfWork<TContext>` |
| Leitura | `SCI.Infrastructure.Projections` | consultas SQL (Dapper) carregadas por `SqlLoader` a partir de recursos embutidos; `QueryProcessor` com filtros, ordenação e paginação |
| Barramento | `SCI.Infrastructure.CQRS` | `ICommandBus`/`IQueryBus` (`CommandBus`, `QueryBus`) e `DomainNotification` |
| Serviços | `SCI.Infrastructure.Services` | JWT, armazenamento em disco, `SecurityId` (AES-GCM), logging, conversão HTML→texto |
| Mensageria | `SCI.IntegrationServices` | consumidor `DenunciaRegistradaConsumer` |
| Documentos | `SCI.GED`, `SCI.Templates` | geração do conteúdo (HTML→PDF) de nota técnica, minuta e relatório do PIP |
| Clientes | `SCI.ParticipaDF.Client`, `SCI.BCadastro.Client`, `SCI.HtmlToPdf.Client`, `SCI.DefaultHttpClient` | integrações HTTP — [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas]] |

### Escrita e leitura separadas
- ✅ Comandos: controller → `ICommandBus.Send` → handler (`IRequestHandler`) → repositório EF → `IUnitOfWork<DefaultDbContext>.SaveChangesAsync()`.
- ✅ Consultas: controller → `IQueryProcessor`/`IQueryBus` → SQL dedicado em `Queries/*` (leitura via Dapper, conexão `ReadModelConnection`).

### Ciclo de eventos de domínio
1. Agregados herdam `AggregateEventManager` e chamam `AddEvent(DomainEvent)`.
2. `UnitOfWork.SaveChangesAsync()` grava a transação EF **primeiro**; depois, para cada evento: preenche `AggregateId`, `UserName` (CPF mascarado), `Unidade`, `Perfil`, `IpRequest`, `UserAgent` (`AuditInfo` do `HttpContext`) e faz `mediator.Publish(new DomainNotification(evento))`.
3. `StoreEventHandler` grava o evento em `TB_EVENTO` pelo `EventStoreDbContext` (nome, tipo do agregado, JSON, usuário, data).
4. `PublishDomainEventHandler` republica o evento concreto (`notification.Metadata`) para handlers específicos, que podem criar processos (`DemandaTratadaEventHandler`), gerar documentos ou publicar eventos de integração (`DenunciaAceitaEventHandler`).
- ✅ Tipos de agregado catalogados em `AggregateTypesCatalog`: Demanda, Denuncia, ProcessoAdmissibilidade, Usuario, AnaliseAdmissibilidade, RevisaoAdmissibilidade, Documento, ProcessoInvestigativoPreliminar, Diligencia, AnalisePip, RevisaoPip, Assunto, Unidade.
- ✅ Não é event sourcing completo: o estado é gravado em tabelas relacionais; o `TB_EVENTO` é um registro de auditoria dos eventos.

### Outros padrões
- ✅ Regras de domínio como `ISpecification<T>` com mensagens (`SpecificationRules.For(x).That(...).Check()`).
- ✅ Filtros de exceção globais: `HandleDomainException`, `HandleInvalidSciOperationException`, `HandleValidationException`, `HandleAuthenticationFailedException`, mais `UseGlobalExceptionHandler`.
- ✅ `FluentValidation` em requests (ex.: `DownloadRequest`).

## Inferências e limitações
- 🔶 Exemplo concreto: `DenunciaAceitaEventHandler` envia `CriarDemandaPorDenunciaCommand` pelo `ICommandBus` dentro do handler de evento (desde `29989114`); falha ali deixa a denúncia aceita sem demanda.
- 🔶 Como os eventos são publicados após o `SaveChanges` e fora da mesma transação, falha em um handler pode deixar o estado gravado sem o efeito derivado (ex.: processo não criado). Não há teste nem compensação verificados.
- `SecurityId` (cifra AES-GCM de identificadores) está registrado em `Program.cs`, mas não encontrei seu uso em requests ou responses de `SCI.Api`/`SCI.Application`.
- `RequestResponseLoggingMiddleware` e `ValidationExceptionMiddleware` existem em `SCI.Api/Middlewares`, mas não encontrei registro deles no pipeline.
- Cobertura parcial: handlers de evento lidos por amostragem.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Modelo-de-Dominio|Modelo de domínio]] · [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco]] · [[01-Sistemas/SCI/Backend/09-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]]

## Pendências e próximo passo
- Ler os demais `EventHandlers` e confirmar a ausência de compensação em falhas.
