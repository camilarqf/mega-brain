---
type: reference
system: SCI
component: Backend
repository: sci-backend
status: confirmado
coverage: parcial
analyzed_commit: 8e3c8648386d0ee6767df7819faea9cdd44bef9c
updated: 2026-10-19
tags:
  - sci
  - backend
  - stack
sources:
  - Directory.Packages.props
  - global.json
  - SCI.sln
  - src/SCI.Api/SCI.Api.csproj
  - src/SCI.Api/Program.cs
  - .docker/Dockerfile
---
# SCI Backend — stack e dependências

Voltar: [[01-Sistemas/SCI/Backend/SCI-Backend-Index|Índice do Backend]]

## Objetivo
Registrar linguagem, framework, bibliotecas e projetos da solução.

## Evidências
- `src/SCI.Api/SCI.Api.csproj` e `src/SCI.Domain/*.csproj`: `TargetFramework` = `net10.0`. `global.json`: SDK `10.0.203`. `Directory.Packages.props`: gerenciamento central de versões.
- `src/SCI.Api/Program.cs`: composição da aplicação.

## Informações confirmadas
- ✅ **Plataforma**: C#, ASP.NET Core, .NET 10 (EF Core SQL Server `10.0.5`).
- ✅ **Padrões e bibliotecas** (versões de `Directory.Packages.props`): MediatR `12.5.0`, FluentValidation `11.11.0`, Dapper `2.1.72` (leitura), Swashbuckle `10.2.3`, Serilog (`Serilog.AspNetCore 10.0.0`, sink Grafana Loki), OpenTelemetry com exportador Prometheus, Polly (políticas de HTTP nos clientes), `Microsoft.FeatureManagement`, `QRCoder` (QR Code nos documentos), `CGDF.DotNet.SDK.PubSub 5.2.246` (RabbitMQ).
- ✅ **Persistência**: SQL Server; dois `DbContext` (`DefaultDbContext`, `EventStoreDbContext`) mais leitura via Dapper — [[01-Sistemas/SCI/Backend/02-Dominio/SCI-Backend-Banco-e-Migrations|Banco e migrations]].
- ✅ **Solução** (`SCI.sln`): `SCI.Api`, `SCI.Application`, `SCI.Domain`, `SCI.Infrastructure.{CQRS,Data,Projections,Services}`, `SCI.IntegrationServices`, `SCI.GED`, `SCI.Templates`, `SCI.DefaultHttpClient`, clientes `SCI.ParticipaDF.Client`, `SCI.BCadastro.Client`, `SCI.HtmlToPdf.Client`; testes `SCI.Integration.Tests` e `SCI.Tests.Helpers`. Detalhe de camadas: [[01-Sistemas/SCI/Backend/01-Visao-Geral/SCI-Backend-Arquitetura-CQRS-e-Event-Sourcing|Arquitetura]].
- ✅ **Health e métricas**: `GET /health` (SQL Server, RabbitMQ, armazenamento compartilhado, logger) e endpoint de scraping Prometheus.
- ✅ **Contêiner e deploy**: `.docker/Dockerfile`, `.docker/inject-docker-secrets-entrypoint.sh`, `.jenkins-pipelines/{deployment.params,prod.env,sandbox.env,staging.env}.yml` (conteúdo dos `.env.yml` **não lido**).
- ✅ **Feature flags** (`FeatureManagement`): `Support.GenerateDatabase` e `Pip.Criar`, ambas `false` em `appsettings.json`.
- ✅ **Seções de configuração** (somente nomes de chaves): `ConnectionStrings`, `DefaultDatabaseSettings`, `ReadModelDatabaseSettings`, `JwtSettings`, `HtmlToPdfClientSettings`, `ParticipaDFClientSettings`, `BCadastroClientSettings`, `GEDSettings`, `FeatureManagement`, `RabbitMqPubSubSettings`, `DataSecuritySettings`, `LoggerSettings`.

## Inferências e limitações
- ⚠️ **Conflito de documentação**: o `LEVANTAMENTO_TECNICO.md` (não versionado) cita .NET 8 e EF Core 8.0.8; o código atual usa .NET 10 e EF Core 10.0.5. Prevalece o código.
- Existem dois projetos de cliente HTML→PDF: `src/SCI.HtmlToPdf.Client` (na solução e usado em `Program.cs`) e `src/SCI.HtmlToPdfClient` (fora da solução). ✅ Os dois arquivos `Services/HtmlToPdfApiClient.cs` são idênticos (diff vazio): duplicata, sem uso encontrado do segundo.
- `Legacy/` tem outra solução (`backend_cgdf.sln`), não analisada.
- Valores de configuração e `appsettings*.json` não foram reproduzidos.

## Relacionamentos
- [[01-Sistemas/SCI/Backend/08-Qualidade/SCI-Backend-Debitos-Tecnicos|Débitos técnicos]] · [[01-Sistemas/SCI/Backend/07-Integracoes/SCI-Backend-Integracoes-Externas|Integrações externas]]

## Pendências e próximo passo
- Confirmar o papel de `src/SCI.HtmlToPdfClient` e de `Legacy/`.
