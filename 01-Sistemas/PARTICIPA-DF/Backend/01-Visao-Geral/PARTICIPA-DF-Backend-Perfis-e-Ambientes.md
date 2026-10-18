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
  - ambientes
  - configuracao
  - docker
sources:
  - src/OuvDF.Api/appsettings.json
  - src/OuvDF.Api/appsettings.Development.json
  - src/OuvDF.Api/appsettings.Homolog.json
  - src/OuvDF.Api/appsettings.Prod.json
  - src/OuvDF.Api/Program.cs
  - src/OuvDF.Api/Config/InitializeApplicationConfig.cs
  - src/Dockerfile
  - .docker/inject-docker-secrets-entrypoint.sh
  - .jenkins-pipelines/deployment.params.yml
  - .jenkins-pipelines/sandbox.env.yml
  - .jenkins-pipelines/staging.env.yml
  - .jenkins-pipelines/prod.env.yml
---

# Perfis e ambientes

Voltar: [[01-Sistemas/PARTICIPA-DF/Backend/PARTICIPA-DF-Backend-Index|Índice do Backend]] · Relacionado: [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Stack-e-Dependencias|Stack]], [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Arquitetura|Arquitetura]]

## Objetivo
Registrar como a configuração é composta por ambiente e como a imagem é construída e implantada. **Somente nomes de chaves**; valores (endereços, segredos, chaves de API) são omitidos de propósito (`BRAIN-RULES.md`, seção 10).

## Evidências
Arquivos em `sources`. Foram lidos os **nomes** das chaves dos `appsettings*.json` e dos YAML de pipeline; os valores não foram reproduzidos. Commit `4901ad5`.

## Informações confirmadas

### Composição da configuração
- ✅ `Program.GetConfigurationBuilder()`: `appsettings.json` (obrigatório) + `appsettings.{ASPNETCORE_ENVIRONMENT ou "Production"}.json` (opcional) + **variáveis de ambiente** (que sobrescrevem os arquivos).
- ✅ Existem os arquivos `appsettings.json`, `.Development`, `.Homolog` e `.Prod`. O csproj ainda referencia `appsettings.Local.json` (não existe no repositório).
- ✅ `InitializeApplicationConfig` traduz chaves para um `IApplicationConfig` (`database-connection-string`, `smtp-*`, `template-directory`, `url-front-end`, `application-date-time`, `url-to-processo-sei`, etc.).
- ✅ Se a seção `LoggerSettings` não existir, a aplicação não sobe (`Program.cs` lança exceção).

### Grupos de chaves (nomes)
| Grupo | Chaves (resumo) |
|---|---|
| Geral | `AllowedHosts`, `CorsOrigins`, `ApplicationDateTime`, `UrlFrontEnd`, `FrontEndURLs.{Principal, RedefinirSenha, SistemaOuvDF, SistemaSicDF, Login}` |
| Segurança | `SecuritySecret`, `Jwt.{Secret, ExpirationDays}` (valores omitidos) |
| Arquivos | `DiretorioArquivos{Raiz, Manifestacao, Pedido, Exportacao, Template}`, `LimiteVolumeArquivo{Manifestacao, PedidoInformacao}` |
| Logs | `Logging.LogLevel.*`, `LoggerSettings.{Uri, AppName, Environment, HealthCheckEndpoint}` |
| Mensageria | `RabbitMqPubSubSettings.{ConnectionStringName, ClientProvidedName, ExchangeName, ConsumerSettings.{MaxProcessingAttempts, PrefetchCount}}`, `ConnectionStrings.RabbitMqConnection` (Development), `RabbitMQSettings.*` (Prod) |
| E-mail | `MailServiceClientSettings.*` (URI, chave de API, timeout, retry, circuit breaker, fallback), `MailServiceApiSettings.{Exchange, RouteKey, VirtualHost, TemplatePath, SubjectEnvironmentDescription}` |
| Clientes HTTP | `IzaClientSettings.{Uri, Timeout, HealthCheckEndpoint}`, `PeoplesCheckClientSettings.*` (URI, chave de API, endpoints de check/challenge, retry, circuit breaker) |
| SEI | `SeiConnectionSettings.{WsURL, WsSiglaSistema, WsIdentificacaoServico}`, `IntegracaoSicSeiSettings.*`, `TipoProcedimentoRecursoTerceiraInstanciaSEI` |
| PDF | `HtmlToPdfConfiguration.{UrlService, Endpoint}` |
| Regras SIC | `ServicoInformacaoCidadaoSettings.*`: prazos em dias (pedido, prorrogação, resposta, recurso, notificação ao órgão, recurso de 3ª instância, notificação CGDF), ids de classificação de resposta, justificativa de prorrogação automática, operador SIC automático |
| Regras Ouvidoria | `ServicoOuvidoriaSettings.{IdTemaZeladoria, PrazoManifestacaoPadrao, UnidadeServicoOuvidoriaSettings.{OgdfId, CoaciId, CqId}}` |
| Operador do sistema | `SharedSettings.IdOperadorSistema` |

- ✅ A string de conexão do banco é lida como `database-connection-string` (a origem exata da chave no `appsettings` não aparece nas listas de chaves; é provável que venha de variável de ambiente ou secret: 🔶).

### Imagem e execução
- ✅ `src/Dockerfile` em dois estágios (SDK 5.0 → ASP.NET 5.0), fuso `America/Sao_Paulo`, instala o agente New Relic .NET e define as variáveis do profiler CoreCLR.
- ✅ `.docker/inject-docker-secrets-entrypoint.sh`: percorre `/run/secrets/*` e exporta cada secret do Docker Swarm como variável de ambiente antes de iniciar a aplicação (imprime apenas os nomes).
- ✅ Chaves em `.jenkins-pipelines/deployment.params.yml`: `app`, `image_definition`, `integration_definition` (`health_check_endpoint: healthcheck`), `constraints_definition`, `regions` (com `cluster`, `credential_id`, `env_file`, `replicas`, `memory`, `network`, `volume`, `secrets`, `labels`, `log_max_*`, `internal_port`). Há uma região de **Staging** e arquivos de variáveis para `sandbox`, `staging` e `prod`.
- ✅ O endpoint de saúde usado pelo deploy é `/healthcheck`.

## Inferências e limitações
- 🔴 O `Dockerfile` contém uma variável de ambiente de licença do New Relic **literal** (valor omitido aqui). Os `appsettings*.json` versionados também têm chaves de nomes sensíveis (`Jwt.Secret`, `SecuritySecret`, `RabbitMQSettings.Password`, chaves de API); se os valores são reais não foi verificado. Tratar no lote 8 ([[01-Sistemas/PARTICIPA-DF/Backend/99-Controle/PARTICIPA-DF-Backend-Pendencias|Pendências]]).
- 🔶 O nome dos ambientes de aplicação é `Development`, `Homolog`, `Prod` (arquivos); os de deploy são sandbox, staging e prod (pipelines). A correspondência exata entre eles (ex.: staging ↔ Homolog) não foi confirmada.
- ❓ Conteúdo (valores) dos `*.env.yml` não foi lido; também a lista de secrets montados por região.
- ❓ Origem da `database-connection-string` por ambiente.

## Relacionamentos
- [[01-Sistemas/PARTICIPA-DF/Backend/01-Visao-Geral/PARTICIPA-DF-Backend-Glossario|Glossário]]

## Pendências e próximo passo
- Confirmar mapeamento entre ambientes de aplicação e de deploy e a origem da string de conexão.
- Registrar os riscos de segredos versionados no lote 8.
