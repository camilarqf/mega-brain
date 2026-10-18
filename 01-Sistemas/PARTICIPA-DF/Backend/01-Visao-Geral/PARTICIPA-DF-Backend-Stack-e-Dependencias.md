---
type: reference
system: PARTICIPA-DF
repository: participa-df-backend
status: confirmado
coverage: parcial
analyzed_commit: 4901ad501a86773f40dcd36fb90470a3ba5c0c96
created: 2026-10-18
updated: 2026-10-18
tags:
  - participa-df
  - backend
  - stack
  - dependencias
sources:
  - src/OuvDF.sln
  - src/Directory.Packages.props
  - src/OuvDF.Api/OuvDF.Api.csproj
  - src/OuvDF.Shared/OuvDF.Shared.csproj
  - src/OuvDF.ServicoOuvidoria/OuvDF.ServicoOuvidoria.csproj
  - src/OuvDF.ServicoInformacaoCidadao/OuvDF.ServicoInformacaoCidadao.csproj
  - src/Dockerfile
---

# Stack e dependências

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Perfis-e-Ambientes|Perfis-e-Ambientes]]

## Objetivo
Registrar a tecnologia, os projetos da solução e os pacotes relevantes do backend.

## Evidências
Repositório `participa-df-backend`, commit `4901ad5`. Arquivos em `sources`. Versões conforme `src/Directory.Packages.props` (gerenciamento central de pacotes).

## Informações confirmadas

### Plataforma
- ✅ .NET 5 (`net5.0`) em todos os projetos; `OuvDF.Api` usa `Microsoft.NET.Sdk.Web`.
- ✅ Imagem Docker: build em `mcr.microsoft.com/dotnet/sdk:5.0`, execução em `mcr.microsoft.com/dotnet/aspnet:5.0` (`src/Dockerfile`), publicação `linux-x64`.
- ✅ Banco: SQL Server (`System.Data.SqlClient`, `Microsoft.Data.SqlClient`, `AspNetCore.HealthChecks.SqlServer`, `Microsoft.Extensions.Caching.SqlServer`).

### Projetos da solução e dependências entre eles
| Projeto | Depende de (ProjectReference) | Papel |
|---|---|---|
| `OuvDF.Api` | MailService.Client, PeoplesCheck.Client, ServicoInformacaoCidadao, ServicoOuvidoria, Shared | host HTTP |
| `OuvDF.ServicoOuvidoria` | Iza.Client, Shared, Templates, IntegrationServices | domínio e consultas da Ouvidoria |
| `OuvDF.ServicoInformacaoCidadao` | Shared, Templates | domínio e consultas do SIC |
| `OuvDF.Shared` | MailService.Client | usuários, operadores, segurança, jobs, infra comum |
| `OuvDF.Templates` | — | templates Razor |
| `OuvDF.Iza.Client`, `MailService.Client`, `PeoplesCheck.Client` | DefaultHttpClient | clientes HTTP de serviços externos |
| `OuvDF.DefaultHttpClient` | — | configuração HTTP comum (Polly) |
| `OuvDF.IntegrationServices` | — (pacote `CGDF.DotNet.SDK.PubSub`) | 1 arquivo `.cs` |

### Pacotes principais (versões)
| Área | Pacote | Versão |
|---|---|---|
| SDK interno | `CGDF.DotNet.SDK` (+ `.Data.NHb`, `.Http`, `.Mapper`, `.PolicyManagement`, `.PubSub`, `.Security.Http`, `.Services.HtmlToPDF`, `.Services.Mail`, `.SqlClient`, `.SqlQueryBuilder`) | 5.2.246 |
| SDK interno | `CGDF.DotNet.SDK.Security.Authentication.Jwt` | 5.2.210 |
| SDK interno | `CGDF.SEI.DotNet.SDK` | 1.0.4 |
| Persistência | `NHibernate` / `FluentNHibernate` | 5.3.8 / 3.1.0 |
| Mediação | `MediatR` (+ extensão DI) | 9.0.0 |
| Mapeamento | `AutoMapper` | 10.1.1 |
| Validação | `Flunt` | 2.0.3 |
| Resiliência HTTP | `Microsoft.Extensions.Http.Polly` | 7.0.10 |
| HTTP | `RestSharp` | 108.0.1 |
| Serialização | `Newtonsoft.Json` / `Mvc.NewtonsoftJson` | 13.0.1 / 5.0.6 |
| Logs | `Serilog.AspNetCore` 4.1.0; sinks File 5.0.0, NewRelic.Logs 1.2.0, Discord 1.2.0, Grafana.Loki 7.0.0 | — |
| Templates | `Razor.Templating.Core` | 1.5.0 |
| Outros | `Cronos` 0.7.1, `Winista.MimeDetect` 1.0.1 | — |

### Testes
- ✅ `tests/`: xUnit, Moq, Shouldly, AutoFixture, coverlet (UnitTests); IntegrationTests também usa `StructureMap`, `CGDF.DotNet.SDK.Services.Generators` e `System.Data.SqlClient`. Detalhes no lote 8.

## Inferências e limitações
- 🔶 `Cronos` é referenciado em `OuvDF.Shared.csproj`, mas nenhum `.cs` o usa; não há agendador dentro do código (ver [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Jobs-Agendados|Jobs-Agendados]]).
- 🔶 `Serilog.Sinks.NewRelic.Logs`, `.Discord` e `.File` estão em `OuvDF.Api.csproj`; `Program.cs` usa Console e Grafana Loki. Se NewRelic/Discord/File são ativados por `ReadFrom.Configuration`, é ❓ (não verificado nos valores).
- ❓ O SDK `CGDF.DotNet.SDK.*` é um pacote interno; o comportamento interno (autenticação, pipeline de comandos) não foi lido.
- ❓ Sem fonte nuget privada documentada além de `src/nuget_sources.config` (não lido).
- Os projetos `OuvDF.BCadastro.Client` e `OuvDF.GovBr.Client` não têm código (ver [[01-Sistemas/PARTICIPA-DF/PARTICIPA-DF-Repositorios|Repositórios]]).

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Glossario|Glossário]]

## Pendências e próximo passo
- Confirmar o suporte do .NET 5 (fora de suporte pelo fabricante) no lote 8 (débitos técnicos).
